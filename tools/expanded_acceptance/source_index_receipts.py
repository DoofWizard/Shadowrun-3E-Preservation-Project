"""Exact original receipt schemas for M&M and Cannon Companion.

The caller must verify the original snapshot, independent custody, and actual
Git registration transition. This adapter does not establish those facts.
"""
import hashlib
import re


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def pin(value, length=40):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-f]{%d}' % length, value) is not None


MM = 'sources/manifests/M&M.yml'
CC = 'sources/manifests/CannonCompanion.yml'
MM_SOURCE = 'source.mm'
CC_SOURCE = 'source.cc'
MM_SHA = '6d4e25208e8ee3b8b8b05a7f9308ccdbf5a73f090f4d0b32a0916457a9dc5ec8'
CC_SHA = '7b979ed358aaa23bbe68eb95a0887b1315f302bedd6bcc04df00d8d68fbd84a4'
MM_SHORT = {'status', 'path', 'commit', 'blob', 'branch_and_commit_readbacks_equal', 'exact_local_proposal_match'}
MM_FULL = {'status', 'source', 'path', 'record_id', 'semantic_commit', 'semantic_blob', 'manifest_commit', 'manifest_blob', 'manifest_sha256', 'branch_and_commit_readback_equal', 'exact_index_proposal_readback_equal', 'global_contiguous_page_credit', 'blob_sha', 'commit_sha'}
CC_FULL = {'semantic_commit', 'semantic_blob', 'index_commit', 'index_blob', 'exact_live_readback', 'exact_commit_readback', 'path', 'record_id', 'record_path', 'status', 'source', 'manifest_commit', 'manifest_blob', 'source_pdf_sha256', 'commit_sha', 'blob_sha', 'prior_blob', 'exact_committed_and_live_bytes_match', 'commit_readback_blob', 'live_readback_blob'}


def adapt(receipt, snapshot, manifest_path, confirm, parent_blob):
    """Normalize a recognized *exact* schema, never synthesize attestations."""
    require(manifest_path in (MM, CC), 'source_index_unsupported_manifest')
    source, source_sha = (MM_SOURCE, MM_SHA) if manifest_path == MM else (CC_SOURCE, CC_SHA)
    require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1' and confirm.get('status') == 'verified', 'source_index_verified_confirm_required')
    require(confirm.get('source') == source and confirm.get('pdf_sha256') == source_sha, 'source_index_original_identity_mismatch')
    for key in ('commit_sha', 'readback_blob_sha'):
        require(pin(confirm.get(key)), 'source_index_semantic_pin_required:' + key)
    require(confirm.get('expected_blob_sha') == confirm['readback_blob_sha'], 'source_index_confirm_blob_mismatch')
    for key in ('path', 'record_id'):
        require(isinstance(confirm.get(key), str) and bool(confirm[key]), 'source_index_record_identity_required:' + key)
    require(isinstance(receipt, dict) and receipt.get('status') == 'indexed', 'source_index_original_status_required')
    keys = set(receipt)
    if manifest_path == MM and keys == MM_SHORT:
        require(receipt['path'] == manifest_path and receipt['branch_and_commit_readbacks_equal'] is True and receipt['exact_local_proposal_match'] is True, 'source_index_mm_original_readback_missing')
        commit, blob = receipt['commit'], receipt['blob']
        prior, schema = None, 'mm-reservoir-index-receipt/v1'
    elif manifest_path == MM and keys == MM_FULL:
        require(receipt['source'] == source and receipt['path'] == confirm['path'] and receipt['record_id'] == confirm['record_id'], 'source_index_mm_record_identity_mismatch')
        require((receipt['semantic_commit'], receipt['semantic_blob']) == (confirm['commit_sha'], confirm['readback_blob_sha']), 'source_index_semantic_identity_mismatch')
        require(receipt['branch_and_commit_readback_equal'] is True and receipt['exact_index_proposal_readback_equal'] is True, 'source_index_mm_original_readback_missing')
        require(type(receipt['global_contiguous_page_credit']) is int and receipt['global_contiguous_page_credit'] == 0, 'source_index_mm_global_credit_mismatch')
        require(receipt['manifest_sha256'] == hashlib.sha256(snapshot).hexdigest(), 'source_index_mm_snapshot_digest_mismatch')
        commit, blob = receipt['manifest_commit'], receipt['manifest_blob']
        require((receipt['commit_sha'], receipt['blob_sha']) == (commit, blob), 'source_index_conflicting_aliases')
        prior, schema = None, 'mm-device-index-receipt/v1'
    elif manifest_path == CC and keys == CC_FULL:
        require(receipt['source'] == source and receipt['source_pdf_sha256'] == source_sha and receipt['path'] == manifest_path and receipt['record_path'] == confirm['path'] and receipt['record_id'] == confirm['record_id'], 'source_index_cc_record_identity_mismatch')
        require((receipt['semantic_commit'], receipt['semantic_blob']) == (confirm['commit_sha'], confirm['readback_blob_sha']), 'source_index_semantic_identity_mismatch')
        require(all(receipt[k] is True for k in ('exact_live_readback', 'exact_commit_readback', 'exact_committed_and_live_bytes_match')), 'source_index_cc_original_readback_missing')
        commit, blob = receipt['index_commit'], receipt['index_blob']
        require((receipt['manifest_commit'], receipt['manifest_blob']) == (commit, blob) and (receipt['commit_sha'], receipt['blob_sha']) == (commit, blob) and receipt['commit_readback_blob'] == receipt['live_readback_blob'] == blob, 'source_index_conflicting_aliases')
        prior, schema = receipt['prior_blob'], 'cc-index-receipt/v1'
        require(pin(parent_blob) and prior == parent_blob, 'source_index_cc_parent_blob_mismatch')
    else:
        raise ValueError('source_index_unsupported_receipt_schema')
    require(pin(commit) and pin(blob), 'source_index_index_pin_required')
    return commit, blob, manifest_path, prior, schema
