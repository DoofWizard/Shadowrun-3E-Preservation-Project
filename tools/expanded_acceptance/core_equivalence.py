"""Fail-closed reuse of a formally accepted SR3 core field by another SR3 source.

This read-only adapter certifies neither the original source, a historical
transaction nor the whole supplement. It accepts exact restatements, plus narrowly audited index-only action
references whose full core conditions must remain controlling, backed by the
FASA7001 acceptance receipt and independent original-page comparison.
It never rewrites source rules, source order or edition precedence.
"""
import hashlib
import json
import re
import yaml

PROTOCOL = 'sr3-accepted-core-equivalence/v1'
CORE_SOURCE = 'source.sr3-core'
CORE_RECEIPT = 'references/audits/fasa7001-available-source-mechanical-core-acceptance-confirmed-2026-11-21.json'
CORE_MANIFEST = 'sources/manifests/SR3.yml'
CORE_QUEUE = 'docs/engine-readiness/FASA7001_CORE_RULES_CLOSURE_QUEUE_2026-11-11.yml'
CORE_SHA = '7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')


class Blocked(ValueError):
    pass


def check(condition, code):
    if not condition:
        raise Blocked(code)


def git_blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\x00' + raw).hexdigest()


def typed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False)


def ptr(obj, pointer):
    check(isinstance(pointer, str) and pointer.startswith('/data/'), 'substantive_pointer_required')
    for token in pointer[1:].split('/'):
        check(re.search(r'~(?![01])', token) is None, 'bad_pointer_escape')
        key = token.replace('~1', '/').replace('~0', '~')
        if isinstance(obj, list):
            check(re.fullmatch(r'0|[1-9][0-9]*', key) is not None, 'bad_pointer_index')
            obj = obj[int(key)]
        else:
            obj = obj[key]
    return obj


def safe_load(raw):
    return yaml.safe_load(raw)


def verify(git, source, original_field, original_page, binding,
           proof, reviewer, custodian):
    """Verify an SR3 original field against the already accepted core snapshot.

    *git* must provide read(path, commit=None), changed(path, commit) and
    ancestor(commit, head), with head being the independently pinned live HEAD.
    Caller already verified original page/field inventory and its original PDF.
    """
    check(source['edition'] == 'SR3' and source['id'] != CORE_SOURCE,
          'only_distinct_sr3_sources_can_restate_core')
    check(original_field['lineage'] in ('sr3_effective', 'sr3_optional'),
          'historical_and_conflicting_rules_not_automatically_equivalent')
    check(binding.get('mode') == PROTOCOL, 'explicit_core_equivalence_mode_required')
    check(proof and proof.get('protocol') == PROTOCOL, 'separate_accepted_core_proof_required')
    check(proof.get('core_source_id') == CORE_SOURCE and
          proof.get('original_pdf_sha256') == CORE_SHA, 'core_source_identity_missing')
    commit = proof.get('receipt_commit')
    check(isinstance(commit, str) and HEX40.fullmatch(commit), 'verified_core_receipt_commit_required')
    git.changed(CORE_RECEIPT, commit)
    git.ancestor(commit, git.head)
    receipt_raw = git.read(CORE_RECEIPT, commit)
    check(git_blob(receipt_raw) == proof.get('receipt_blob'), 'core_receipt_blob_mismatch')
    receipt = json.loads(receipt_raw)
    a = receipt['assessment']
    check(receipt['status'] == 'verified_core_acceptance' and
          a['status'] == 'acceptance_evidence_validated' and
          receipt['source'] == CORE_SOURCE and
          a['source_pdf_sha256'] == CORE_SHA and
          a['authorized_printed_pages'] == 0,
          'not_an_accepted_core_receipt')
    manifest_raw = git.read(CORE_MANIFEST, commit)
    queue_raw = git.read(CORE_QUEUE, commit)
    check(git_blob(manifest_raw) == a['manifest_blob'] and
          git_blob(queue_raw) == a['closure_queue_blob'],
          'accepted_core_snapshot_mismatch')
    manifest, queue = safe_load(manifest_raw), safe_load(queue_raw)
    check(manifest['id'] == CORE_SOURCE and
          manifest['source_pdf_sha256'] == CORE_SHA and
          queue['core_acceptance_inventory']['source'] == CORE_SOURCE,
          'original_core_manifest_or_queue_identity_mismatch')
    accepted = queue['core_acceptance_inventory']
    check(accepted['independently_reviewed_original_headings_fields_and_classes'] is True and
          accepted['unresolved_mechanical_fields'] == [],
          'core_inventory_not_source_reviewed')
    obligation = binding.get('core_obligation')
    check(isinstance(obligation, str) and obligation in accepted['bindings'],
          'unaccepted_core_obligation')
    ob = accepted['bindings'][obligation]
    core_id, pointer = ob['record_id'], ob['record_pointer']
    selected_pointer = binding['pointer']
    nested = selected_pointer != pointer
    if nested:
        check(selected_pointer.startswith(pointer + '/'), 'accepted_core_pointer_mismatch')
    path = binding['path']
    check(re.fullmatch(r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*', path) and
          '..' not in path.split('/'), 'invalid_core_record_path')
    raw = git.read(path, commit)
    check(git.read(path) == raw, 'accepted_core_target_modified_after_acceptance')
    rec = safe_load(raw)
    check(rec['id'] == core_id and rec['source'] == CORE_SOURCE and
          rec['content_class'] == [original_field['class']],
          'core_record_identity_or_class_mismatch')
    regs = manifest['postscan_verified_mechanics_recovery']['verified_semantic_records']
    matching = [entry for entry in regs if entry.get('id') == core_id and
                entry.get('path') == path and entry.get('blob') == git_blob(raw) and
                entry.get('gate') == 'verified']
    check(len(matching) == 1, 'core_record_not_uniquely_indexed_in_accepted_snapshot')
    check(typed(ptr(rec, selected_pointer)) == typed(original_field['value']),
          'original_and_core_typed_values_differ')
    comparison = proof.get('comparisons', {}).get(original_field['id'])
    check(isinstance(comparison, dict), 'independent_equivalence_comparison_missing')
    check(comparison.get('source_field_id') == original_field['id'] and
          comparison.get('core_obligation') == obligation and
          comparison.get('source_id') == source['id'] and
          comparison.get('source_sha256') == source['sha256'] and
          comparison.get('core_source_sha256') == CORE_SHA and
          comparison.get('source_printed') == original_page['printed'] and
          comparison.get('source_pdf') == original_page['pdf'] and
          comparison.get('original_heading') == original_field['heading'] and
          comparison.get('lineage') == original_field['lineage'],
          'comparison_source_or_field_binding_mismatch')
    relation = comparison.get('relation')
    if relation == 'indexed_action_reference':
        # FASA7905a p130 is a consolidated ACTION INDEX, explicitly referring
        # readers to SR3 and other books for the rules. It is NOT an alternate
        # detailed procedure. For these three independently reviewed entries,
        # the p105 SR3 qualifying conditions remain fully operative.
        action = original_field['value']
        check(source['id'] == 'source.srcomp' and
              source['sha256'] == '8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5' and
              original_page['printed'] == 130 and original_page['pdf'] == 131,
              'not_the_reviewed_companion_action_index')
        check(original_field.get('kind') == 'row' and
              original_field['lineage'] == 'sr3_effective' and nested and
              selected_pointer.startswith('/data/selected_free_actions/') and
              selected_pointer.endswith('/action') and
              pointer == '/data/selected_free_actions',
              'not_an_accepted_core_free_action_label')
        check(action in ('Activate Cyberware', 'Observe', 'Speak a Word') and
              comparison.get('indexed_action_class') == 'Free' and
              comparison.get('indexed_action_group') == 'General' and
              comparison.get('appendix_is_reference_only') is True and
              comparison.get('no_new_or_conflicting_rules_on_appendix_page') is True and
              comparison.get('preserve_core_conditions_without_weakening') is True,
              'index_reference_scope_or_action_discrepancy')
        check(comparison.get('rule_scope') == 'core_procedure_controls' and
              comparison.get('conditions') == 'core_conditions_preserved' and
              comparison.get('exceptions') == 'core_exceptions_preserved' and
              comparison.get('optional_status') == 'core_status_preserved',
              'index_reference_attempts_to_override_core_rule')
        # Do not merely match the headline: bind the full accepted condition
        # for the original source's action entry, so it cannot be discarded by
        # an index label during game-rule generation.
        core_condition_pointer = selected_pointer[:-len('/action')] + '/condition'
        condition = ptr(rec, core_condition_pointer)
        check(isinstance(condition, str) and condition.strip() and
              comparison.get('full_core_condition') == condition and
              comparison.get('core_condition_pointer') == core_condition_pointer,
              'full_core_action_condition_not_preserved')
        result_status = 'CORE_ACTION_INDEX_REFERENCE_CANDIDATE'
    else:
        check(relation == 'exact_restatement' and
              all(comparison.get(k) == 'identical' for k in
                  ('rule_scope','conditions','exceptions','units','optional_status')),
              'conditional_or_partial_equivalence_not_proven')
        result_status = 'CORE_FIELD_MATCH_CANDIDATE'
    if nested:
        check(comparison.get('accepted_core_group_pointer') == pointer and
              comparison.get('reviewed_subfield_pointer') == selected_pointer and
              isinstance(comparison.get('core_group_original_review'), str) and
              comparison['core_group_original_review'].strip(),
              'accepted_group_descendant_not_independently_reviewed')
    check(isinstance(comparison.get('reviewer'), str) and
          comparison['reviewer'].strip() and
          comparison['reviewer'] not in (reviewer, custodian) and
          isinstance(comparison.get('source_image_review'), str) and
          comparison['source_image_review'].strip() and
          isinstance(comparison.get('core_image_review'), str) and
          comparison['core_image_review'].strip(),
          'independent_original_page_equivalence_review_required')
    # The caller must authenticate the supplied review locators and reviewer;
    # syntactic presence is deliberately NOT original-page certification.
    return {'protocol': PROTOCOL, 'status': result_status,
            'source_field_id': original_field['id'],
            'core_obligation': obligation, 'core_record_id': core_id,
            'core_path': path, 'core_record_blob': git_blob(raw),
            'accepted_core_receipt_commit': commit,
            'formal_acceptance': False, 'independent_review_still_required': True,
            'original_source_page_authorized': False, 'global_pages_advanced': 0}
