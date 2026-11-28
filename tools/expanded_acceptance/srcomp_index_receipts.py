"""Two observed Companion historical index receipt layouts (read-only)."""
import re
from index_transition import _identity, _gate

SOURCE = 'source.srcomp'
SHA = '8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5'
MANIFEST = 'sources/manifests/SRComp.yml'
DISCLOSURE_KEY = 'srcomp_contact_disclosure_example_original_p67_2026_11_25'
DISCLOSURE_ID = 'rule.contacts.srcomp-contact-success-contest-p67-68'
DISCLOSURE_PATH = 'rules/contacts/srcomp-contact-success-contest-p67-68.yml'
LAW_ID = 'option.campaign.srcomp-law-campaign-resource-access-p117-118'
LAW_PATH = 'rules/campaign/srcomp-law-campaign-resource-access-p117-118.yml'
COMMON = {'manifest_path', 'index_commit', 'index_blob', 'semantic_commit', 'semantic_blob'}


def require(ok, reason):
    if not ok:
        raise ValueError('inline_index_srcomp_' + reason)


def adapt(r, snapshot_raw, manifest_path, confirm):
    """Require original receipt, verified confirm and exact source-specific entry.

    The caller must separately establish custody and actual index transition;
    neither original receipt contains a parent hash.
    """
    from validator import parse
    require(manifest_path == MANIFEST and r.get('manifest_path') == MANIFEST, 'manifest')
    require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1'
            and confirm.get('status') == 'verified' and confirm.get('source') == SOURCE
            and confirm.get('pdf_sha256') == SHA, 'confirm_source')
    require(all(isinstance(confirm.get(k), str) and re.fullmatch(r'[0-9a-f]{40}', confirm[k])
                for k in ('commit_sha', 'readback_blob_sha'))
            and confirm.get('expected_blob_sha') == confirm.get('readback_blob_sha')
            and (r.get('semantic_commit'), r.get('semantic_blob')) ==
            (confirm['commit_sha'], confirm['readback_blob_sha']), 'semantic_identity')
    require(all(isinstance(confirm.get(k), str) and re.fullmatch(r'[0-9a-f]{64}', confirm[k])
                for k in ('candidate_sha256', 'immutable_sha256')), 'confirm_digests')
    m = parse(snapshot_raw)
    require(isinstance(m, dict) and m.get('id') == SOURCE and m.get('source_pdf_sha256') == SHA
            and m.get('edition') == 'SR3' and m.get('catalog_number') == 'FASA7905a'
            and m.get('publisher') == 'FASA Corporation', 'snapshot_identity')
    if set(r) == COMMON | {'registration_key', 'exact_commit_and_live_bytes'}:
        require(r['registration_key'] == DISCLOSURE_KEY and r['exact_commit_and_live_bytes'] is True,
                'disclosure_receipt_flags')
        rid, path, pages, pdfs = DISCLOSURE_ID, DISCLOSURE_PATH, [67, 68], [68, 69]
        entry = m.get(DISCLOSURE_KEY)
        require(isinstance(entry, dict) and entry.get('source_id') == SOURCE
                and entry.get('original_pdf_sha256') == SHA
                and entry.get('actual_confirm') == 'verified'
                and entry.get('exact_commit_and_live_bytes') is True
                and entry.get('content_class') == 'rule_exact'
                and type(entry.get('global_contiguous_pages')) is int
                and entry['global_contiguous_pages'] == 0, 'disclosure_entry_flags')
        ep, ef = entry.get('printed_pages'), entry.get('physical_pdf_pages')
        schema = 'srcomp-disclosure-index-receipt/v1'
    elif set(r) == COMMON | {'exact_commit_live_readback', 'registration_matched', 'global_pages_advanced'}:
        require(r['exact_commit_live_readback'] is True and r['registration_matched'] is True
                and type(r['global_pages_advanced']) is int and r['global_pages_advanced'] == 0,
                'law_receipt_flags')
        rid, path, pages, pdfs = LAW_ID, LAW_PATH, [117, 118], [118, 119]
        section = m.get('postcompletion_mechanics_recovery')
        regs = section.get('verified_semantic_records') if isinstance(section, dict) else None
        require(isinstance(regs, list), 'law_registrations')
        matches = [e for e in regs if isinstance(e, dict) and
                   (e.get('id') == rid or e.get('path') == path)]
        require(len(matches) == 1, 'law_unique_registration')
        entry = matches[0]
        require(entry.get('original_source_sha256') == SHA
                and entry.get('content_class') == 'character_option'
                and entry.get('contiguous_advance') is False, 'law_entry_flags')
        ep, ef = entry.get('range_printed'), entry.get('range_pdf')
        schema = 'srcomp-law-campaign-index-receipt/v1'
    else:
        raise ValueError('inline_index_unsupported_receipt_schema')
    require(confirm.get('record_id') == rid and confirm.get('path') == path
            and confirm.get('printed_pages') == '-'.join(map(str, pages))
            and confirm.get('pdf_pages') == '-'.join(map(str, pdfs)), 'record_scope')
    require(ep == pages and ef == pdfs and all(type(n) is int for n in ep + ef), 'entry_pages')
    require(_identity(entry) == (rid, path, confirm['commit_sha'], confirm['readback_blob_sha'])
            and _gate(entry) == 'verified'
            and all(entry.get(k) == confirm[k] for k in ('candidate_sha256', 'immutable_sha256')),
            'entry_identity')
    return r['index_commit'], r['index_blob'], MANIFEST, None, schema
