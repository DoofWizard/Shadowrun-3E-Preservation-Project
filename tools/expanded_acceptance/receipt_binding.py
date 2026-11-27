"""Bind original split archives to an independently pinned editorial attestation.

Read-only backend for expanded acceptance; never manufactures historical review.
"""
import base64
import json
from pathlib import Path
import tempfile

import yaml
from archive_adapter import (PRE, POST, Strict, blob, inspect, load_json,
                             read_archive, require, sha)

LAYOUT = 'split_archive/v1'


def exact(a, b):
    return json.dumps(a, sort_keys=True, allow_nan=False) == json.dumps(b, sort_keys=True, allow_nan=False)


def bind_archive(git, source, path, transaction, inventory_reviewer, custodian):
    """Trusted caller pins entire transaction bundle and independent attestation.

    Git interface is the validator's immutable, full-commit Git reader.
    Source identity is independently verified by the outer source validator.
    """
    require(transaction['layout'] == LAYOUT, 'unsupported_archive_layout')
    pre = base64.b64decode(transaction['pre_base64'], validate=True)
    post = base64.b64decode(transaction['post_base64'], validate=True)
    att_raw = base64.b64decode(transaction['attestation_base64'], validate=True)
    require(sha(att_raw) == transaction['attestation_sha256'], 'editorial_attestation_pin_mismatch')
    a = read_archive(pre, transaction['pre_sha256'], PRE)
    b = read_archive(post, transaction['post_sha256'], POST)
    plan = load_json(a['journal/plan.json'])
    rb = load_json(b['journal/readback-receipt.json'])
    idx = load_json(b['journal/index-receipt.json'])
    record = yaml.load(a['journal/candidate.yml'], Loader=Strict)
    mp = source['manifest']
    require(plan['source'] == source['id'] == record['source'] and plan['pdf_sha256'] == source['sha256'] and plan['path'] == path and idx['path'] == mp, 'archive_source_path_mismatch')
    commit, index_commit = rb['commit'], idx['commit']
    git.changed(path, commit)
    git.changed(mp, index_commit)
    git.ancestor(commit, index_commit)
    git.ancestor(index_commit, git.head)
    historic = git.read(path, commit)
    current = git.read(path)
    indexed = git.read(mp, index_commit)
    live_manifest = yaml.load(git.read(mp), Loader=Strict)
    historical_manifest = yaml.load(indexed, Loader=Strict)
    require(historic == current == a['journal/candidate.yml'] and indexed == b['journal/indexed-manifest.yml'], 'archive_exact_git_bytes_mismatch')
    key = idx['registration_key']
    require(exact(live_manifest[key], historical_manifest[key]), 'archive_live_registration_changed')
    for k, v in {'id': source['id'], 'source_pdf_sha256': source['sha256'], 'edition': source['edition'], 'catalog_number': source['catalog'], 'publisher': source['publisher']}.items():
        require(live_manifest[k] == v and historical_manifest[k] == v, 'archive_manifest_identity_mismatch:' + k)
    att = load_json(att_raw)
    expected = {'protocol': 'sr3-expanded-editorial-binding/v1', 'source': source['id'],
                'source_sha256': source['sha256'], 'edition': source['edition'],
                'publisher': source['publisher'], 'catalog': source['catalog'],
                'path': path, 'record_id': record['id'], 'printed_pages': record['printed_pages'],
                'pdf_pages': record['pdf_pages'], 'reviewed_edition_scope': record['edition_scope'],
                'content_class': record['content_class'], 'baseline_sha256': sha(a['journal/baseline.yml']),
                'candidate_sha256': sha(current), 'historical_review_sha256': sha(a['source-review.txt']),
                'pre_sha256': sha(pre), 'post_sha256': sha(post), 'semantic_commit': commit,
                'index_commit': index_commit, 'baseline_reviewed_independently': True,
                'candidate_reviewed_independently': True, 'nested_text_reviewed': True,
                'historical_custody_and_chronology_reviewed': True}
    require(all(k in att and exact(att[k], v) for k, v in expected.items()), 'archive_editorial_binding_mismatch')
    require(isinstance(att['reviewer'], str) and att['reviewer'].strip() and att['reviewer'] not in (inventory_reviewer, custodian) and isinstance(att['original_review_locator'], str) and att['original_review_locator'].strip(), 'archive_independent_attestation_required')
    with tempfile.TemporaryDirectory() as d:
        t = Path(d)
        for n in ('ingestion_gate.py', 'connector_preflight.py'):
            (t / n).write_bytes(git.read('tools/ingestion/' + n))
        diagnostic = inspect(pre, post, transaction['pre_sha256'], transaction['post_sha256'], t/'ingestion_gate.py', blob(historic), blob(current), blob(indexed))
    require(diagnostic['journal_consistency'] == 'consistent_stored_evidence' and diagnostic['present_day_prepare_rechecked'] is True and diagnostic['present_day_confirm_rechecked'] is True, 'archive_gate_recheck_failed')
    return record, {'status': 'consistent_bound_evidence', 'layout': LAYOUT,
                    'attestation_sha256': sha(att_raw), 'historical_review_sha256': sha(a['source-review.txt']),
                    'semantic_commit': commit, 'semantic_blob': blob(current), 'index_commit': index_commit,
                    'index_blob': blob(indexed), 'registration_key': key,
                    'present_day_prepare_rechecked': True, 'present_day_confirm_rechecked': True,
                    'formal_acceptance': False}
