#!/usr/bin/env python3
"""Offline write gate. Requires preflighted bytes and GitHub readback before advancing.

Never claims source accuracy or predicts connector acceptance. There is no network
access and no content rewriting in this module.
"""
import hashlib, json, re, sys
from pathlib import Path
import yaml
from connector_preflight import validate_files, InvalidRecord

HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')

def sha256(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw): return hashlib.sha1(('blob %s\0' % len(raw)).encode()+raw).hexdigest()
def fail(reason): raise InvalidRecord(reason)
def read(path): return yaml.safe_load(Path(path).read_text(encoding='utf-8'))

def prepare(baseline, candidate, path, source, pdf_sha256):
    if not HEX64.fullmatch(pdf_sha256): fail('missing_source_pdf_hash')
    if not re.fullmatch(r'(references|rule|rules|equipment|options|entities|world|procedure|procedures)/[\w./-]+\.yml', path) or '..' in path.split('/'):
        fail('invalid_semantic_path')
    preflight=validate_files(Path(baseline),Path(candidate))
    c=read(candidate)
    if c['source']!=source: fail('source_mismatch')
    raw=Path(candidate).read_bytes()
    return {'protocol':'sr3-gate/v1','status':'preflighted','record_id':c['id'],
            'path':path,'source':source,'printed_pages':c['printed_pages'],
            'pdf_pages':c['pdf_pages'],'pdf_sha256':pdf_sha256,
            'candidate_sha256':sha256(raw),'expected_blob_sha':blob(raw),
            'immutable_sha256':preflight['immutable_sha256']}

def confirm(plan, candidate, commit_sha, readback_blob_sha):
    raw=Path(candidate).read_bytes()
    if plan.get('protocol')!='sr3-gate/v1' or plan.get('status')!='preflighted': fail('missing_preflight')
    if sha256(raw)!=plan['candidate_sha256'] or blob(raw)!=plan['expected_blob_sha']: fail('bytes_changed')
    if not HEX40.fullmatch(commit_sha) or not HEX40.fullmatch(readback_blob_sha):fail('readback_required')
    if readback_blob_sha!=plan['expected_blob_sha']:fail('readback_mismatch')
    return {**plan,'status':'verified','commit_sha':commit_sha,'readback_blob_sha':readback_blob_sha}

def authorize_advance(manifest, checkpoint, verified, expected_start, expected_pdf, next_printed, next_pdf):
    if manifest['id']!=checkpoint['active_source'] or manifest['status']!='ingesting':fail('source_state_mismatch')
    if manifest['done']!={'p':checkpoint['completed_through']['printed_page'],'pdf':checkpoint['completed_through']['pdf_page']}:fail('manifest_checkpoint_disagree')
    if manifest['next']!={'p':expected_start,'pdf':expected_pdf} or checkpoint['resume_at']!={'printed_page':expected_start,'pdf_page':expected_pdf}:fail('stale_boundary')
    if manifest.get('pending') or checkpoint.get('pending_normalization') or checkpoint.get('open_conflicts'):fail('unresolved_pending')
    if next_printed<=expected_start or next_pdf<=expected_pdf or next_printed-expected_start!=next_pdf-expected_pdf:fail('invalid_range')
    if not any(r[0]<=expected_start and r[1]>=next_printed-1 for r in manifest.get('routes',[])):fail('not_one_route')
    if isinstance(verified, dict): verified=[verified]
    if not isinstance(verified, list) or not verified:fail('no_verified_records')
    seen=set()
    for item in verified:
        if item.get('status')!='verified' or item.get('protocol')!='sr3-gate/v1':fail('unverified_record')
        if item.get('source')!=manifest['id'] or item.get('readback_blob_sha')!=item.get('expected_blob_sha'):fail('provenance_mismatch')
        if not HEX40.fullmatch(str(item.get('commit_sha',''))):fail('missing_commit')
        if item['path'] in seen:fail('duplicate_path')
        seen.add(item['path'])
    return {'authorized':True,'source':manifest['id'],'from':[expected_start,expected_pdf],
            'to':[next_printed-1,next_pdf-1], 'records':[{'path':x['path'],'commit':x['commit_sha']} for x in verified]}

def main():
    import argparse
    parser=argparse.ArgumentParser();s=parser.add_subparsers(dest='mode',required=True)
    p=s.add_parser('prepare');p.add_argument('baseline');p.add_argument('candidate');p.add_argument('path');p.add_argument('source');p.add_argument('pdf_sha256')
    p=s.add_parser('confirm');p.add_argument('plan');p.add_argument('candidate');p.add_argument('commit');p.add_argument('readback_blob')
    p=s.add_parser('authorize-advance');p.add_argument('manifest');p.add_argument('checkpoint');p.add_argument('verified_json');p.add_argument('start',type=int);p.add_argument('start_pdf',type=int);p.add_argument('next',type=int);p.add_argument('next_pdf',type=int)
    a=parser.parse_args()
    try:
        if a.mode=='prepare':result=prepare(a.baseline,a.candidate,a.path,a.source,a.pdf_sha256)
        elif a.mode=='confirm':result=confirm(json.loads(Path(a.plan).read_text()),a.candidate,a.commit,a.readback_blob)
        else:result=authorize_advance(read(a.manifest),read(a.checkpoint),json.loads(Path(a.verified_json).read_text()),a.start,a.start_pdf,a.next,a.next_pdf)
    except (InvalidRecord, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({'status':'blocked','reason':str(e) if isinstance(e,InvalidRecord) else type(e).__name__}));return 1
    print(json.dumps(result,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())
