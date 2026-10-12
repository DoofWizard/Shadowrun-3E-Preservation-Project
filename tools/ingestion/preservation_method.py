#!/usr/bin/env python3
"""Offline, source-fidelity-first submission preparation and failure triage.

Never connects to GitHub, edits protected facts, guesses filter triggers, or
retries a denied submission. A source reviewer must independently verify the
baseline against the actual catalogued PDF before using this program.

All GitHub writes remain ordinary create_file/update_file actions; the existing
transaction_recovery.stage, ingestion_gate.confirm, and authorize steps remain
mandatory. This module is an aid to those gates, never a substitute for them.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import yaml
from connector_preflight import (InvalidRecord, PROTECTED, load_text,
                                 validate_pair, validate_shape)

HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')

class MethodError(ValueError):
    pass

def require(ok: bool, reason: str) -> None:
    if not ok:
        raise MethodError(reason)

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def git_blob(raw: bytes) -> str:
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()

def fresh_write(path: Path, raw: bytes) -> None:
    """Never overwrite a baseline, staged candidate, or recovery receipt."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as dest:
        dest.write(raw)

def initial_candidate(baseline: dict) -> dict:
    """Create an initial archival envelope without changing ANY source fields.

    Existing human-authored headlines/summaries are not removed. For records
    with no presentation text, add metadata-only index text; all meaningful
    source assertions must already be in the frozen `data` field.
    """
    kind = validate_shape(baseline, candidate=False)
    candidate = copy.deepcopy(baseline)
    candidate['framing'] = 'reference_exact' if kind in PROTECTED else 'newsroom_neutral'
    candidate.setdefault('headline', f"{baseline['id']} — archival {kind} record")
    candidate.setdefault('summary',
                         f"Source-indexed {kind} from {baseline['source']}, "
                         f"printed pages {baseline['printed_pages']}; "
                         'substantive assertions and provenance are in the structured data.')
    validate_pair(baseline, candidate)
    return candidate

def compose(baseline_path: Path, candidate_path: Path) -> dict:
    baseline = load_text(baseline_path.read_text(encoding='utf-8'))
    candidate = initial_candidate(baseline)
    # Dump only the candidate; the independently authored baseline is never edited.
    raw = yaml.safe_dump(candidate, allow_unicode=True, sort_keys=False).encode('utf-8')
    validate_pair(baseline, load_text(raw.decode('utf-8')))
    fresh_write(candidate_path, raw)
    return {'status': 'composed_initial', 'path': str(candidate_path),
            'record_id': candidate['id'], 'class': candidate['content_class'][0],
            'candidate_sha256': digest(raw), 'source_review': 'required_independently',
            'next': 'transaction_recovery.stage_and_gate_prepare'}

def load_stage(journal: Path) -> tuple[dict, dict]:
    """Validate the locally preserved preparation plan against exact bytes."""
    try:
        plan = json.loads((journal / 'plan.json').read_text(encoding='utf-8'))
        baseline_raw = (journal / 'baseline.yml').read_bytes()
        candidate_raw = (journal / 'candidate.yml').read_bytes()
    except (ValueError, OSError, UnicodeError) as exc:
        raise MethodError('missing_or_invalid_journal') from exc
    require(plan.get('protocol') == 'sr3-gate/v1' and
            plan.get('status') == 'preflighted', 'journal_missing_actual_prepare_gate')
    require(digest(candidate_raw) == plan.get('candidate_sha256') and
            git_blob(candidate_raw) == plan.get('expected_blob_sha'),
            'staged_candidate_bytes_changed')
    require(bool(HEX64.fullmatch(str(plan.get('pdf_sha256', '')))),
            'missing_source_pdf_hash')
    baseline = load_text(baseline_raw.decode('utf-8'))
    candidate = load_text(candidate_raw.decode('utf-8'))
    checked = validate_pair(baseline, candidate)
    for field, value in [('source', candidate['source']),
                         ('record_id', candidate['id']),
                         ('printed_pages', candidate['printed_pages']),
                         ('pdf_pages', candidate['pdf_pages'])]:
        require(plan.get(field) == value, 'staged_plan_provenance_mismatch')
    require(checked['immutable_sha256'] == plan.get('immutable_sha256'),
            'staged_immutable_digest_mismatch')
    return plan, candidate

def error_log(journal: Path) -> list[dict]:
    path = journal / 'write_attempts.json'
    if not path.exists():
        return []
    try:
        result = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise MethodError('invalid_write_attempt_log') from exc
    require(type(result) is list and all(type(x) is dict for x in result),
            'invalid_write_attempt_log')
    return result

def record_failure(journal: Path, operation: str, diagnostic: str,
                   http_status: int | None, explicit: bool) -> dict:
    from transaction_recovery import classify_failure  # existing evidence classifier
    plan, _ = load_stage(journal)
    require(operation in ('create', 'update'), 'semantic_operation_only_use_recovery_tool_for_admin')
    require(type(diagnostic) is str and diagnostic.strip(), 'missing_observed_error')
    if http_status is not None:
        require(type(http_status) is int and 100 <= http_status <= 599,
                'invalid_http_status')
    classification = classify_failure(operation, diagnostic, http_status, explicit)
    attempts = error_log(journal)
    require(all(x.get('candidate_sha256') == plan['candidate_sha256'] for x in attempts),
            'attempt_log_candidate_mismatch')
    entry = {'operation': operation, 'candidate_sha256': plan['candidate_sha256'],
             'category': classification['category'],
             'github_http_status': http_status,
             'explicit_restriction': explicit,
             'observed_error': diagnostic[:512],
             'observed_error_sha256': digest(diagnostic.encode('utf-8'))}
    # Idempotent recording; never generate unlimited repeat-log noise.
    if entry not in attempts:
        require(len(attempts) < 32, 'attempt_log_full_defer_for_review')
        attempts.append(entry)
        target = journal / 'write_attempts.json'
        temp = journal / 'write_attempts.json.tmp'
        require(not temp.exists(), 'incomplete_attempt_log_write')
        try:
            fresh_write(temp, (json.dumps(attempts, indent=2, sort_keys=True) + '\n').encode())
            temp.replace(target)
        finally:
            if temp.exists():
                temp.unlink()
    return {'status': 'observed_failure_logged', 'path': plan['path'],
            'category': classification['category'], 'github_http_status': http_status,
            'attempts': len(attempts), 'cause_proved': classification['cause_proved']}

def decide(journal: Path, *, remote_absent: bool = False,
           observed_blob: str | None = None,
           commit_sha: str | None = None) -> dict:
    """Make a *non-executing* recommendation from real recorded evidence.

    Remote observations must come from fresh ordinary GitHub readback; an omitted
    observation is UNKNOWN, not proof that a file does not exist.
    """
    plan, _ = load_stage(journal)
    attempts = error_log(journal)
    require(all(x.get('candidate_sha256') == plan['candidate_sha256'] for x in attempts),
            'attempt_log_candidate_mismatch')
    require(not (remote_absent and observed_blob is not None), 'conflicting_remote_evidence')
    require(commit_sha is None or bool(HEX40.fullmatch(commit_sha)), 'invalid_commit_sha')
    require(observed_blob is None or bool(HEX40.fullmatch(observed_blob)), 'invalid_remote_blob')
    require(not (commit_sha and observed_blob is None), 'commit_without_blob')
    base = {'protocol': 'sr3-preservation-method/v1', 'record_path': plan['path'],
            'candidate_sha256': plan['candidate_sha256'],
            'last_observed_category': attempts[-1]['category'] if attempts else None,
            'candidate_source_review': 'required_independently',
            'authorized_page_advance': False}
    if observed_blob is not None:
        if observed_blob != plan['expected_blob_sha']:
            return {**base, 'decision': 'divergent_remote_blob_investigate_no_overwrite'}
        if commit_sha is None:
            return {**base, 'decision': 'matching_remote_blob_resolve_actual_commit'}
        return {**base, 'decision': 'run_actual_ingestion_gate_confirm',
                'observed_blob_sha': observed_blob, 'commit_sha': commit_sha}
    if not remote_absent:
        return {**base, 'decision': 'fresh_readback_required'}
    if any(x.get('explicit_restriction') or
           x.get('category') == 'explicit_restriction' for x in attempts):
        return {**base, 'decision': 'stop_preserve_pending_explicit_restriction'}
    if not attempts:
        return {**base, 'decision': 'first_normal_github_contents_write_permitted'}
    last = attempts[-1]['category']
    if last in ('ambiguous_tool_layer_rejection', 'unclassified'):
        return {**base, 'decision': 'defer_identical_payload_review_actual_error_and_source'}
    if last == 'stale_sha':
        return {**base, 'decision': 'refresh_current_sha_then_normal_update'}
    if last == 'transient_provider_error':
        return {**base, 'decision': 'check_provider_state_and_permitted_normal_retry'}
    if last == 'provider_denial':
        return {**base, 'decision': 'check_permissions_no_alternate_api'}
    return {**base, 'decision': 'defer_pending_review'}

def verify_source_pdf(pdf_path: Path, manifest_path: Path) -> dict:
    """Verify bytes against the LIVE manifest after a fresh Drive acquisition.

    This is a hash check only, NOT an image, page-map or extraction review.
    """
    manifest = load_text(manifest_path.read_text(encoding='utf-8'))
    expected = manifest.get('source_pdf_sha256')
    require(isinstance(expected,str) and bool(HEX64.fullmatch(expected)),
            'manifest_source_pdf_hash_missing')
    with pdf_path.open('rb') as source_file:
        observed = hashlib.file_digest(source_file, 'sha256').hexdigest()
    require(observed == expected, 'fresh_source_pdf_sha256_mismatch')
    return {'status':'source_pdf_hash_verified', 'source':manifest.get('id'),
            'sha256': observed, 'page_images_review': 'still_required_independently'}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    p = sub.add_parser('verify-source')
    p.add_argument('fresh_pdf', type=Path)
    p.add_argument('live_manifest', type=Path)
    p = sub.add_parser('compose-first')
    p.add_argument('baseline', type=Path); p.add_argument('candidate', type=Path)
    p = sub.add_parser('log-failure')
    p.add_argument('journal', type=Path)
    p.add_argument('operation', choices=('create', 'update'))
    p.add_argument('diagnostic')
    p.add_argument('--http-status', type=int)
    p.add_argument('--explicit-restriction', action='store_true')
    p = sub.add_parser('decide')
    p.add_argument('journal', type=Path)
    p.add_argument('--remote-absent', action='store_true')
    p.add_argument('--observed-blob')
    p.add_argument('--commit-sha')
    args = parser.parse_args()
    try:
        if args.mode == 'verify-source':
            result = verify_source_pdf(args.fresh_pdf,args.live_manifest)
        elif args.mode == 'compose-first':
            result = compose(args.baseline, args.candidate)
        elif args.mode == 'log-failure':
            result = record_failure(args.journal, args.operation, args.diagnostic,
                                    args.http_status, args.explicit_restriction)
        else:
            result = decide(args.journal, remote_absent=args.remote_absent,
                            observed_blob=args.observed_blob, commit_sha=args.commit_sha)
    except (MethodError, InvalidRecord, OSError, UnicodeError, ValueError, KeyError) as exc:
        print(json.dumps({'status': 'blocked', 'reason': str(exc) if isinstance(exc, (MethodError, InvalidRecord)) else type(exc).__name__}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == '__main__':
    sys.exit(main())