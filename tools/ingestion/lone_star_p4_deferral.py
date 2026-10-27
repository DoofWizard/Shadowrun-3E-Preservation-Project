#!/usr/bin/env python3
"""Strict, source-specific authorization of the owner's deferred missing printed p4.

This does not extract a page, claim it is blank, forge a semantic receipt, change an
ordinary record gate, or allow a source-complete assertion. One auditable exception
moves only the *resume cursor* from printed p4/PDF5 to printed p5/PDF5 while
completed-through stays printed p3/PDF4. Subsequent pages use ordinary gates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import yaml

SOURCE = 'source.fasa-7115'
PDF_SHA = 'c24e67bec3b2e2659236f96cfa334f06cde95ad4f76958e09943379060e69c28'
GAP = 'source7115.missing-printed-p4'
TOC = 'Welcome to Shadowland'
MARKER = 'source_specific_user_authorized_unverified_p4_resumption_2026_10_27'

class GateError(ValueError):
    pass

def require(value, code):
    if not value:
        raise GateError(code)

def parse(raw):
    data = yaml.safe_load(raw)
    require(isinstance(data, dict), 'invalid_yaml_mapping')
    return data

def check_original(manifest, checkpoint, observed_sha):
    require(observed_sha == PDF_SHA, 'fresh_original_pdf_hash_mismatch')
    require(manifest.get('id') == SOURCE and manifest.get('catalog_number') == 'FASA7115', 'wrong_source')
    require(manifest.get('source_pdf_sha256') == PDF_SHA and manifest.get('source_pdf_page_count') == 145, 'wrong_source_copy')
    require(manifest.get('status') == 'ingesting' and checkpoint.get('active_source') == SOURCE, 'source_state_mismatch')
    require(manifest.get('done') == {'p': 3, 'pdf': 4} and manifest.get('next') == {'p': 4, 'pdf': 5}, 'wrong_initial_boundary')
    require(checkpoint.get('completed_through') == {'printed_page': 3, 'pdf_page': 4} and checkpoint.get('resume_at') == {'printed_page': 4, 'pdf_page': 5}, 'checkpoint_mismatch')
    require(not manifest.get('pending') and not checkpoint.get('pending_normalization') and not checkpoint.get('open_conflicts'), 'unresolved_pending')
    require([4, 4, 'missing_original_page_hold'] in manifest.get('routes', []) and [5, 8, 'orientation'] in manifest.get('routes', []), 'route_mismatch')
    integrity = manifest.get('source_integrity', {})
    require('printed_p4_absent' in integrity.get('page_mapping', ''), 'page_mapping_mismatch')
    require(integrity.get('visually_checked_mapping', {}).get('printed_5') == 5, 'wrong_successor_pdf_page')
    gaps = integrity.get('unresolved_source_copy_gaps', [])
    require(isinstance(gaps,list) and len([g for g in gaps if isinstance(g,dict) and g.get('id')==GAP]) == 1, 'gap_evidence_missing')
    gap = next(g for g in gaps if g.get('id')==GAP)
    require(gap.get('printed_page') == 4 and gap.get('toc_heading') == TOC, 'toc_evidence_missing')
    require(gap.get('disposition') == 'project_level_exception_user_approved_2026_10_27', 'user_approval_missing')
    require(gap.get('user_instruction') == 'skip_this_one_printed_page_manual_verification_later', 'user_instruction_missing')
    require(gap.get('manually_verified') is False and gap.get('presumed_blank') is False, 'unverified_page_state_mismatch')
    require(gap.get('authorizes_synthetic_semantic_record') is False and gap.get('authorizes_unaudited_page_advance') is False, 'missing_scope_limit')
    require('toc_names_Welcome_to_Shadowland_at_printed_p4' in gap.get('evidence_retained',''), 'contradictory_evidence_missing')
    require('deferred_page_authorization' not in integrity, 'already_authorized_or_conflicting')
    return {'status':'approved_one_page_source_copy_deferral', 'source': SOURCE, 'observed_pdf_sha256': observed_sha,
            'deferred_printed_page': 4, 'physical_pdf_page': None,
            'old_done': {'p': 3, 'pdf': 4}, 'old_next': {'p': 4, 'pdf': 5},
            'new_done': {'p': 3, 'pdf': 4}, 'new_next': {'p': 5, 'pdf': 5},
            'source_page_verified': False, 'page_authorizations': 0,
            'source_completion_permitted': False, 'manual_verification_required': True,
            'source_integrity_marker': MARKER}

def proposed_manifest(original, receipt):
    require(receipt.get('status') == 'approved_one_page_source_copy_deferral' and receipt.get('source_integrity_marker') == MARKER, 'invalid_receipt')
    require(original.count('next: {p: 4, pdf: 5}')==1, 'nonunique_boundary')
    edited=original.replace('next: {p: 4, pdf: 5}', 'next: {p: 5, pdf: 5}', 1)
    anchor='  next_unscanned_forward: {printed_page: 137, pdf_page: 146}'
    require(edited.count(anchor)==1, 'integrity_anchor_missing')
    proof=('  deferred_page_authorization:\n'
           f'    marker: {MARKER}\n'
           '    printed_page: 4\n'
           '    physical_pdf_page: null\n'
           '    status: user_approved_unverified_source_copy_deferral\n'
           '    scope: resume_after_p4_only_not_a_semantic_page_receipt\n'
           '    manual_verification_required: true\n'
           '    source_completion_blocked: true\n'
           f'    original_source_pdf_sha256: {PDF_SHA}\n')
    edited=edited.replace(anchor,proof+anchor,1)
    before=parse(original);after=parse(edited)
    require(after['done']==before['done'] and after['next']=={'p':5,'pdf':5}, 'boundary_change_failed')
    require(after['source_integrity']['unresolved_source_copy_gaps']==before['source_integrity']['unresolved_source_copy_gaps'], 'gap_evidence_mutated')
    require(after['verified_ahead_of_contiguous_boundary']==before['verified_ahead_of_contiguous_boundary'] and after['records']==before['records'], 'semantic_index_mutated')
    for key in set(before) - {'next','source_integrity'}:
        require(before[key]==after[key], 'other_manifest_field_mutated')
    for key in set(before['source_integrity']):
        require(before['source_integrity'][key]==after['source_integrity'][key], 'other_integrity_field_mutated')
    return edited

def check_active(manifest, checkpoint):
    integrity=manifest.get('source_integrity', {})
    mark=integrity.get('deferred_page_authorization', {})
    require(manifest.get('id')==SOURCE and manifest.get('source_pdf_sha256')==PDF_SHA, 'wrong_source')
    require(mark.get('marker')==MARKER and mark.get('printed_page')==4 and mark.get('physical_pdf_page') is None, 'deferral_marker_missing')
    require(mark.get('source_completion_blocked') is True and mark.get('manual_verification_required') is True, 'scope_corrupted')
    require(manifest.get('status') == 'ingesting', 'source_completion_requires_manual_review')
    require(manifest.get('next')=={'p':checkpoint['resume_at']['printed_page'],'pdf':checkpoint['resume_at']['pdf_page']},'checkpoint_mismatch')
    require(manifest.get('done')=={'p':checkpoint['completed_through']['printed_page'],'pdf':checkpoint['completed_through']['pdf_page']},'checkpoint_mismatch')
    require(manifest['next']['p']>=5,'invalid_resume_after_deferral')
    gap=next((g for g in integrity.get('unresolved_source_copy_gaps',[]) if g.get('id')==GAP),None)
    require(gap and gap.get('manually_verified') is False and gap.get('presumed_blank') is False,'gap_evidence_missing')
    return {'status':'valid_source_specific_unverified_deferral','id':GAP,'done':manifest['done'],'next':manifest['next'],'source_completion_allowed':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['authorize','verify-active'])
    p.add_argument('manifest',type=Path);p.add_argument('checkpoint',type=Path)
    p.add_argument('--fresh-pdf',type=Path);p.add_argument('--output-manifest',type=Path)
    a=p.parse_args()
    try:
        m_text=a.manifest.read_text(encoding='utf-8');m=parse(m_text);c=parse(a.checkpoint.read_text(encoding='utf-8'))
        if a.mode=='authorize':
            require(a.fresh_pdf is not None and a.output_manifest is not None, 'fresh_source_and_output_required')
            observed=hashlib.sha256(a.fresh_pdf.read_bytes()).hexdigest()
            receipt=check_original(m,c,observed)
            proposed=proposed_manifest(m_text,receipt)
            a.output_manifest.write_text(proposed,encoding='utf-8')
        else:receipt=check_active(m,c)
        print(json.dumps(receipt,sort_keys=True));return 0
    except (GateError,KeyError,OSError,ValueError,yaml.YAMLError) as exc:
        print(json.dumps({'status':'blocked','reason':str(exc) if isinstance(exc,GateError) else type(exc).__name__}));return 1
if __name__=='__main__':sys.exit(main())
