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

def source7116_color_plate_jump(manifest, start, start_pdf, next_printed, next_pdf):
    """Permit only the independently indexed FASA7116 eight-plate interleaf.

    Printed 64 is PDF65; eight unnumbered plates occupy PDF66-73;
    printed 65 resumes at PDF74. This is a source-specific provenance check,
    not a generic exemption from contiguous printed-page receipts.
    """
    if manifest.get('id') != 'source.fasa-7116': return False
    integrity=manifest.get('source_integrity',{})
    mapping=integrity.get('page_mapping','')
    verified=integrity.get('visually_checked_mapping',{})
    if not ('eight_unnumbered_color_plates_at_pdf66-73' in mapping
            and verified.get('printed_64') == 65
            and verified.get('printed_65') == 74
            and verified.get('unnumbered_color_plates_pdf') == [66,73]
            and manifest.get('source_pdf_sha256') == '85656be71abc5583b671cc1613c12c07db77239611a90cbb95f4faa168ec1d30'):
        return False
    if (start,start_pdf) != (64,65) or next_printed not in (65,66) or next_pdf != next_printed+9:
        return False
    ahead=manifest.get('verified_ahead_of_contiguous_boundary',[])
    required={
        ('references/prime-runners/unnumbered-color-plates-visual-index-pdf66-73.yml',(66,73)),
        ('world/prime-runners/unnumbered-color-plates-character-voices-pdf67-73.yml',(67,73)),
    }
    recorded={(x.get('path'),tuple(x.get('range_pdf',[])))
              for x in ahead if x.get('gate')=='verified' and x.get('range_printed')==[]}
    return required.issubset(recorded)

def source7115_color_plate_jump(manifest, start, start_pdf, next_printed, next_pdf):
    """Validate Lone Star's actual eight unnumbered plates after printed p80.

    Printed p80 is PDF80; PDF81-88 are original recruitment-art plates,
    and printed p81 resumes at PDF89. No semantic page is synthesized or
    counted as a printed-page receipt. This exemption is source-hash-bound.
    """
    if manifest.get('id') != 'source.fasa-7115': return False
    integrity=manifest.get('source_integrity',{})
    mapping=integrity.get('page_mapping','')
    verified=integrity.get('visually_checked_mapping',{})
    if (manifest.get('source_pdf_sha256') != 'c24e67bec3b2e2659236f96cfa334f06cde95ad4f76958e09943379060e69c28'
        or 'eight_unnumbered_color_plates_pdf81-88' not in mapping
        or verified.get('printed_80') != 80
        or verified.get('printed_81') != 89
        or integrity.get('color_plates_pdf_pages') != [81,88]):
        return False
    if (not 5 <= start <= 80 or start_pdf != start
        or (next_printed,next_pdf) != (81,89)):
        return False
    return any(
        item.get('path') == 'references/lone-star/unnumbered-recruitment-color-plates-pdf81-88.yml'
        and item.get('range_printed') == []
        and item.get('range_pdf') == [81,88]
        and item.get('gate') == 'verified'
        and bool(HEX40.fullmatch(str(item.get('commit',''))))
        and bool(HEX40.fullmatch(str(item.get('blob',''))))
        for item in manifest.get('verified_ahead_of_contiguous_boundary',[]))

def authorize_advance(manifest, checkpoint, verified, expected_start, expected_pdf, next_printed, next_pdf):
    if manifest['id']!=checkpoint['active_source'] or manifest['status']!='ingesting':fail('source_state_mismatch')
    if manifest['done']!={'p':checkpoint['completed_through']['printed_page'],'pdf':checkpoint['completed_through']['pdf_page']}:fail('manifest_checkpoint_disagree')
    if manifest['next']!={'p':expected_start,'pdf':expected_pdf} or checkpoint['resume_at']!={'printed_page':expected_start,'pdf_page':expected_pdf}:fail('stale_boundary')
    if manifest.get('pending') or checkpoint.get('pending_normalization') or checkpoint.get('open_conflicts'):fail('unresolved_pending')
    crosses_plates=manifest['id']=='source.fasa-7116' and expected_start<=64<next_printed
    prime_plate_jump=source7116_color_plate_jump(manifest,expected_start,expected_pdf,next_printed,next_pdf)
    lone_plate_jump=source7115_color_plate_jump(manifest,expected_start,expected_pdf,next_printed,next_pdf)
    plate_jump=prime_plate_jump or lone_plate_jump
    crosses_lone_plates=manifest['id']=='source.fasa-7115' and expected_start<=80<next_printed
    if crosses_lone_plates and not lone_plate_jump:fail('unverified_lone_star_color_plate_boundary')
    if crosses_plates and not prime_plate_jump:fail('unverified_color_plate_boundary')
    if next_printed<=expected_start or next_pdf<=expected_pdf or (not plate_jump and next_printed-expected_start!=next_pdf-expected_pdf):fail('invalid_range')
    if not any(r[0]<=expected_start and r[1]>=next_printed-1 for r in manifest.get('routes',[])):fail('not_one_route')
    if isinstance(verified, dict): verified=[verified]
    if not isinstance(verified, list) or not verified:fail('no_verified_records')
    seen=set()
    covered=set()
    for item in verified:
        if item.get('status')!='verified' or item.get('protocol')!='sr3-gate/v1':fail('unverified_record')
        if item.get('source')!=manifest['id'] or item.get('readback_blob_sha')!=item.get('expected_blob_sha'):fail('provenance_mismatch')
        if not HEX40.fullmatch(str(item.get('commit_sha',''))):fail('missing_commit')
        p=item.get('printed_pages','')
        q=item.get('pdf_pages','')
        def range_pair(x):
            m=re.fullmatch(r'([0-9]+)(?:-([0-9]+))?',str(x))
            if not m:fail('invalid_record_range')
            return int(m.group(1)),int(m.group(2) or m.group(1))
        first,last=range_pair(p)
        pdf_first,pdf_last=range_pair(q)
        if not (first<=last<next_printed and pdf_first<=pdf_last<next_pdf and last-first==pdf_last-pdf_first):fail('record_outside_slice')
        if not plate_jump and first-expected_start != pdf_first-expected_pdf:fail('record_page_mapping_mismatch')
        if first<expected_start or pdf_first<expected_pdf:
            # A verified source record can begin on the last already-authorized page
            # and finish in the new slice. Retain its full printed/PDF provenance;
            # never re-label its pages or make a synthetic receipt for the suffix.
            if (plate_jump or first>=expected_start or pdf_first>=expected_pdf
                or last<expected_start or pdf_last<expected_pdf
                or manifest.get('done',{}).get('p')!=expected_start-1
                or manifest.get('done',{}).get('pdf')!=expected_pdf-1):
                fail('untrusted_prior_page_overlap')
            matched=any(
                entry.get('gate')=='verified'
                and entry.get('path')==item['path']
                and entry.get('commit')==item['commit_sha']
                and entry.get('blob')==item['readback_blob_sha']
                and entry.get('range_printed')==[first,last]
                and entry.get('range_pdf')==[pdf_first,pdf_last]
                for entry in manifest.get('verified_ahead_of_contiguous_boundary',[])
            )
            if not matched:fail('overlap_requires_exact_verified_forward_entry')
        covered.update(range(max(expected_start,first),last+1))
        if prime_plate_jump:
            if first<=64<last:fail('plate_crossing_record_requires_separate_pagination')
            offset=1 if last<=64 else 9
            if pdf_first!=first+offset or pdf_last!=last+offset:fail('plate_receipt_mapping_mismatch')
        if lone_plate_jump:
            if last>80 or pdf_first!=first or pdf_last!=last:fail('lone_star_plate_receipt_mapping_mismatch')
        if item['path'] in seen:fail('duplicate_path')
        seen.add(item['path'])
    if covered!=set(range(expected_start,next_printed)):fail('uncovered_pages')
    last_pdf=80 if lone_plate_jump else next_pdf-1
    return {'authorized':True,'source':manifest['id'],'from':[expected_start,expected_pdf],
            'to':[next_printed-1,last_pdf], 'records':[{'path':x['path'],'commit':x['commit_sha']} for x in verified]}

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
