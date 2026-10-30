"""Regression tests for the one owner-authorized transition and preserved gates."""
import copy
import hashlib
from pathlib import Path
import unittest
from ingestion_gate import authorize_advance, InvalidRecord
from transaction_recovery import RecoveryError, parse_yaml, git_blob
import source_transition as t

ROOT = Path(__file__).resolve().parents[2]


class TransitionTests(unittest.TestCase):
    def setUp(self):
        self.old = (ROOT / t.OLD_MANIFEST).read_bytes()
        self.before = (ROOT / t.ARCHIVE).read_bytes()
        target = parse_yaml((ROOT / t.MANIFEST).read_bytes())
        # Later normal worker progress must not turn this regression fixture into
        # a request to reset production. Reset only this in-memory test input.
        target.update(status='ingesting', done={'p': 0, 'pdf': 0}, next={'p': 2, 'pdf': 3},
                      records=[], verified_ahead_of_contiguous_boundary=[],
                      pending=[], open_conflicts=[])
        self.target = t.dump(target)
        # The initial successor manifest is a fixture for this one-time gate.
        # No synthetic test receipt is published or used for actual progress.
        self.receipt = t.dump(t.authorize(self.old, self.before, self.target, t.TARGET_SHA))
        self.payloads = {t.OLD_MANIFEST: self.old, t.ARCHIVE: self.before,
                         t.MANIFEST: self.target, t.RECEIPT: self.receipt}
        self.readbacks = {p: {'commit_sha': 'a' * 40, 'blob_sha': git_blob(raw),
                             'content_sha256': hashlib.sha256(raw).hexdigest()}
                          for p, raw in self.payloads.items()}

    def activate(self, **kwargs):
        args = dict(manifest_raw=self.old, checkpoint_raw=self.before,
                    target_raw=self.target, receipt_raw=self.receipt, readbacks=self.readbacks)
        args.update(kwargs)
        return t.activate(**args)

    def test_zero_credit_and_preserved_old_state(self):
        old = self.old
        cp = self.activate()
        result = t.audit(self.old, self.before, self.target, self.receipt, cp)
        self.assertFalse(result['source_complete'])
        self.assertEqual(result['new_pages_from_transition'], 0)
        self.assertEqual(parse_yaml(cp)['completed_through'], {'printed_page': 0, 'pdf_page': 0})
        self.assertEqual(self.old, old)
        self.assertEqual(len(parse_yaml(old)['verified_ahead_of_contiguous_boundary']), 163)
        self.assertEqual(parse_yaml(self.before)['active_source'], t.SOURCE)
        self.assertEqual(parse_yaml(cp)['manual_review_obligations'], [t.OBLIGATION])

    def test_wrong_pdf(self):
        with self.assertRaisesRegex(ValueError, 'pdf_hash_mismatch'):
            t.authorize(self.old, self.before, self.target, 'f' * 64)

    def test_all_outgoing_changes_fail_closed(self):
        for key, value in [('done', {'p': 135, 'pdf': 143}), ('status', 'complete'),
                           ('pending', [{'id': 'new-pending'}]), ('open_conflicts', ['new-conflict']),
                           ('source_pdf_sha256', 'f' * 64), ('records', []),
                           ('verified_ahead_of_contiguous_boundary', [])]:
            with self.subTest(key=key):
                data = parse_yaml(self.old); data[key] = value
                with self.assertRaises(ValueError):
                    t.authorize(t.dump(data), self.before, self.target, t.TARGET_SHA)

    def test_deferral_cannot_be_relaxed_or_removed(self):
        for key, value in [('manually_verified', True), ('presumed_blank', True),
                           ('user_instruction', 'skip_forever'),
                           ('authorizes_synthetic_semantic_record', True)]:
            with self.subTest(key=key):
                m = parse_yaml(self.old)
                m['source_integrity']['unresolved_source_copy_gaps'][0][key] = value
                with self.assertRaises(ValueError):
                    t.authorize(t.dump(m), self.before, self.target, t.TARGET_SHA)
        m = parse_yaml(self.old); m['source_integrity']['unresolved_source_copy_gaps'] = []
        with self.assertRaises(ValueError):
            t.authorize(t.dump(m), self.before, self.target, t.TARGET_SHA)

    def test_stale_wrong_successor_or_conflicted_checkpoint(self):
        for key, value in [('next_sources', ['source.fasa-7214']),
                           ('last_commit', 'b' * 40), ('open_conflicts', ['conflict']),
                           ('pending_normalization', ['pending'])]:
            with self.subTest(key=key):
                cp = parse_yaml(self.before); cp[key] = value
                with self.assertRaises(ValueError):
                    t.authorize(self.old, t.dump(cp), self.target, t.TARGET_SHA)

    def test_no_forward_promotion_in_seed(self):
        for key, value in [('records', [['forward', 'a' * 40]]),
                           ('verified_ahead_of_contiguous_boundary', [{'gate': 'verified'}]),
                           ('done', {'p': 110, 'pdf': 111}), ('status', 'complete'),
                           ('id', 'source.fasa-7214'), ('next', {'p': 4, 'pdf': 5}),
                           ('pending', [{'id': 'pending'}])]:
            with self.subTest(key=key):
                target = parse_yaml(self.target); target[key] = value
                with self.assertRaises(ValueError):
                    t.authorize(self.old, self.before, t.dump(target), t.TARGET_SHA)

    def test_each_readback_is_required(self):
        for path in self.payloads:
            with self.subTest(path=path):
                readbacks = copy.deepcopy(self.readbacks); del readbacks[path]
                with self.assertRaisesRegex(ValueError, 'readbacks'):
                    self.activate(readbacks=readbacks)

    def test_readback_requires_commit_blob_and_exact_bytes(self):
        for path in self.payloads:
            for key, value in [('commit_sha', None), ('blob_sha', 'f' * 40),
                               ('content_sha256', 'f' * 64)]:
                with self.subTest(path=path, key=key):
                    readbacks = copy.deepcopy(self.readbacks); readbacks[path][key] = value
                    with self.assertRaises(ValueError):
                        self.activate(readbacks=readbacks)

    def test_tampered_authorization_never_activates(self):
        for key, value in [('source_complete', True), ('source_completion_allowed', True),
                           ('authorized_page_advance', 1), ('manual_review_obligations', [])]:
            with self.subTest(key=key):
                receipt = parse_yaml(self.receipt); receipt[key] = value
                with self.assertRaisesRegex(ValueError, 'authorization_changed'):
                    self.activate(receipt_raw=t.dump(receipt))

    def test_rerun_cannot_reset_active_progress(self):
        with self.assertRaises(ValueError):
            t.authorize(self.old, self.activate(), self.target, t.TARGET_SHA)

    def test_audit_rejects_lost_obligation_link_or_archived_checkpoint(self):
        for key, value in [('manual_review_obligations', []), ('provisional_source_transition', {}),
                           ('completed_through', {'printed_page': 3, 'pdf_page': 4})]:
            with self.subTest(key=key):
                cp = parse_yaml(self.activate()); cp[key] = value
                with self.assertRaises(ValueError):
                    t.audit(self.old, self.before, self.target, self.receipt, t.dump(cp))
        with self.assertRaises(ValueError):
            t.audit(self.old, self.before + b'\n', self.target, self.receipt, self.activate())

    def test_successor_continues_only_through_existing_gate(self):
        m, c = parse_yaml(self.target), parse_yaml(self.activate())
        with self.assertRaisesRegex(InvalidRecord, 'no_verified_records'):
            authorize_advance(m, c, [], 2, 3, 4, 5)
        # Unit-test fixture only: demonstrate unchanged numeric page coverage gate.
        r = {'protocol': 'sr3-gate/v1', 'status': 'verified', 'source': t.TARGET,
             'printed_pages': '2-3', 'pdf_pages': '3-4', 'commit_sha': 'a' * 40,
             'readback_blob_sha': 'b' * 40, 'expected_blob_sha': 'b' * 40,
             'path': 'references/test-only/contents.yml'}
        self.assertTrue(authorize_advance(m, c, [r], 2, 3, 4, 5)['authorized'])
        m['done'] = {'p': 3, 'pdf': 4}; m['next'] = {'p': 4, 'pdf': 5}
        c['completed_through'] = {'printed_page': 3, 'pdf_page': 4}
        c['resume_at'] = {'printed_page': 4, 'pdf_page': 5}
        self.assertEqual(t.audit(self.old, self.before, t.dump(m), self.receipt, t.dump(c))['status'],
                         'consistent_provisional_transition')

    def test_duplicate_yaml_keys_fail_closed(self):
        with self.assertRaisesRegex(RecoveryError, 'yaml_duplicate_key'):
            t.authorize(self.old, self.before, self.target + b'\nstatus: complete\n', t.TARGET_SHA)

    def test_live_transition_when_successor_is_active(self):
        cp = (ROOT / 'WORKER_CHECKPOINT.yml').read_bytes()
        if parse_yaml(cp).get('active_source') != t.TARGET:
            self.skipTest('successor is not the current active source')
        result = t.audit(self.old, self.before, (ROOT / t.MANIFEST).read_bytes(),
                         (ROOT / t.RECEIPT).read_bytes(), cp)
        self.assertEqual(result['status'], 'consistent_provisional_transition')


if __name__ == '__main__':
    unittest.main()
