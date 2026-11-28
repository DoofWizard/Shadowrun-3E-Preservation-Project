"""Exact observed R3R route/environment and M&M purchase receipt adapters.

The original receipts have no parent digest. A successful check only confirms
these archived receipt/snapshot bindings. The existing actual Git transition,
source review, independent custody and chronology remain mandatory.
"""
from source_index_receipts import MM, MM_SOURCE, MM_SHA, pin, require
from index_transition import _identity, _gate, _registrations

R3R = 'sources/manifests/Rigger3Revised.yml'
R3R_SOURCE = 'source.fanpro-10662'
R3R_SHA = '88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909'
MM_KEYS = {'source', 'semantic_commit', 'semantic_blob', 'index_commit',
           'index_blob', 'semantic_live_and_commit_exact',
           'manifest_live_and_commit_exact', 'gate', 'status'}
R3R_KEYS = {'semantic_commit', 'semantic_blob', 'manifest_commit',
            'manifest_blob', 'commit_readback_exact', 'live_readback_exact',
            'registration_count'}
MM_RECORDS = {
    'entities/cyberware/muscle-replacement.yml': ('entity.cyberware.muscle-replacement',
        'confirmed_muscle_replacement_purchase_2026_11_28'),
    'entities/cyberware/simrig-simlink.yml': ('entity.cyberware.simrig-simlink',
        'confirmed_simrig_simlink_purchase_2026_11_28'),
}
R3R_RECORDS = {
    'rules/vehicles/r3-revised-design-modification-cost-basis-p112.yml':
        ('rule.vehicles.r3-revised-design-modification-cost-basis-p112', '112', '114', [112, 112], [114, 114]),
    'rules/vehicles/r3-revised-vehicle-market-class-qualifications-p113.yml':
        ('rule.vehicles.r3-revised-vehicle-market-class-qualifications-p113', '113', '115', [113, 113], [115, 115]),
    'rules/vehicles/r3-revised-final-design-cost-worked-examples-p113-114.yml':
        ('rule.vehicles.r3-revised-final-design-cost-worked-examples-p113-114', '113-114', '115-116', [113, 114], [115, 116]),
    'rules/vehicles/r3-revised-design-option-entry-point-operations-p114-115.yml':
        ('rule.vehicles.r3-revised-design-option-entry-point-operations-p114-115', '114-115', '116-117', [114, 115], [116, 117]),
    'rules/vehicles/r3-revised-autonav-route-eligibility-p128.yml':
        ('rule.vehicles.r3-revised-autonav-route-eligibility-p128', '128', '130', [128, 128], [130, 130]),
    'rules/vehicles/r3-revised-environmental-system-qualifications-p132-133.yml':
        ('rule.vehicles.r3-revised-environmental-system-qualifications-p132-133',
         '132-133', '134-135', [132, 133], [134, 135]),
}


def adapt(receipt, snapshot, manifest_path, confirm):
    from validator import parse
    require(manifest_path in (MM, R3R), 'r3r_mm_manifest_required')
    is_mm = manifest_path == MM
    source, source_sha, catalog, edition, publisher = (
        (MM_SOURCE, MM_SHA, 'FASA7126', 'SR3', 'FASA Corporation') if is_mm else
        (R3R_SOURCE, R3R_SHA, 'FanPro10662', 'Shadowrun Third Edition', 'FanPro'))
    require(isinstance(receipt, dict) and set(receipt) == (MM_KEYS if is_mm else R3R_KEYS),
            'r3r_mm_receipt_fields')
    require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1'
            and confirm.get('status') == 'verified', 'r3r_mm_verified_confirm_required')
    require(confirm.get('source') == source and confirm.get('pdf_sha256') == source_sha,
            'r3r_mm_original_identity_mismatch')
    require(all(pin(confirm.get(k)) for k in ('commit_sha', 'readback_blob_sha'))
            and confirm.get('expected_blob_sha') == confirm['readback_blob_sha'],
            'r3r_mm_semantic_pin_required')
    require(all(pin(confirm.get(k), 64) for k in ('candidate_sha256', 'immutable_sha256')),
            'r3r_mm_digest_required')
    require((receipt['semantic_commit'], receipt['semantic_blob']) ==
            (confirm['commit_sha'], confirm['readback_blob_sha']), 'r3r_mm_semantic_identity_mismatch')
    path = confirm.get('path')
    require(isinstance(path, str) and path in (MM_RECORDS if is_mm else R3R_RECORDS),
            'r3r_mm_record_path_required')
    doc = parse(snapshot)
    require(isinstance(doc, dict) and (doc.get('id'), doc.get('source_pdf_sha256'),
            doc.get('catalog_number'), doc.get('edition'), doc.get('publisher')) ==
            (source, source_sha, catalog, edition, publisher), 'r3r_mm_snapshot_identity_mismatch')
    if is_mm:
        record_id, section_name = MM_RECORDS[path]
        require(receipt['source'] == source and receipt['gate'] == 'verified'
                and receipt['status'] == 'indexed', 'r3r_mm_original_status_required')
        require(receipt['semantic_live_and_commit_exact'] is True and
                receipt['manifest_live_and_commit_exact'] is True, 'r3r_mm_original_readback_missing')
        require((confirm.get('printed_pages'), confirm.get('pdf_pages')) == ('154', '155'),
                'r3r_mm_original_pages_mismatch')
        sections = doc.get('source_field_review')
        section = sections.get(section_name) if isinstance(sections, dict) else None
        regs = section.get('records') if isinstance(section, dict) else None
        require(isinstance(regs, list), 'r3r_mm_original_registration_list_required')
        require(section.get('source_pdf_sha256') == source_sha, 'r3r_mm_section_source_mismatch')
        commit, recorded_blob, schema = receipt['index_commit'], receipt['index_blob'], 'mm-p154-purchase-index-receipt/v1'
    else:
        record_id, printed, pdf, printed_range, pdf_range = R3R_RECORDS[path]
        require((confirm.get('printed_pages'), confirm.get('pdf_pages')) == (printed, pdf),
                'r3r_mm_original_pages_mismatch')
        require(receipt['commit_readback_exact'] is True and receipt['live_readback_exact'] is True,
                'r3r_mm_original_readback_missing')
        regs = doc.get('verified_semantic_records')
        require(isinstance(regs, list) and type(receipt['registration_count']) is int
                and receipt['registration_count'] == len(regs), 'r3r_mm_registration_count_mismatch')
        commit, recorded_blob, schema = receipt['manifest_commit'], receipt['manifest_blob'], 'r3r-qualified-index-receipt/v1'
    require(confirm.get('record_id') == record_id, 'r3r_mm_record_id_mismatch')
    identity = (record_id, path, confirm['commit_sha'], confirm['readback_blob_sha'])
    matches = [e for e in regs if isinstance(e, dict) and (e.get('id') == record_id or e.get('path') == path)]
    require(len(matches) == 1, 'r3r_mm_unique_registration_required')
    entry = matches[0]
    require(_identity(entry) == identity and _gate(entry) == 'verified', 'r3r_mm_registration_identity_mismatch')
    require(list(_registrations(doc, identity)).count((identity, 'verified')) == 1,
            'r3r_mm_duplicate_verified_registration')
    require(all(entry.get(k) == confirm[k] for k in ('candidate_sha256', 'immutable_sha256'))
            and pin(entry.get('baseline_sha256'), 64), 'r3r_mm_registration_digest_mismatch')
    if is_mm:
        require((entry.get('printed'), entry.get('pdf')) == ('154', '155'), 'r3r_mm_registration_pages_mismatch')
    else:
        require(entry.get('range_printed') == printed_range and entry.get('range_pdf') == pdf_range
                and all(type(n) is int for n in entry['range_printed'] + entry['range_pdf'])
                and entry.get('content_class') == 'rule_exact'
                and entry.get('original_source_sha256') == source_sha
                and entry.get('contiguous_advance') is False, 'r3r_mm_registration_pages_mismatch')
    require(pin(commit) and pin(recorded_blob), 'r3r_mm_index_pin_required')
    # No original receipt parent digest exists. Do not invent one.
    return commit, recorded_blob, manifest_path, None, schema
