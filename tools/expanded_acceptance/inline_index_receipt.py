"""Read-only validation of retained original inline index receipts and snapshots.

Receipt custody must be independently pinned by the coordinator. A present-day
Git export is not an original archived local snapshot.
"""
import base64
import hashlib
import json
import re


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, 'inline_index_duplicate_receipt_key')
        out[key] = value
    return out


def artifact(a):
    require(isinstance(a, dict) and isinstance(a.get('original_locator'), str)
            and a['original_locator'].strip(), 'inline_index_original_locator_required')
    raw = base64.b64decode(a['bytes_base64'], validate=True)
    require(digest(raw) == a['sha256'], 'inline_index_artifact_digest_mismatch')
    return raw


def verify_bytes(receipt_raw, snapshot_raw, manifest_path, index_commit,
                 historical_blob, parent_blob=None, *,
                 semantic_commit=None, semantic_blob=None, confirm=None):
    """Check exact archived bytes against independently obtained Git blob pins.

    This lower-level diagnostic does not establish Git ancestry or custody.
    Supported schemas are the observed Rigger, split, Matrix, M&M and CC receipt shapes.
    """
    r = json.loads(receipt_raw, object_pairs_hook=pairs)
    require(isinstance(r, dict), 'inline_index_receipt_object_required')
    require(re.fullmatch(r'[0-9a-f]{40}', index_commit) and
            re.fullmatch(r'[0-9a-f]{40}', historical_blob), 'inline_index_full_git_pin_required')
    require(manifest_path == 'sources/manifests/M&M.yml' or
            re.fullmatch(r'sources/manifests/[A-Za-z0-9_.-]+\.yml', manifest_path),
            'inline_index_manifest_path_required')
    if {'commit_sha', 'blob_sha', 'manifest_path', 'readback_exact'} <= r.keys():
        require(set(r) <= {'commit_sha', 'blob_sha', 'manifest_path', 'readback_exact',
                           'prior_blob_sha', 'contiguous_advance'}, 'inline_index_unknown_receipt_fields')
        commit, recorded_blob, path = r['commit_sha'], r['blob_sha'], r['manifest_path']
        require(r['readback_exact'] is True, 'inline_index_original_readback_missing')
        if 'contiguous_advance' in r:
            require(type(r['contiguous_advance']) is bool, 'inline_index_invalid_advance_type')
        prior = r.get('prior_blob_sha')
        schema = 'rigger-index-receipt/v1'
    elif {'commit', 'blob', 'path', 'exact_commit_live_bytes', 'registration_key'} <= r.keys():
        require(set(r) <= {'commit', 'blob', 'path', 'exact_commit_live_bytes', 'registration_key'},
                'inline_index_unknown_receipt_fields')
        commit, recorded_blob, path = r['commit'], r['blob'], r['path']
        require(r['exact_commit_live_bytes'] is True, 'inline_index_original_readback_missing')
        require(isinstance(r['registration_key'], str) and r['registration_key'],
                'inline_index_registration_key_required')
        prior = None
        schema = 'split-index-receipt/v1'
    elif 'exact_commit_and_branch_readback' in r:
        required = {'path', 'commit', 'blob', 'previous_blob', 'semantic_commit',
                    'semantic_blob', 'exact_commit_and_branch_readback', 'commit_sha', 'blob_sha'}
        require(set(r) == required, 'inline_index_matrix_receipt_fields')
        require(manifest_path == 'sources/manifests/Matrix.yml',
                'inline_index_matrix_manifest_required')
        commit, recorded_blob, path = r['commit'], r['blob'], r['path']
        require((r['commit_sha'], r['blob_sha']) == (commit, recorded_blob),
                'inline_index_matrix_conflicting_aliases')
        require(r['exact_commit_and_branch_readback'] is True,
                'inline_index_original_readback_missing')
        require(all(isinstance(x, str) and re.fullmatch(r'[0-9a-f]{40}', x)
                    for x in (semantic_commit, semantic_blob, parent_blob)),
                'inline_index_matrix_external_pins_required')
        require((r['semantic_commit'], r['semantic_blob']) == (semantic_commit, semantic_blob),
                'inline_index_matrix_semantic_identity_mismatch')
        prior = r['previous_blob']
        require(isinstance(prior, str) and prior == parent_blob,
                'inline_index_parent_blob_mismatch')
        schema = 'matrix-index-receipt/v1'
    elif manifest_path == 'sources/manifests/TargetWastelands.yml':
        required = {'source', 'record_id', 'index_commit', 'manifest_blob_sha',
                    'previous_manifest_blob_sha', 'readback_commit_and_main_blob_match',
                    'semantic_commit'}
        require(set(r) == required, 'inline_index_wastelands_receipt_fields')
        require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1'
                and confirm.get('status') == 'verified', 'inline_index_wastelands_verified_confirm_required')
        require(r['source'] == confirm.get('source') == 'source.fanpro-10653'
                and confirm.get('pdf_sha256') == '31db497dcbe649eda35b596ed2dff9475241518027137c65f35ea720b03d0c6b',
                'inline_index_wastelands_original_identity_mismatch')
        require(isinstance(r['record_id'], str) and bool(r['record_id'])
                and r['record_id'] == confirm.get('record_id'),
                'inline_index_wastelands_record_identity_mismatch')
        require(all(isinstance(x, str) and re.fullmatch(r'[0-9a-f]{40}', x)
                    for x in (confirm.get('commit_sha'), confirm.get('readback_blob_sha'), parent_blob)),
                'inline_index_wastelands_external_pins_required')
        require(r['semantic_commit'] == confirm['commit_sha']
                and confirm.get('expected_blob_sha') == confirm['readback_blob_sha'],
                'inline_index_wastelands_semantic_identity_mismatch')
        require(r['readback_commit_and_main_blob_match'] is True,
                'inline_index_original_readback_missing')
        commit, recorded_blob, path = r['index_commit'], r['manifest_blob_sha'], manifest_path
        prior = r['previous_manifest_blob_sha']
        require(prior == parent_blob, 'inline_index_parent_blob_mismatch')
        schema = 'wastelands-alter-pressure-index-receipt/v1'
    elif manifest_path in ('sources/manifests/M&M.yml', 'sources/manifests/CannonCompanion.yml'):
        from source_index_receipts import adapt
        commit, recorded_blob, path, prior, schema = adapt(
            r, snapshot_raw, manifest_path, confirm, parent_blob)
    else:
        raise ValueError('inline_index_unsupported_receipt_schema')
    require((commit, recorded_blob, path) == (index_commit, historical_blob, manifest_path),
            'inline_index_receipt_identity_mismatch')
    require(blob(snapshot_raw) == historical_blob, 'inline_index_snapshot_blob_mismatch')
    if prior is not None:
        require(isinstance(prior, str) and re.fullmatch(r'[0-9a-f]{40}', prior),
                'inline_index_invalid_parent_blob')
        if parent_blob is not None:
            require(prior == parent_blob, 'inline_index_parent_blob_mismatch')
    return {'status': 'consistent_original_index_artifacts', 'schema': schema,
            'index_commit': index_commit, 'index_blob': historical_blob,
            'receipt_sha256': digest(receipt_raw), 'snapshot_sha256': digest(snapshot_raw),
            'receipt_prior_blob': prior, 'receipt_prior_blob_checked': prior is not None and parent_blob is not None,
            'formal_acceptance': False}


def verify(git, manifest_path, transaction, transition):
    """Production CLI supplement to the actual index-transition proof."""
    for key in ('historical_index_receipt_artifact', 'historical_index_snapshot_artifact'):
        require(key in transaction, 'inline_index_missing:' + key)
    receipt = artifact(transaction['historical_index_receipt_artifact'])
    snapshot = artifact(transaction['historical_index_snapshot_artifact'])
    commit = transaction['index_commit']
    require(transition['index_commit'] == commit and
            transition['status'] == 'new_or_changed_verified_registration',
            'inline_index_transition_required')
    actual = git.read(manifest_path, commit)
    require(snapshot == actual, 'inline_index_snapshot_bytes_mismatch')
    r = json.loads(receipt, object_pairs_hook=pairs)
    prior = None
    if ('prior_blob_sha' in r or 'exact_commit_and_branch_readback' in r or
            (manifest_path == 'sources/manifests/CannonCompanion.yml' and 'prior_blob' in r) or
            manifest_path == 'sources/manifests/TargetWastelands.yml'):
        prior = blob(git.read(manifest_path, transition['index_parent']))
    if 'registration_key' in r:
        key = r['registration_key']
        require(isinstance(key, str) and transition['index_pointer'] == '/' +
                key.replace('~', '~0').replace('/', '~1'), 'inline_index_registration_pointer_mismatch')
    if 'exact_commit_and_branch_readback' in r:
        confirm = transaction['confirm']
        require(confirm['status'] == 'verified', 'inline_index_matrix_verified_confirm_required')
        return verify_bytes(receipt, snapshot, manifest_path, commit, blob(actual), prior,
                            semantic_commit=confirm['commit_sha'],
                            semantic_blob=confirm['readback_blob_sha'])
    return verify_bytes(receipt, snapshot, manifest_path, commit, blob(actual), prior,
                        confirm=transaction.get('confirm'))
