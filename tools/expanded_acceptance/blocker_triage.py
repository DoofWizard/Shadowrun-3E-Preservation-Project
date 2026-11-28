#!/usr/bin/env python3
"""Read-only, all-at-once prerequisite triage for expanded SR3 acceptance.

This is NOT an acceptance gate, historical receipt issuer, original-image
review, or authorization to change source/edition/Denver status. Its results
are leads to be checked by the independent validator and source reviewers.
"""
import argparse
import base64
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from binding_schema import substantive_pointer

PROTOCOL = 'sr3-expanded-acceptance/v1'
HEX64 = re.compile(r'[a-f0-9]{64}\Z')
SPLIT = 'split_archive/v1'
CLASSES = {'rule_exact', 'rule_procedure', 'equipment_stat', 'character_option', 'campaign_guidance'}
KINDS = {'rule', 'row', 'condition', 'exception', 'example', 'procedure'}
LINEAGES = {'sr3_effective', 'sr3_optional', 'sr2_unsuperseded', 'sr2_superseded', 'preserved_variant'}


def unique_pairs(items):
    value = {}
    for key, entry in items:
        if not isinstance(key, str) or key in value:
            raise ValueError('duplicate_or_invalid_json_key')
        value[key] = entry
    return value


def load_pinned(path, expected_sha):
    raw = Path(path).read_bytes()
    if not HEX64.fullmatch(expected_sha) or hashlib.sha256(raw).hexdigest() != expected_sha:
        raise ValueError('independent_input_pin_mismatch:' + str(path))
    return json.loads(raw, object_pairs_hook=unique_pairs)


def scan(review, bindings, evidence):
    errors = []
    def add(category, subject, code):
        item = {'category': category, 'subject': str(subject), 'code': code}
        if item not in errors:
            errors.append(item)
    if not isinstance(review, dict) or review.get('protocol') != PROTOCOL:
        add('inventory', 'source', 'original_derived_review_inventory_missing_or_wrong_protocol')
        review = review if isinstance(review, dict) else {}
    if not isinstance(bindings, dict):
        add('binding', 'source', 'field_bindings_missing'); bindings = {}
    if not isinstance(evidence, dict) or evidence.get('protocol') != PROTOCOL:
        add('receipt', 'source', 'historical_evidence_bundle_missing_or_wrong_protocol')
        evidence = evidence if isinstance(evidence, dict) else {}
    if not review.get('reviewer') or not evidence.get('custodian') or review.get('reviewer') == evidence.get('custodian'):
        add('independence', 'source', 'independent_reviewer_and_custodian_required')
    source = review.get('source', {})
    if not isinstance(source, dict) or not all(source.get(k) for k in ('id','sha256','manifest','catalog','publisher','edition','physical_pages')):
        add('source', 'source', 'original_source_identity_or_pdf_pin_missing')
        source = source if isinstance(source, dict) else {}
    if source.get('edition') not in ('SR2','SR3') or not isinstance(source.get('sha256'),str) or not HEX64.fullmatch(source['sha256']):
        add('source', 'source', 'invalid_source_edition_or_pdf_hash')
    unresolved = review.get('unresolved_fields', None)
    if unresolved is None:
        add('inventory', 'source', 'explicit_unresolved_field_list_missing')
    elif unresolved:
        for item in unresolved:
            add('original_rule', str(item), 'unresolved_original_field')
    fields = {}
    field_pages = {}
    pages = review.get('pages', None)
    if not isinstance(pages, list) or not pages:
        add('inventory', 'source', 'finite_original_page_inventory_missing')
        pages = []
    expected_count = source.get('physical_pages')
    observed = [p.get('pdf') for p in pages if isinstance(p, dict)]
    if type(expected_count) is not int or observed != list(range(1, expected_count+1)):
        add('inventory', 'source', 'physical_page_coverage_unproven')
    printed = set()
    if not isinstance(review.get('unrepresented_printed'), list):
        add('inventory', 'source', 'unrepresented_printed_folios_list_missing')
    unrepresented = set()
    for item in review.get('unrepresented_printed', []):
        if not isinstance(item, dict) or type(item.get('printed')) is not int or not item.get('reason') or not item.get('authority') or item.get('no_page_credit') is not True or item.get('disposition') not in ('accepted_scan_omission','original_folio_not_present'):
            add('inventory', 'unrepresented', 'unverified_or_unauthorized_printed_gap')
            continue
        if item['printed'] in unrepresented:
            add('inventory', item['printed'], 'duplicate_unrepresented_printed_folio')
        unrepresented.add(item['printed'])
    for page in pages:
        if not isinstance(page, dict):
            add('inventory', 'page', 'invalid_page_entry'); continue
        n = page.get('pdf')
        if not page.get('image_review') or not page.get('heading'):
            add('original_review', 'PDF '+str(n), 'original_page_image_heading_review_missing')
        folio = page.get('printed')
        if folio is not None:
            if type(folio) is not int or folio <= 0 or folio in printed:
                add('inventory', 'PDF '+str(n), 'duplicate_or_invalid_printed_folio')
            printed.add(folio)
        ff = page.get('fields')
        if not isinstance(ff, list):
            add('inventory', 'PDF '+str(n), 'original_field_inventory_missing'); continue
        if page.get('disposition') == 'mechanical' and not ff:
            add('inventory', 'PDF '+str(n), 'mechanical_page_has_no_original_derived_fields')
        if page.get('disposition') not in ('mechanical','zero_rules','owner_omission'):
            add('inventory', 'PDF '+str(n), 'unclassified_original_page')
        elif page['disposition'] != 'mechanical':
            if ff or not page.get('reason'):
                add('inventory', 'PDF '+str(n), 'no_rule_page_not_justified')
            if page['disposition'] == 'owner_omission' and (not page.get('owner_authority') or page.get('no_page_credit') is not True):
                add('inventory', 'PDF '+str(n), 'omission_lacks_owner_authority')
        for f in ff:
            if not isinstance(f, dict) or not isinstance(f.get('id'), str) or not f['id']:
                add('inventory', 'PDF '+str(n), 'invalid_rule_field'); continue
            fid = f['id']
            if fid in fields:
                add('inventory', fid, 'duplicate_original_rule_obligation')
            fields[fid] = f
            field_pages[fid] = page
            if not f.get('heading') or f.get('lineage') not in LINEAGES or f.get('class') not in CLASSES or f.get('kind') not in KINDS or f.get('value') in (None,'',[],{}):
                add('original_rule', fid, 'incomplete_field_or_lineage')
            if f.get('lineage', '').startswith('sr2') and (not f.get('precedence_review') or (f['lineage']=='sr2_superseded' and not f.get('named_successor'))):
                add('equivalence', fid, 'sr2_precedence_or_named_successor_unresolved')
            if (source.get('edition') == 'SR2' and f.get('lineage', '').startswith('sr3')) or (source.get('edition') == 'SR3' and f.get('lineage', '').startswith('sr2')):
                add('equivalence', fid, 'field_lineage_mismatches_original_edition')
    expected = review.get('expected_printed_folios')
    if not isinstance(expected,list) or expected != sorted(printed | unrepresented) or printed & unrepresented:
        add('inventory', 'source', 'expected_printed_folios_not_reconciled')
    contradictions = review.get('contradictions')
    if not isinstance(contradictions,list):
        add('equivalence', 'source', 'explicit_contradiction_inventory_missing')
    else:
        listed = set()
        for conflict in contradictions:
            ids = conflict.get('fields',[]) if isinstance(conflict,dict) else []
            if not isinstance(ids,list) or len(set(ids)) < 2 or not set(ids).issubset(fields) or not isinstance(conflict,dict) or conflict.get('disposition') != 'preserve_distinct_variants' or not conflict.get('reason'):
                add('equivalence', str(ids), 'unreviewed_or_collapsed_contradiction')
            else:
                listed.update(ids)
        if listed != {k for k,v in fields.items() if v.get('lineage')=='preserved_variant'}:
            add('equivalence', 'source', 'unmapped_preserved_variant')
    for f in sorted(set(fields) - set(bindings)):
        add('binding', f, 'original_rule_has_no_canonical_binding')
    for f in sorted(set(bindings) - set(fields)):
        add('binding', f, 'binding_not_justified_by_original_source')
    transactions = evidence.get('transactions')
    if not isinstance(transactions, dict):
        add('receipt', 'source', 'transaction_inventory_missing'); transactions = {}
    for fid in sorted(set(fields) & set(bindings)):
        b = bindings[fid]
        if not isinstance(b, dict):
            add('binding', fid, 'invalid_canonical_binding'); continue
        path, pointer = b.get('path'), b.get('pointer')
        if not substantive_pointer(b, fields[fid], source, field_pages[fid]):
            add('binding', fid, 'substantive_canonical_path_and_pointer_required'); continue
        mode = b.get('mode', 'source_local')
        if mode == 'sr3-accepted-core-equivalence/v1':
            core = evidence.get('accepted_core_equivalence')
            if not isinstance(core, dict) or core.get('protocol') != mode or not core.get('receipt_commit') or not core.get('receipt_blob'):
                add('equivalence', fid, 'accepted_core_receipt_proof_missing')
            if not b.get('core_obligation'):
                add('equivalence', fid, 'accepted_core_obligation_missing')
            if not isinstance(core, dict) or not isinstance(core.get('comparisons'), dict) or fid not in core['comparisons']:
                add('equivalence', fid, 'independent_original_page_comparison_missing')
            # A core reference uses the actual accepted FASA7001 receipt, not
            # an invented historical Companion transaction. The independent
            # expanded validator must verify this evidence at pinned Git HEAD.
            continue
        if mode != 'source_local':
            add('equivalence', fid, 'external_equivalence_requires_own_reviewed_lineage_and_accepted_target_proof')
            continue
        if path not in transactions:
            add('receipt', path, 'no_accepted_transaction_evidence'); continue
        t = transactions[path]
        if not isinstance(t, dict):
            add('receipt', path, 'invalid_transaction_evidence'); continue
        layout = t.get('layout')
        if layout == SPLIT:
            for k in ('pre_base64','post_base64','pre_sha256','post_sha256','attestation_base64','attestation_sha256'):
                if not t.get(k):
                    add('receipt', path, 'missing_split_archive_' + k)
            for k, digest in (('pre_base64','pre_sha256'),('post_base64','post_sha256'),('attestation_base64','attestation_sha256')):
                if t.get(k) and t.get(digest):
                    try:
                        data = base64.b64decode(t[k], validate=True)
                        if hashlib.sha256(data).hexdigest() != t[digest]:
                            add('receipt', path, 'split_archive_pin_mismatch_' + k)
                    except (ValueError, TypeError):
                        add('receipt', path, 'split_archive_bytes_invalid_' + k)
        elif layout is None:
            for k in ('plan','confirm','baseline_sha256','prewrite_journal_artifact','historical_confirm_artifact','editorial_review_artifact','historical_index_receipt_artifact','historical_index_snapshot_artifact','index_commit','index_pointer'):
                if not t.get(k):
                    add('receipt', path, 'missing_historical_' + k)
            journal = t.get('prewrite_journal_artifact', {})
            for k in ('baseline','candidate','plan'):
                if not isinstance(journal, dict) or not journal.get(k):
                    add('receipt', path, 'missing_original_prewrite_' + k)
        else:
            add('receipt', path, 'unsupported_historical_archive_layout')
    for path in sorted(set(transactions) - {b.get('path') for b in bindings.values() if isinstance(b, dict)}):
        add('receipt', path, 'orphan_transaction_not_bound_to_original_field')
    counts = dict(sorted(Counter(e['category'] for e in errors).items()))
    return {'protocol': 'sr3-expanded-prerequisite-triage/v1', 'status': 'TRIAGE_ONLY',
            'candidate_acceptance': False, 'formal_acceptance': False,
            'original_fields_seen': len(fields), 'paths_referenced': len({b.get('path') for b in bindings.values() if isinstance(b, dict) and b.get('path')}),
            'blocker_counts': counts, 'blockers': errors, 'next_gate': 'independent expanded_acceptance/validator.py and original editorial review'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for n in ('review','bindings','evidence'):
        ap.add_argument('--' + n, required=True)
        ap.add_argument('--' + n + '-sha', required=True)
    args = ap.parse_args()
    try:
        result = scan(*(load_pinned(getattr(args, n),getattr(args,n+'_sha')) for n in ('review','bindings','evidence')))
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'status':'TRIAGE_INPUT_BLOCKED','reason':str(exc),'formal_acceptance':False},sort_keys=True))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
