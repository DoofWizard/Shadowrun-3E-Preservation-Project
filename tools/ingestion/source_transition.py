#!/usr/bin/env python3
"""Offline FASA7115 -> FASA7215 provisional transition, never source completion.

Keep LoneStar.yml byte-for-byte and archive the outgoing checkpoint. Publish the
archive, next manifest and authorization with ordinary GitHub contents actions;
confirm their exact readbacks before publishing the checkpoint LAST. No semantic
receipt is generated and no existing prepare/confirm/authorize gate is changed.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import yaml
from lone_star_p4_deferral import check_active, SOURCE, PDF_SHA, GAP
from transaction_recovery import parse_yaml, state, git_blob, require, HEX40

TARGET = 'source.fasa-7215'
TARGET_SHA = '6d7e2f400eefd2c1edb99babe4cb7ed1ec3237be00c3c5423fc9428a23afc636'
MANIFEST = 'sources/manifests/TargetSmugglerHavens.yml'
ARCHIVE = 'sources/transitions/FASA7115-to-FASA7215.checkpoint-before.yml'
RECEIPT = 'sources/transitions/FASA7115-to-FASA7215.yml'
OLD_MANIFEST = 'sources/manifests/LoneStar.yml'
OLD_BLOB = 'fcdf013acc415b4443c8691d9b10a362d8ff8249'
OLD_CHECKPOINT_BLOB = 'af15219f0bc1464d562a52737a033bfab31a81c8'
PROTOCOL = 'sr3-provisional-source-transition/v1'
APPROVAL = 'owner_request_2026_10_30_FASA7115_p4_deferred_manual_review'
OBLIGATION = {'id': GAP, 'source': SOURCE, 'printed_page': 4,
              'physical_pdf_page': None, 'status': 'unverified_deferred_manual_review',
              'manually_verified': False, 'presumed_blank': False,
              'manual_verification_required': True, 'source_completion_blocked': True,
              'source_manifest': OLD_MANIFEST}


def dump(value):
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=True).encode('utf-8')


def authorize(manifest_raw, checkpoint_raw, target_raw, observed_target_sha):
    """Bind this one owner-approved transition to the verified outgoing state.

    These pins deliberately fail closed if another worker changes the source or
    checkpoint. A new state needs reconciliation, not a broader exception.
    """
    m, c, target = map(parse_yaml, (manifest_raw, checkpoint_raw, target_raw))
    state(m, c)
    check_active(m, c)
    require(git_blob(manifest_raw) == OLD_BLOB, 'outgoing_manifest_changed_reconcile')
    require(git_blob(checkpoint_raw) == OLD_CHECKPOINT_BLOB, 'stale_outgoing_checkpoint')
    require(m['done'] == {'p': 136, 'pdf': 144}
            and m['source_end'] == {'printed_page': 136, 'pdf_page': 144,
                                    'back_cover_pdf_page': 145}, 'source_end_not_reached')
    require(not m.get('pending') and not m.get('open_conflicts')
            and not c.get('pending_normalization') and not c.get('open_conflicts'),
            'unresolved_pending')
    require(c.get('next_sources', [])[:1] == [TARGET], 'wrong_successor')
    require(observed_target_sha == TARGET_SHA == target.get('source_pdf_sha256'),
            'fresh_successor_pdf_hash_mismatch')
    require(target.get('id') == TARGET and target.get('status') == 'ingesting'
            and c.get('source_status') == 'ingesting'
            and target.get('catalog_number') == 'FASA7215'
            and target.get('source_pdf_page_count') == 114, 'wrong_successor_manifest')
    require(target.get('done') == {'p': 0, 'pdf': 0}
            and target.get('next') == {'p': 2, 'pdf': 3}, 'successor_must_start_uncredited')
    require(target.get('records') == []
            and target.get('verified_ahead_of_contiguous_boundary') == []
            and target.get('pending') == [] and target.get('open_conflicts') == [],
            'successor_must_not_promote_forward_work')
    require(target.get('source_integrity', {}).get('visually_checked_mapping', {})
            .get('printed_2') == 3, 'successor_start_mapping_missing')
    require(target.get('transition_receipt') == RECEIPT, 'successor_transition_link_missing')
    return {'protocol': PROTOCOL, 'status': 'authorized_provisional_transition',
            'authorization': APPROVAL, 'from_source': SOURCE, 'to_source': TARGET,
            'outgoing_source_state': 'extraction_finished_manual_review_deferred',
            'source_complete': False, 'source_completion_allowed': False,
            'authorized_page_advance': 0, 'outgoing_done': m['done'],
            'outgoing_next': m['next'], 'outgoing_pdf_sha256': PDF_SHA,
            'outgoing_manifest_blob': git_blob(manifest_raw),
            'outgoing_checkpoint_blob': git_blob(checkpoint_raw),
            'outgoing_checkpoint_archive': ARCHIVE,
            'successor_manifest': MANIFEST, 'successor_manifest_blob': git_blob(target_raw),
            'successor_pdf_sha256': observed_target_sha,
            'verified_forward_entries_preserved': len(m['verified_ahead_of_contiguous_boundary']),
            'manual_review_obligations': [copy.deepcopy(OBLIGATION)],
            'worker_policy': 'existing_single_hourly_worker_schedule_unchanged'}


def confirmed_readback(expected_raw, observation):
    require(isinstance(observation, dict)
            and bool(HEX40.fullmatch(str(observation.get('commit_sha', '')))),
            'commit_readback_required')
    require(observation.get('blob_sha') == git_blob(expected_raw), 'readback_blob_mismatch')
    require(observation.get('content_sha256') == hashlib.sha256(expected_raw).hexdigest(),
            'readback_bytes_mismatch')


def activate(manifest_raw, checkpoint_raw, target_raw, receipt_raw, readbacks):
    """Produce checkpoint only after all prerequisites have committed readbacks.

    readbacks is keyed by exact repo path; observations must come from fresh
    GitHub reads at the returned commits, never from a write response alone.
    The caller must re-read current main and use its checkpoint SHA for CAS.
    """
    receipt = parse_yaml(receipt_raw)
    expected = authorize(manifest_raw, checkpoint_raw, target_raw,
                         receipt.get('successor_pdf_sha256'))
    require(receipt == expected, 'transition_authorization_changed')
    payloads = {OLD_MANIFEST: manifest_raw, ARCHIVE: checkpoint_raw,
                MANIFEST: target_raw, RECEIPT: receipt_raw}
    require(set(readbacks) == set(payloads), 'incomplete_or_extra_readbacks')
    for path, raw in payloads.items():
        confirmed_readback(raw, readbacks[path])
    before = parse_yaml(checkpoint_raw)
    target = parse_yaml(target_raw)
    after = copy.deepcopy(before)
    after.update(active_source=TARGET, source_status='ingesting',
                 completed_through={'printed_page': 0, 'pdf_page': 0},
                 resume_at={'printed_page': 2, 'pdf_page': 3},
                 last_commit=readbacks[MANIFEST]['commit_sha'],
                 next_sources=before['next_sources'][1:])
    after['provisional_source_transition'] = {
        'receipt': RECEIPT, 'receipt_commit': readbacks[RECEIPT]['commit_sha'],
        'receipt_blob': git_blob(receipt_raw), 'outgoing_checkpoint_archive': ARCHIVE,
        'outgoing_checkpoint_blob': git_blob(checkpoint_raw)}
    after['manual_review_obligations'] = copy.deepcopy(receipt['manual_review_obligations'])
    state(target, after)
    return dump(after)


def audit(manifest_raw, archive_raw, target_raw, receipt_raw, checkpoint_raw):
    """Startup audit; accepts ordinary successor progress without losing p4 debt."""
    receipt, c, target = map(parse_yaml, (receipt_raw, checkpoint_raw, target_raw))
    require(receipt.get('protocol') == PROTOCOL
            and receipt.get('status') == 'authorized_provisional_transition'
            and receipt.get('authorization') == APPROVAL
            and receipt.get('from_source') == SOURCE and receipt.get('to_source') == TARGET,
            'invalid_transition_receipt')
    require(receipt.get('source_complete') is False
            and receipt.get('source_completion_allowed') is False
            and receipt.get('authorized_page_advance') == 0, 'false_completion_claim')
    require(git_blob(manifest_raw) == receipt.get('outgoing_manifest_blob') == OLD_BLOB
            and git_blob(archive_raw) == receipt.get('outgoing_checkpoint_blob') == OLD_CHECKPOINT_BLOB,
            'outgoing_evidence_changed')
    state(parse_yaml(manifest_raw), parse_yaml(archive_raw))
    check_active(parse_yaml(manifest_raw), parse_yaml(archive_raw))
    link = c.get('provisional_source_transition', {})
    require(link.get('receipt') == RECEIPT and link.get('receipt_blob') == git_blob(receipt_raw)
            and bool(HEX40.fullmatch(str(link.get('receipt_commit', ''))))
            and link.get('outgoing_checkpoint_archive') == ARCHIVE
            and link.get('outgoing_checkpoint_blob') == OLD_CHECKPOINT_BLOB,
            'checkpoint_transition_link_changed')
    require(c.get('manual_review_obligations') == receipt.get('manual_review_obligations')
            == [OBLIGATION], 'manual_review_obligation_changed')
    require(target.get('id') == TARGET and target.get('status') == 'ingesting'
            and target.get('source_pdf_sha256') == TARGET_SHA
            and target.get('transition_receipt') == RECEIPT
            and c.get('source_status') == 'ingesting', 'wrong_active_successor')
    state(target, c)
    return {'status': 'consistent_provisional_transition', 'active_source': TARGET,
            'source_complete': False, 'deferred_unverified_page': 4,
            'manual_review_required': True, 'new_pages_from_transition': 0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['authorize', 'activate', 'audit'])
    p.add_argument('manifest', type=Path)
    p.add_argument('outgoing_checkpoint', type=Path)
    p.add_argument('successor_manifest', type=Path)
    p.add_argument('receipt', type=Path)
    p.add_argument('--fresh-successor-pdf', type=Path)
    p.add_argument('--readbacks', type=Path)
    p.add_argument('--checkpoint', type=Path)
    a = p.parse_args()
    try:
        args = [x.read_bytes() for x in (a.manifest, a.outgoing_checkpoint, a.successor_manifest)]
        if a.mode == 'authorize':
            require(a.fresh_successor_pdf is not None, 'fresh_successor_pdf_required')
            result = authorize(*args, hashlib.sha256(a.fresh_successor_pdf.read_bytes()).hexdigest())
            with a.receipt.open('xb') as dest:
                dest.write(dump(result))
        elif a.mode == 'activate':
            require(a.readbacks is not None and a.checkpoint is not None, 'activation_inputs_required')
            raw = activate(*args, a.receipt.read_bytes(), json.loads(a.readbacks.read_text()))
            with a.checkpoint.open('xb') as dest:
                dest.write(raw)
            result = {'status': 'checkpoint_proposed', 'blob': git_blob(raw),
                      'next': 'ordinary_checkpoint_update_then_fresh_readback_and_audit'}
        else:
            require(a.checkpoint is not None, 'active_checkpoint_required')
            result = audit(*args, a.receipt.read_bytes(), a.checkpoint.read_bytes())
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as exc:
        print(json.dumps({'status': 'blocked', 'reason': str(exc)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
