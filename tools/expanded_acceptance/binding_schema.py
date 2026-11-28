"""Narrow acceptance-only adapters for observed source-local binding schemas."""
import re

from source_index_receipts import MM, MM_SOURCE, MM_SHA, require


def safe_git_path(path):
    return isinstance(path, str) and (path == MM or bool(re.fullmatch(
        r'[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*', path))) and not {'.', '..'}.intersection(path.split('/'))


def substantive_pointer(binding, field):
    pointer, path = binding.get('pointer'), binding.get('path')
    if not isinstance(pointer, str) or not safe_git_path(path):
        return False
    if pointer.startswith('/data/') and len(pointer) > len('/data/'):
        return True
    return (binding.get('mode', 'source_local') == 'source_local' and
            field.get('class') == 'equipment_stat' and path.startswith('entities/') and
            pointer.startswith('/intrinsic/') and len(pointer) > len('/intrinsic/'))


def mm_registration(source, record, plan, confirm, baseline_sha, entry, pointer):
    """The observed nested M&M schema omits content_class but pins candidate bytes.

    Require exact class on the independent record and source review elsewhere;
    this does not infer a class from a summary or fill an absent field.
    """
    require(source['manifest'] == MM and source['id'] == MM_SOURCE and source['sha256'] == MM_SHA,
            'mm_registration_original_identity_mismatch')
    require(re.fullmatch(r'/source_field_review/confirmed_[A-Za-z0-9_]+/records/(0|[1-9][0-9]*)', pointer),
            'mm_registration_unsupported_pointer')
    keys = {'id', 'path', 'printed', 'pdf', 'commit', 'blob', 'baseline_sha256', 'candidate_sha256', 'immutable_sha256', 'gate', 'fields'}
    require(set(entry) == keys, 'mm_registration_unsupported_entry_schema')
    require(record['source'] == MM_SOURCE and record['edition_scope'] == 'SR3' and
            len(record['content_class']) == 1 and record['content_class'][0] in {'rule_exact', 'rule_procedure', 'equipment_stat', 'character_option', 'campaign_guidance'},
            'mm_registration_record_class_or_edition_mismatch')
    expected = {'id': record['id'], 'path': plan['path'], 'printed': record['printed_pages'],
                'pdf': record['pdf_pages'], 'commit': confirm['commit_sha'], 'blob': confirm['readback_blob_sha'],
                'baseline_sha256': baseline_sha, 'candidate_sha256': plan['candidate_sha256'],
                'immutable_sha256': plan['immutable_sha256'], 'gate': 'verified'}
    require(all(type(entry[k]) is type(v) and entry[k] == v for k, v in expected.items()),
            'mm_registration_exact_evidence_mismatch')
    require(isinstance(entry['fields'], str) and entry['fields'].strip(), 'mm_registration_scope_missing')
    return True
