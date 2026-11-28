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
    Supported schemas include the observed Matrix and Target: Matrix receipt shapes.
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
        require(manifest_path in ('sources/manifests/Matrix.yml',
                                  'sources/manifests/TargetMatrix.yml'),
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
        if manifest_path == 'sources/manifests/TargetMatrix.yml':
            require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1'
                    and confirm.get('status') == 'verified',
                    'inline_index_target_matrix_verified_confirm_required')
            require(confirm.get('source') == 'source.fasa-7219' and
                    confirm.get('pdf_sha256') == 'dc9fbba78b9eb5efc60941213a90dfa0be190275dc92ea671631ddb7db154c4b',
                    'inline_index_target_matrix_original_identity_mismatch')
            require(isinstance(confirm.get('record_id'), str) and confirm['record_id'].strip()
                    and isinstance(confirm.get('path'), str)
                    and re.fullmatch(r'(references|rule|rules|equipment|options|entities|world|procedure|procedures)/[\w./-]+\.yml', confirm['path'])
                    and '..' not in confirm['path'].split('/'),
                    'inline_index_target_matrix_record_identity_required')
            require(confirm.get('commit_sha') == semantic_commit and
                    confirm.get('readback_blob_sha') == semantic_blob and
                    confirm.get('expected_blob_sha') == semantic_blob,
                    'inline_index_target_matrix_semantic_identity_mismatch')
            schema = 'target-matrix-index-receipt/v1'
    elif (manifest_path == 'sources/manifests/SprawlSurvivalGuide.yml' or
          (manifest_path == 'sources/manifests/TargetWastelands.yml' and 'index_commit_sha' in r)):
        if manifest_path == 'sources/manifests/SprawlSurvivalGuide.yml':
            source, pdf_sha, record_id, record_path, schema = (
                'source.fanpro-10667', 'b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f',
                'rule.lifestyle.ssg-detailed-lifestyle-edges-flaws-p137-144',
                'rules/lifestyle/ssg-detailed-lifestyle-edges-flaws-p137-144.yml',
                'ssg-lifestyle-p137-index-receipt/v1')
            label = 'ssg'
        else:
            source, pdf_sha, record_id, record_path, schema = (
                'source.fanpro-10653', '31db497dcbe649eda35b596ed2dff9475241518027137c65f35ea720b03d0c6b',
                'catalog.gear.target-wastelands-underwater-systems',
                'entities/gear/target-wastelands-underwater-systems.yml',
                'wastelands-underwater-p131-index-receipt/v1')
            label = 'wastelands_underwater'
        required = {'path', 'prior_blob_sha', 'index_commit_sha', 'index_blob_sha',
                    'record_id', 'semantic_commit_sha', 'semantic_blob_sha',
                    'candidate_sha256', 'immutable_sha256', 'committed_exact',
                    'live_exact', 'semantic_committed_exact', 'semantic_live_exact', 'status'}
        require(set(r) == required, f'inline_index_{label}_receipt_fields')
        require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1'
                and confirm.get('status') == 'verified', f'inline_index_{label}_verified_confirm_required')
        require(confirm.get('source') == source and confirm.get('pdf_sha256') == pdf_sha,
                f'inline_index_{label}_original_identity_mismatch')
        require(r['record_id'] == record_id and r['record_id'] == confirm.get('record_id') and
                confirm.get('path') == record_path,
                f'inline_index_{label}_record_identity_mismatch')
        require(r['status'] == 'indexed' and all(r[k] is True for k in (
                    'committed_exact', 'live_exact', 'semantic_committed_exact', 'semantic_live_exact')),
                'inline_index_original_readback_missing')
        require(all(isinstance(x, str) and re.fullmatch(r'[0-9a-f]{40}', x)
                    for x in (r['semantic_commit_sha'], r['semantic_blob_sha'], parent_blob)),
                f'inline_index_{label}_external_pins_required')
        require(r['semantic_commit_sha'] == confirm.get('commit_sha') and
                r['semantic_blob_sha'] == confirm.get('expected_blob_sha') == confirm.get('readback_blob_sha'),
                f'inline_index_{label}_semantic_identity_mismatch')
        require(all(isinstance(r[k], str) and re.fullmatch(r'[0-9a-f]{64}', r[k])
                    and r[k] == confirm.get(k) for k in ('candidate_sha256', 'immutable_sha256')),
                f'inline_index_{label}_digest_mismatch')
        commit, recorded_blob, path = r['index_commit_sha'], r['index_blob_sha'], r['path']
        prior = r['prior_blob_sha']
        require(prior == parent_blob, 'inline_index_parent_blob_mismatch')
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
    elif manifest_path == 'sources/manifests/SRComp.yml' and 'registration_delta' in r:
        # Original p17 custom-trait archive. Only this observed record/format
        # is supported; the receipt contains no historical parent blob pin.
        required = {'path', 'commit', 'blob', 'record_id',
                    'exact_commit_and_live_readback', 'registration_delta'}
        require(set(r) == required, 'inline_index_srcomp_p17_receipt_fields')
        require(r['exact_commit_and_live_readback'] is True,
                'inline_index_original_readback_missing')
        require(type(r['registration_delta']) is int and r['registration_delta'] == 1,
                'inline_index_srcomp_p17_registration_delta')
        require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1'
                and confirm.get('status') == 'verified',
                'inline_index_srcomp_p17_verified_confirm_required')
        source_sha = '8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5'
        record_id = 'option.character-creation.srcomp-custom-edge-flaw-worked-example-p17'
        record_path = 'options/character-creation/srcomp-custom-edge-flaw-worked-example-p17.yml'
        require(confirm.get('source') == 'source.srcomp' and confirm.get('pdf_sha256') == source_sha
                and confirm.get('printed_pages') == '17' and confirm.get('pdf_pages') == '18',
                'inline_index_srcomp_p17_original_identity_mismatch')
        require(r['record_id'] == confirm.get('record_id') == record_id
                and confirm.get('path') == record_path,
                'inline_index_srcomp_p17_record_identity_mismatch')
        require(all(isinstance(confirm.get(k), str) and re.fullmatch(r'[0-9a-f]{40}', confirm[k])
                    for k in ('commit_sha', 'readback_blob_sha'))
                and confirm.get('expected_blob_sha') == confirm.get('readback_blob_sha'),
                'inline_index_srcomp_p17_semantic_identity_mismatch')
        require(all(isinstance(confirm.get(k), str) and re.fullmatch(r'[0-9a-f]{64}', confirm[k])
                    for k in ('candidate_sha256', 'immutable_sha256')),
                'inline_index_srcomp_p17_digest_required')
        from validator import parse
        manifest = parse(snapshot_raw)
        require(isinstance(manifest, dict) and manifest.get('id') == confirm['source']
                and manifest.get('catalog_number') == 'FASA7905a'
                and manifest.get('edition') == 'SR3'
                and manifest.get('publisher') == 'FASA Corporation'
                and manifest.get('source_pdf_sha256') == source_sha,
                'inline_index_srcomp_p17_snapshot_identity_mismatch')
        section = manifest.get('postcompletion_mechanics_recovery')
        regs = section.get('verified_semantic_records') if isinstance(section, dict) else None
        require(isinstance(regs, list), 'inline_index_srcomp_p17_registrations_required')
        matches = [e for e in regs if isinstance(e, dict) and
                   (e.get('id') == record_id or e.get('path') == record_path)]
        require(len(matches) == 1, 'inline_index_srcomp_p17_unique_registration_required')
        entry = matches[0]
        from index_transition import _identity, _gate
        require(_identity(entry) == (record_id, record_path, confirm['commit_sha'],
                                     confirm['readback_blob_sha'])
                and _gate(entry) == 'verified'
                and entry.get('content_class') == 'character_option'
                and entry.get('original_source_sha256') == source_sha
                and entry.get('range_printed') == [17, 17]
                and entry.get('range_pdf') == [18, 18]
                and all(type(n) is int for n in entry['range_printed'] + entry['range_pdf'])
                and entry.get('contiguous_advance') is False
                and all(entry.get(k) == confirm[k] for k in ('candidate_sha256', 'immutable_sha256')),
                'inline_index_srcomp_p17_registration_mismatch')
        commit, recorded_blob, path = r['commit'], r['blob'], r['path']
        prior, schema = None, 'srcomp-p17-index-receipt/v1'
    elif manifest_path == 'sources/manifests/SRComp.yml':
        from srcomp_index_receipts import adapt
        commit, recorded_blob, path, prior, schema = adapt(r, snapshot_raw, manifest_path, confirm)
    elif manifest_path == 'sources/manifests/MrJohnsonsLittleBlackBook.yml':
        # Actual FanPro25003 archived compact index receipt. The exact flag
        # attests the retained snapshot only; do not invent an original parent
        # digest or distinguish branch/commit attestations absent in the receipt.
        # Full verify() still requires original artifact custody, exact historical
        # bytes and the separate actual Git registration transition.
        require(set(r) == {'commit', 'blob', 'exact'},
                'inline_index_mjlbb_receipt_fields')
        require(r['exact'] is True, 'inline_index_original_readback_missing')
        require(isinstance(confirm, dict) and confirm.get('protocol') == 'sr3-gate/v1'
                and confirm.get('status') == 'verified',
                'inline_index_mjlbb_verified_confirm_required')
        source_sha = '2426699e60652473e1d1be3387c6baf45fa950d3b1ae05e8cfd07302bc34cd5d'
        require(confirm.get('source') == 'source.fanpro-25003' and
                confirm.get('pdf_sha256') == source_sha,
                'inline_index_mjlbb_original_identity_mismatch')
        record_id, record_path = confirm.get('record_id'), confirm.get('path')
        require(isinstance(record_id, str) and record_id.startswith('reference.mjlbb.')
                and isinstance(record_path, str)
                and re.fullmatch(r'references/campaign/mjlbb-[A-Za-z0-9_-]+\.yml', record_path),
                'inline_index_mjlbb_record_identity_required')
        require(all(isinstance(confirm.get(k), str) and
                    re.fullmatch(r'[0-9a-f]{40}', confirm[k]) for k in
                    ('commit_sha', 'readback_blob_sha')) and
                confirm.get('expected_blob_sha') == confirm.get('readback_blob_sha'),
                'inline_index_mjlbb_semantic_identity_mismatch')
        require(all(isinstance(confirm.get(k), str) and
                    re.fullmatch(r'[0-9a-f]{64}', confirm[k]) for k in
                    ('candidate_sha256', 'immutable_sha256')),
                'inline_index_mjlbb_digest_required')
        # Reuse the strict YAML parser rather than accepting duplicate keys.
        from validator import parse
        manifest = parse(snapshot_raw)
        require(isinstance(manifest, dict) and manifest.get('id') == confirm['source']
                and manifest.get('catalog_number') == 'FanPro25003'
                and manifest.get('edition') == 'SR3'
                and manifest.get('source_pdf_sha256') == source_sha,
                'inline_index_mjlbb_snapshot_identity_mismatch')
        regs = manifest.get('verified_semantic_records')
        require(isinstance(regs, list), 'inline_index_mjlbb_registrations_required')
        matches = [e for e in regs if isinstance(e, dict) and
                   (e.get('id') == record_id or e.get('path') == record_path)]
        require(len(matches) == 1, 'inline_index_mjlbb_unique_registration_required')
        entry = matches[0]
        require(entry.get('id') == record_id and entry.get('path') == record_path
                and entry.get('commit') == confirm['commit_sha']
                and entry.get('blob') == confirm['readback_blob_sha']
                and entry.get('gate') == 'verified'
                and all(entry.get(k) == confirm[k] for k in
                        ('candidate_sha256', 'immutable_sha256')),
                'inline_index_mjlbb_registration_mismatch')
        commit, recorded_blob, path = r['commit'], r['blob'], manifest_path
        prior, schema = None, 'mjlbb-compact-index-receipt/v1'
    elif (manifest_path == 'sources/manifests/Rigger3Revised.yml' or
          (manifest_path == 'sources/manifests/M&M.yml' and 'semantic_live_and_commit_exact' in r)):
        from r3r_mm_index_receipts import adapt
        commit, recorded_blob, path, prior, schema = adapt(r, snapshot_raw, manifest_path, confirm)
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
                            semantic_blob=confirm['readback_blob_sha'], confirm=confirm)
    return verify_bytes(receipt, snapshot, manifest_path, commit, blob(actual), prior,
                        confirm=transaction.get('confirm'))
