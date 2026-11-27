"""Synthetic regression tests only; historical diagnostics run separately."""
import base64
import json
import unittest

from inline_index_receipt import blob, digest, verify, verify_bytes


class FixtureGit:
    def read(self, path, ref):
        return {'a'*40: b'new manifest\n', 'b'*40: b'old manifest\n'}[ref]


def art(raw):
    return {'bytes_base64': base64.b64encode(raw).decode(), 'sha256': digest(raw),
            'original_locator': 'SYNTHETIC fixture'}


class InlineIndexTests(unittest.TestCase):
    def setUp(self):
        self.git = FixtureGit()
        self.path = 'sources/manifests/Rigger3Revised.yml'
        self.commit = 'a'*40
        self.snapshot = self.git.read(self.path, self.commit)
        self.receipt = {'commit_sha': self.commit, 'blob_sha': blob(self.snapshot),
                        'manifest_path': self.path, 'readback_exact': True,
                        'prior_blob_sha': blob(b'old manifest\n')}
        self.transition = {'status': 'new_or_changed_verified_registration',
                           'index_commit': self.commit, 'index_parent': 'b'*40,
                           'index_pointer': '/verified/0'}

    def transaction(self):
        return {'index_commit': self.commit,
                'historical_index_receipt_artifact': art(json.dumps(self.receipt).encode()),
                'historical_index_snapshot_artifact': art(self.snapshot)}

    def check(self):
        return verify(self.git, self.path, self.transaction(), self.transition)

    def test_positive(self):
        self.assertTrue(self.check()['receipt_prior_blob_checked'])
        self.assertFalse(self.check()['formal_acceptance'])

    def test_missing_artifacts(self):
        for k in ('historical_index_receipt_artifact', 'historical_index_snapshot_artifact'):
            t = self.transaction(); del t[k]
            with self.assertRaisesRegex(ValueError, 'inline_index_missing'):
                verify(self.git, self.path, t, self.transition)

    def test_altered_snapshot(self):
        self.snapshot += b'\n'
        with self.assertRaisesRegex(ValueError, 'snapshot_bytes_mismatch'):
            self.check()

    def test_receipt_mismatch(self):
        for k, v in [('commit_sha', 'c'*40), ('blob_sha', 'd'*40), ('manifest_path', 'sources/manifests/Other.yml')]:
            old = self.receipt[k]; self.receipt[k] = v
            with self.assertRaisesRegex(ValueError, 'identity_mismatch'):
                self.check()
            self.receipt[k] = old

    def test_readback_not_boolean_true(self):
        for v in (1, 'true', False):
            self.receipt['readback_exact'] = v
            with self.assertRaisesRegex(ValueError, 'readback_missing'):
                self.check()

    def test_prior_mismatch(self):
        self.receipt['prior_blob_sha'] = 'e'*40
        with self.assertRaisesRegex(ValueError, 'parent_blob_mismatch'):
            self.check()

    def test_conflicting_alias(self):
        self.receipt['commit'] = 'c'*40
        with self.assertRaisesRegex(ValueError, 'unknown_receipt_fields'):
            self.check()

    def test_duplicate_json(self):
        raw = json.dumps(self.receipt).encode().replace(b'{', b'{"commit_sha":"wrong",', 1)
        with self.assertRaisesRegex(ValueError, 'duplicate_receipt_key'):
            verify_bytes(raw, self.snapshot, self.path, self.commit, blob(self.snapshot))

    def test_unpinned_artifact(self):
        t = self.transaction(); t['historical_index_snapshot_artifact']['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'digest_mismatch'):
            verify(self.git, self.path, t, self.transition)

    def test_split_registration_pointer(self):
        self.receipt = {'commit': self.commit, 'blob': blob(self.snapshot), 'path': self.path,
                        'exact_commit_live_bytes': True, 'registration_key': 'correction~1'}
        with self.assertRaisesRegex(ValueError, 'pointer_mismatch'):
            self.check()
        self.transition['index_pointer'] = '/correction~01'
        self.assertEqual(self.check()['schema'], 'split-index-receipt/v1')

    def test_transition_required(self):
        self.transition['status'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'transition_required'):
            self.check()


if __name__ == '__main__':
    unittest.main()
