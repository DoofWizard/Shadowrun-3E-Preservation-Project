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
                 historical_blob, parent_blob=None):
    """Check exact archived bytes against independently obtained Git blob pins.

    This lower-level diagnostic does not establish Git ancestry or custody.
    Supported schemas are the observed Rigger and split-archive receipt shapes.
    """
    r = json.loads(receipt_raw, object_pairs_hook=pairs)
    require(isinstance(r, dict), 'inline_index_receipt_object_required')
    require(re.fullmatch(r'[0-9a-f]{40}', index_commit) and
            re.fullmatch(r'[0-9a-f]{40}', historical_blob), 'inline_index_full_git_pin_required')
    require(re.fullmatch(r'sources/manifests/[A-Za-z0-9_.-]+\.yml', manifest_path),
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
    if 'prior_blob_sha' in r:
        prior = blob(git.read(manifest_path, transition['index_parent']))
    if 'registration_key' in r:
        key = r['registration_key']
        require(isinstance(key, str) and transition['index_pointer'] == '/' +
                key.replace('~', '~0').replace('/', '~1'), 'inline_index_registration_pointer_mismatch')
    return verify_bytes(receipt, snapshot, manifest_path, commit, blob(actual), prior)
