"""Read-only two-version proof for the observed M&M implant-effects correction.

Historical originals and independent successor adjudication are mandatory; a
present-day Git export or equal values alone cannot supply either artifact.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from binding_schema import mm_registration
from index_transition import verify as verify_transition, _registrations
from inline_index_receipt import verify as verify_index_artifacts
from source_index_receipts import MM, MM_SOURCE, MM_SHA, require

PATH = 'rules/cyberware/mm-implant-device-game-effects-p41-42.yml'


def verify_link(git, old, new, old_index, new_index, old_pointer, new_pointer, parse, ptr, blob):
    """Prove actual Git registration and predecessor path bytes, not custody."""
    require(old[:2] == new[:2] and old[1] == PATH and old[2] != new[2] and old[3] != new[3],
            'mm_successor_distinct_same_record_required')
    a = verify_transition(git, MM, old_index, old_pointer, old, parse, ptr, blob)
    b = verify_transition(git, MM, new_index, new_pointer, new, parse, ptr, blob)
    parents = git.run('rev-list', '--parents', '-n', '1', new[2]).decode().split()
    require(len(parents) == 2, 'mm_successor_single_semantic_parent_required')
    parent = parents[1]
    git.ancestor(old_index, parent)
    require(blob(git.read(PATH, parent)) == old[3], 'mm_successor_predecessor_bytes_mismatch')
    require(blob(git.read(PATH, a['index_parent'])) == old[3] and
            blob(git.read(PATH, b['index_parent'])) == new[3] and blob(git.read(PATH)) == new[3],
            'mm_successor_stale_index_or_head')
    prior = parse(git.read(MM, old_index))
    before = parse(git.read(MM, b['index_parent']))
    after = parse(git.read(MM, new_index))
    live = parse(git.read(MM))
    for tree, expected in ((prior, [old]), (before, [old]), (after, [old, new]), (live, [old, new])):
        found = sorted(i for i, status in _registrations(tree, new) if status == 'verified')
        require(found == sorted(expected), 'mm_successor_unaccounted_or_missing_registration')
    require(ptr(prior, old_pointer) == ptr(before, old_pointer) == ptr(after, old_pointer) == ptr(live, old_pointer),
            'mm_successor_predecessor_registration_changed')
    require(ptr(after, new_pointer) == ptr(live, new_pointer), 'mm_successor_current_registration_changed')
    return a, b, parent


def verify(git, source, current, reviewer, custodian, parse, ptr, blob, sha, encoded, artifact, pairs):
    require(source['id'] == MM_SOURCE and source['sha256'] == MM_SHA and source['manifest'] == MM,
            'mm_successor_source_identity_mismatch')
    require('predecessor_transaction' in current and 'successor_review_artifact' in current,
            'mm_successor_original_predecessor_and_review_required')
    prior = current['predecessor_transaction']
    require('layout' not in prior and 'predecessor_transaction' not in prior,
            'mm_successor_only_observed_two_versions_supported')
    plan, confirm = prior['plan'], prior['confirm']
    new = current['confirm']
    j = prior['prewrite_journal_artifact']
    baseline, candidate = artifact(j['baseline']), artifact(j['candidate'])
    rec = parse(candidate)
    require(rec['source'] == MM_SOURCE and rec['edition_scope'] == 'SR3' and rec['content_class'] == ['rule_exact'],
            'mm_successor_predecessor_record_identity_mismatch')
    require(json.loads(artifact(j['plan']), object_pairs_hook=pairs) == plan and
            json.loads(artifact(prior['historical_confirm_artifact']), object_pairs_hook=pairs) == confirm,
            'mm_successor_original_receipt_mismatch')
    require(sha(baseline) == prior['baseline_sha256'] and plan['protocol'] == 'sr3-gate/v1' and plan['status'] == 'preflighted',
            'mm_successor_original_prepare_required')
    frozen = lambda record: {k: v for k, v in record.items() if k not in {'headline', 'summary', 'framing'}}
    require(encoded(frozen(parse(baseline))) == encoded(frozen(rec)) and sha(encoded(frozen(rec))) == plan['immutable_sha256'],
            'mm_successor_immutable_mismatch')
    expected = {'record_id': rec['id'], 'path': PATH, 'source': MM_SOURCE, 'pdf_sha256': MM_SHA,
                'printed_pages': rec['printed_pages'], 'pdf_pages': rec['pdf_pages'],
                'candidate_sha256': sha(candidate), 'expected_blob_sha': blob(candidate)}
    require(all(plan[k] == v for k, v in expected.items()) and
            confirm == {**plan, 'status': 'verified', 'commit_sha': confirm['commit_sha'], 'readback_blob_sha': blob(candidate)},
            'mm_successor_original_confirm_mismatch')
    require(git.read(PATH, confirm['commit_sha']) == candidate and new['record_id'] == rec['id'] and new['path'] == PATH,
            'mm_successor_historical_candidate_mismatch')
    editorial = json.loads(artifact(prior['editorial_review_artifact']), object_pairs_hook=pairs)
    ed_expected = {'source': MM_SOURCE, 'source_sha256': MM_SHA, 'edition': 'SR3', 'publisher': source['publisher'],
                   'catalog': source['catalog'], 'path': PATH, 'candidate_sha256': sha(candidate),
                   'baseline_sha256': sha(baseline), 'baseline_reviewed_independently': True,
                   'candidate_reviewed_independently': True, 'nested_text_reviewed': True,
                   'printed_pages': rec['printed_pages'], 'pdf_pages': rec['pdf_pages'], 'reviewed_edition_scope': 'SR3'}
    require(all(k in editorial and type(editorial[k]) is type(v) and editorial[k] == v for k, v in ed_expected.items()),
            'mm_successor_original_editorial_binding_missing')
    old_identity = (rec['id'], PATH, confirm['commit_sha'], blob(candidate))
    new_identity = (rec['id'], PATH, new['commit_sha'], new['readback_blob_sha'])
    a, b, parent = verify_link(git, old_identity, new_identity, prior['index_commit'], current['index_commit'],
                              prior['index_pointer'], current['index_pointer'], parse, ptr, blob)
    historical = parse(git.read(MM, prior['index_commit']))
    mm_registration(source, rec, plan, confirm, sha(baseline), ptr(historical, prior['index_pointer']), prior['index_pointer'])
    original = verify_index_artifacts(git, MM, prior, a)
    att = json.loads(artifact(current['successor_review_artifact']), object_pairs_hook=pairs)
    expected = {'protocol': 'sr3-mm-successor-review/v1', 'source': MM_SOURCE, 'source_sha256': MM_SHA,
                'path': PATH, 'record_id': rec['id'], 'previous_semantic_commit': old_identity[2],
                'previous_semantic_blob': old_identity[3], 'previous_index_commit': prior['index_commit'],
                'current_semantic_commit': new_identity[2], 'current_semantic_blob': new_identity[3],
                'current_index_commit': current['index_commit'], 'all_changed_fields_reviewed': True,
                'same_edition_confirmed': True, 'current_controls': True}
    require(all(k in att and type(att[k]) is type(v) and att[k] == v for k, v in expected.items()) and
            isinstance(att.get('reviewer'), str) and att['reviewer'].strip() and att['reviewer'] not in (reviewer, custodian) and
            isinstance(att.get('original_review_locator'), str) and att['original_review_locator'].strip(),
            'mm_successor_independent_lineage_review_required')
    with tempfile.TemporaryDirectory() as directory:
        t = Path(directory)
        for name in ('ingestion_gate.py', 'connector_preflight.py'):
            (t/name).write_bytes(git.read('tools/ingestion/'+name))
        (t/'baseline.yml').write_bytes(baseline)
        (t/'candidate.yml').write_bytes(candidate)
        (t/'plan.json').write_bytes(encoded(plan))
        gate = str(t/'ingestion_gate.py')
        def call(*args):
            return json.loads(subprocess.check_output([sys.executable, gate, *map(str, args)]))
        require(call('prepare', t/'baseline.yml', t/'candidate.yml', PATH, MM_SOURCE, MM_SHA) == plan and
                call('confirm', t/'plan.json', t/'candidate.yml', confirm['commit_sha'], blob(candidate)) == confirm,
                'mm_successor_present_day_gate_recheck_mismatch')
    return {'status': 'consistent_reviewed_successor_chain', 'previous_semantic_commit': old_identity[2],
            'previous_index_commit': prior['index_commit'], 'current_semantic_commit': new_identity[2],
            'current_index_commit': current['index_commit'], 'current_semantic_parent': parent,
            'previous_index_artifacts': original, 'current_index_transition': b, 'formal_acceptance': False}
