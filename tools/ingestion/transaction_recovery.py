#!/usr/bin/env python3
"""Fail-closed, offline recovery planner for Pass B semantic transactions.

This does not call GitHub or rewrite semantic material. The caller uses the
ordinary GitHub file actions in the order: semantic -> manifest -> checkpoint.
A denied semantic payload must not be re-submitted through an alternate API.
Journal files contain original semantic bytes and MUST remain in a trusted
persistent working directory, never a substitute GitHub upload endpoint.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import yaml

GATE = Path(__file__).with_name('ingestion_gate.py')
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
PATH = re.compile(r'(?:references|rule|rules|equipment|options|entities|world|procedure|procedures)/[\w./-]+\.yml\Z')

class RecoveryError(ValueError):
    pass

def require(condition, code):
    if not condition: raise RecoveryError(code)

def sha256(raw): return hashlib.sha256(raw).hexdigest()
def git_blob(raw): return hashlib.sha1(('blob %s\0' % len(raw)).encode()+raw).hexdigest()

class StrictLoader(yaml.SafeLoader): pass

def _mapping(loader, node):
    result={}
    for key, value in node.value:
        k=loader.construct_object(key)
        require(isinstance(k,str), 'yaml_nonstring_key')
        require(k not in result, 'yaml_duplicate_key')
        result[k]=loader.construct_object(value)
    return result

StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)

def parse_yaml(raw):
    try: data=yaml.load(raw,Loader=StrictLoader)
    except (yaml.YAMLError, UnicodeDecodeError) as exc: raise RecoveryError('invalid_yaml') from exc
    require(isinstance(data,dict),'yaml_not_mapping')
    return data

def _write_once(path:Path, payload:bytes):
    if path.exists():
        require(path.read_bytes()==payload,'journal_collision_or_corruption')
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(str(path),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(fd,'wb') as target:
        target.write(payload);target.flush();os.fsync(target.fileno())

def stage(baseline:Path, candidate:Path, repo_path:str, source:str, pdf_sha:str, journal:Path, gate:Path=GATE):
    require(bool(HEX64.fullmatch(pdf_sha)),'invalid_pdf_hash')
    require(bool(PATH.fullmatch(repo_path)) and '..' not in repo_path.split('/'),'invalid_semantic_path')
    require(journal.is_dir() or not journal.exists(),'journal_not_directory')
    command=[sys.executable,str(gate),'prepare',str(baseline),str(candidate),repo_path,source,pdf_sha]
    run=subprocess.run(command,text=True,capture_output=True,check=False)
    require(run.returncode==0,'gate_prepare_failed')
    try: plan=json.loads(run.stdout)
    except (ValueError,TypeError) as exc: raise RecoveryError('invalid_gate_response') from exc
    require(plan.get('status')=='preflighted' and plan.get('protocol')=='sr3-gate/v1','not_preflighted')
    b,c=baseline.read_bytes(),candidate.read_bytes()
    require(plan.get('candidate_sha256')==sha256(c) and plan.get('expected_blob_sha')==git_blob(c),'candidate_changed_after_preflight')
    require(plan.get('path')==repo_path and plan.get('source')==source and plan.get('pdf_sha256')==pdf_sha,'plan_provenance_mismatch')
    journal.mkdir(parents=True,exist_ok=True)
    _write_once(journal/'baseline.yml',b)
    _write_once(journal/'candidate.yml',c)
    _write_once(journal/'plan.json',(json.dumps(plan,sort_keys=True,indent=2)+'\n').encode())
    return {'status':'staged','journal':str(journal),'plan':plan,'baseline_sha256':sha256(b)}

def load_journal(journal:Path):
    try:
        plan=json.loads((journal/'plan.json').read_text())
        baseline=(journal/'baseline.yml').read_bytes()
        candidate=(journal/'candidate.yml').read_bytes()
    except (ValueError,OSError) as exc: raise RecoveryError('journal_unavailable_or_invalid') from exc
    require(plan.get('status')=='preflighted' and plan.get('protocol')=='sr3-gate/v1','journal_not_preflighted')
    require(sha256(candidate)==plan['candidate_sha256'] and git_blob(candidate)==plan['expected_blob_sha'],'journal_bytes_changed')
    require(isinstance(parse_yaml(baseline),dict) and isinstance(parse_yaml(candidate),dict),'journal_yaml_invalid')
    return plan,candidate

def inspect(journal:Path, observed_blob_sha:str|None, commit_sha:str|None):
    plan,candidate=load_journal(journal)
    if observed_blob_sha is None: return {'status':'absent','action':'normal_write_if_permitted','path':plan['path']}
    require(bool(HEX40.fullmatch(observed_blob_sha)),'invalid_observed_blob_sha')
    if observed_blob_sha!=plan['expected_blob_sha']:
        return {'status':'divergent_blob','action':'investigate_no_overwrite','path':plan['path'], 'observed_blob_sha':observed_blob_sha}
    if commit_sha is None:
        return {'status':'matching_blob_commit_unknown','action':'resolve_real_commit_before_confirm','path':plan['path']}
    require(bool(HEX40.fullmatch(commit_sha)),'invalid_commit_sha')
    return {'status':'verified','receipt':{**plan,'status':'verified','commit_sha':commit_sha,'readback_blob_sha':observed_blob_sha}}

def pages(x):
    m=re.fullmatch(r'(\d+)(?:-(\d+))?',str(x))
    require(m is not None,'invalid_page_range')
    first,last=int(m[1]),int(m[2] or m[1]);require(first<=last,'invalid_page_range')
    return set(range(first,last+1))

def state(manifest,checkpoint):
    require(manifest.get('id')==checkpoint.get('active_source'),'source_mismatch')
    m_done=manifest.get('done');m_next=manifest.get('next')
    c_done=checkpoint.get('completed_through');c_next=checkpoint.get('resume_at')
    require(isinstance(m_done,dict) and isinstance(m_next,dict) and isinstance(c_done,dict) and isinstance(c_next,dict),'invalid_boundaries')
    b1=(m_done.get('p'),m_done.get('pdf'),m_next.get('p'),m_next.get('pdf'))
    b2=(c_done.get('printed_page'),c_done.get('pdf_page'),c_next.get('printed_page'),c_next.get('pdf_page'))
    require(b1==b2,'boundary_mismatch')
    pending=[x.get('id') for x in manifest.get('pending',[]) if isinstance(x,dict)]
    require(len(pending)==len(manifest.get('pending',[])) and len(pending)==len(set(pending)),'invalid_pending')
    require(pending==checkpoint.get('pending_normalization',[]),'pending_mirror_mismatch')
    index=manifest.get('records',[])
    require(all(isinstance(x,list) and len(x)==2 and isinstance(x[0],str) and bool(HEX40.fullmatch(str(x[1]))) for x in index),'invalid_record_index')
    keys=[x[0] for x in index]
    require(len(keys)==len(set(keys)),'duplicate_record_index')
    return {'status':'consistent','source':manifest['id'],'done':b1[:2],'next':b1[2:],'pending':pending}

def _gate_authorize(manifest,checkpoint,receipts,start,start_pdf,next_printed,next_pdf):
    from ingestion_gate import authorize_advance
    return authorize_advance(manifest,checkpoint,receipts,start,start_pdf,next_printed,next_pdf)

def authorize(manifest,checkpoint,receipts,pending_id:str,start:int,start_pdf:int,next_printed:int,next_pdf:int,expected_paths:list[str]):
    state(manifest,checkpoint)
    require((next_printed-start)==(next_pdf-start_pdf)>0,'invalid_range')
    require(manifest.get('next')=={'p':start,'pdf':start_pdf},'stale_boundary')
    require(manifest.get('status')=='ingesting','source_not_ingesting')
    pending=[x['id'] for x in manifest.get('pending',[])]
    require(pending==[pending_id] or not pending,'unrelated_pending')
    require(len(set(expected_paths))==len(expected_paths) and expected_paths,'invalid_expected_paths')
    require(isinstance(receipts,list) and len(receipts)==len(expected_paths),'receipt_count_mismatch')
    require(set(x.get('path') for x in receipts)==set(expected_paths),'incomplete_or_extra_receipts')
    coverage=set()
    for r in receipts:
        require(r.get('protocol')=='sr3-gate/v1' and r.get('status')=='verified','unverified_receipt')
        require(r.get('source')==manifest['id'],'receipt_source_mismatch')
        require(r.get('pdf_sha256')==manifest.get('source_pdf_sha256'),'source_pdf_mismatch')
        require(r.get('readback_blob_sha')==r.get('expected_blob_sha') and bool(HEX40.fullmatch(str(r.get('commit_sha','')))),'readback_not_verified')
        p,q=pages(r.get('printed_pages')),pages(r.get('pdf_pages'))
        require(len(p)==len(q) and min(q)-min(p)==start_pdf-start,'receipt_page_mismatch')
        require(p.issubset(set(range(start,next_printed))) and q.issubset(set(range(start_pdf,next_pdf))),'receipt_outside_slice')
        coverage|=p
    require(coverage==set(range(start,next_printed)),'uncovered_pages')
    require(any(int(r[0])<=start and int(r[1])>=next_printed-1 for r in manifest.get('routes',[])),'not_one_route')
    clean_m=copy.deepcopy(manifest);clean_c=copy.deepcopy(checkpoint)
    clean_m['pending']=[];clean_c['pending_normalization']=[]
    try: gate_result=_gate_authorize(clean_m,clean_c,receipts,start,start_pdf,next_printed,next_pdf)
    except Exception as exc: raise RecoveryError('ingestion_gate_authorization_failed') from exc
    require(gate_result.get('authorized') is True,'ingestion_gate_did_not_authorize')
    return {'authorized':True,'protocol':'sr3-recovery/v1','source':manifest['id'],'pending_id':pending_id,'from':[start,start_pdf],'next':[next_printed,next_pdf], 'records':[{k:r[k] for k in ('path','commit_sha','expected_blob_sha')} for r in receipts]}

def classify_failure(operation:str, diagnostic:str, http_status:int|None=None, explicit_restriction:bool=False):
    """Classify observable failures without guessing a hidden safety trigger."""
    require(operation in {'create','update','read','preflight','confirm','manifest','checkpoint'},'invalid_operation')
    message=diagnostic.lower()
    if explicit_restriction:
        category,action='explicit_restriction','stop_preserve_pending'
    elif http_status in {409,412} or (http_status==422 and 'sha' in message):
        category,action='stale_sha','refresh_then_reconcile'
    elif http_status in {401,403}:
        category,action='provider_denial','inspect_permissions_no_alternate_api'
    elif http_status==429 or http_status in {500,502,503,504}:
        category,action='transient_provider_error','readback_then_retry_when_allowed'
    elif 'blocked by openai' in message or 'safety checks' in message:
        category,action='ambiguous_tool_layer_rejection','readback_and_check_permissions'
    elif operation=='preflight':
        category,action='preflight_failure','repair_schema_or_provenance_before_write'
    else:
        category,action='unclassified','inspect_readback_and_evidence'
    return {'category':category,'next_action':action,'github_http_status':http_status,'cause_proved':False}

def _replace_one(text:str,pattern:str,replacement:str):
    result,count=re.subn(pattern,replacement,text,count=1,flags=re.M)
    require(count==1,'state_field_missing')
    return result

def render_manifest(original:str,authorization:dict,record_keys:dict[str,str]):
    m=parse_yaml(original)
    require(authorization.get('authorized') is True and authorization.get('source')==m.get('id'),'authorization_mismatch')
    start,start_pdf=authorization['from'];end,end_pdf=authorization['next']
    require(m.get('next')=={'p':start,'pdf':start_pdf},'stale_manifest')
    req={r['path']:r['commit_sha'] for r in authorization['records']}
    require(set(record_keys)==set(req) and len(set(record_keys.values()))==len(record_keys),'record_key_mismatch')
    index={k:v for k,v in m['records']}
    for path,key in record_keys.items():
        require(key not in index or index[key]==req[path],'record_index_conflict')
    pending_id=authorization['pending_id'];pending=m.get('pending',[])
    require(not pending or len(pending)==1 and pending[0].get('id')==pending_id,'unrelated_pending')
    s=original
    s=_replace_one(s,r'^done:.*$',f'done: {{p: {end-1}, pdf: {end_pdf-1}}}')
    s=_replace_one(s,r'^next:.*$',f'next: {{p: {end}, pdf: {end_pdf}}}')
    if pending:
        # Limit removal to the pending root mapping: verified-forward and
        # deferred-forward evidence may occur before resolved_pending.
        match=re.search(r'^pending:[^\n]*(?:\n|$)',s,flags=re.M)
        require(match is not None,'pending_field_missing')
        next_root=re.search(r'^[A-Za-z_][A-Za-z0-9_]*:',s[match.end():],flags=re.M)
        require(next_root is not None,'pending_end_missing')
        pending_end=match.end()+next_root.start()
        s=s[:match.start()]+'pending: []\n'+s[pending_end:]
    if pending_id not in m.get('resolved_pending',[]):
        if 'resolved_pending: []' in s:
            s=s.replace('resolved_pending: []','resolved_pending:\n  - '+pending_id,1)
        else:
            s=s.replace('resolved_pending:\n','resolved_pending:\n  - '+pending_id+'\n',1)
    new=''.join(f'  - ["{key}", {req[path]}]\n' for path,key in record_keys.items() if key not in index)
    require('source_end:\n' in s,'missing_source_end')
    s=s.replace('source_end:\n',new+'source_end:\n',1)
    parsed=parse_yaml(s)
    require(parsed['done']=={'p':end-1,'pdf':end_pdf-1} and parsed['next']=={'p':end,'pdf':end_pdf},'render_boundary_error')
    require(not parsed.get('pending'),'pending_not_cleared')
    keys=[r[0] for r in parsed['records']];require(len(keys)==len(set(keys)),'duplicate_record_index')
    return s

def render_checkpoint(manifest_after:str,checkpoint_before:str,manifest_commit:str):
    m=parse_yaml(manifest_after);c=parse_yaml(checkpoint_before)
    require(bool(HEX40.fullmatch(manifest_commit)),'missing_manifest_commit')
    require(m.get('id')==c.get('active_source'),'source_mismatch')
    n=m['next'];d=m['done']
    target=f'completed_through: {{printed_page: {d["p"]}, pdf_page: {d["pdf"]}}}'
    out=_replace_one(checkpoint_before,r'^completed_through:.*$',target)
    out=_replace_one(out,r'^resume_at:.*$',f'resume_at: {{printed_page: {n["p"]}, pdf_page: {n["pdf"]}}}')
    pend=[x['id'] for x in m.get('pending',[])]
    pendtxt='pending_normalization: []' if not pend else 'pending_normalization:\n'+''.join('  - '+p+'\n' for p in pend).rstrip('\n')
    out=_replace_one(out,r'^pending_normalization:[\s\S]*?(?=^open_conflicts:)',pendtxt+'\n',)
    out=_replace_one(out,r'^last_commit:.*$','last_commit: '+manifest_commit)
    c2=parse_yaml(out);state(m,c2)
    return out

def cli():
    a=argparse.ArgumentParser(description=__doc__); subs=a.add_subparsers(dest='mode',required=True)
    p=subs.add_parser('stage');p.add_argument('baseline',type=Path);p.add_argument('candidate',type=Path);p.add_argument('path');p.add_argument('source');p.add_argument('pdf_sha');p.add_argument('journal',type=Path)
    p=subs.add_parser('inspect');p.add_argument('journal',type=Path);p.add_argument('--observed-blob');p.add_argument('--commit')
    p=subs.add_parser('audit');p.add_argument('manifest',type=Path);p.add_argument('checkpoint',type=Path)
    p=subs.add_parser('authorize');p.add_argument('manifest',type=Path);p.add_argument('checkpoint',type=Path);p.add_argument('receipts',type=Path);p.add_argument('pending');p.add_argument('start',type=int);p.add_argument('start_pdf',type=int);p.add_argument('next',type=int);p.add_argument('next_pdf',type=int);p.add_argument('paths',nargs='+')
    p=subs.add_parser('manifest-proposal');p.add_argument('manifest',type=Path);p.add_argument('authorization',type=Path);p.add_argument('keys',type=Path);p.add_argument('output',type=Path)
    p=subs.add_parser('checkpoint-proposal');p.add_argument('manifest_after',type=Path);p.add_argument('checkpoint_before',type=Path);p.add_argument('manifest_commit');p.add_argument('output',type=Path)
    args=a.parse_args()
    try:
        if args.mode=='stage': result=stage(args.baseline,args.candidate,args.path,args.source,args.pdf_sha,args.journal)
        elif args.mode=='inspect':result=inspect(args.journal,args.observed_blob,args.commit)
        elif args.mode=='audit':result=state(parse_yaml(args.manifest.read_text()),parse_yaml(args.checkpoint.read_text()))
        elif args.mode=='authorize':result=authorize(parse_yaml(args.manifest.read_text()),parse_yaml(args.checkpoint.read_text()),json.loads(args.receipts.read_text()),args.pending,args.start,args.start_pdf,args.next,args.next_pdf,args.paths)
        elif args.mode=='manifest-proposal':
            args.output.write_text(render_manifest(args.manifest.read_text(),json.loads(args.authorization.read_text()),json.loads(args.keys.read_text())),encoding='utf-8');result={'status':'proposal_created','path':str(args.output)}
        else:
            args.output.write_text(render_checkpoint(args.manifest_after.read_text(),args.checkpoint_before.read_text(),args.manifest_commit),encoding='utf-8');result={'status':'proposal_created','path':str(args.output)}
        print(json.dumps(result,sort_keys=True));return 0
    except (RecoveryError,KeyError,TypeError,ValueError,OSError) as exc:
        print(json.dumps({'status':'blocked','reason':str(exc) if isinstance(exc,RecoveryError) else type(exc).__name__}));return 1
if __name__=='__main__':sys.exit(cli())
