"""Synthetic regression fixtures for the observed Matrix index receipt schema."""
import base64
import json
import unittest

from inline_index_receipt import blob, digest, verify, verify_bytes


def artifact(raw):
    return {'bytes_base64': base64.b64encode(raw).decode(), 'sha256': digest(raw),
            'original_locator': 'SYNTHETIC fixture'}


class MatrixInlineReceiptTests(unittest.TestCase):
    def setUp(self):
        self.path = 'sources/manifests/Matrix.yml'
        self.snapshot = b'new synthetic manifest\n'
        self.parent = b'old synthetic manifest\n'
        self.receipt = {'path': self.path, 'commit': 'a'*40, 'blob': blob(self.snapshot),
                        'previous_blob': blob(self.parent), 'semantic_commit': 'b'*40,
                        'semantic_blob': 'c'*40, 'exact_commit_and_branch_readback': True,
                        'commit_sha': 'a'*40, 'blob_sha': blob(self.snapshot)}
        self.pins = {'semantic_commit': 'b'*40, 'semantic_blob': 'c'*40}

    def check(self):
        return verify_bytes(json.dumps(self.receipt).encode(), self.snapshot, self.path,
                            'a'*40, blob(self.snapshot), blob(self.parent), **self.pins)

    def test_positive(self):
        result = self.check()
        self.assertEqual(result['schema'], 'matrix-index-receipt/v1')
        self.assertTrue(result['receipt_prior_blob_checked'])
        self.assertFalse(result['formal_acceptance'])

    def test_conflicting_aliases(self):
        for key in ('commit_sha', 'blob_sha'):
            with self.subTest(key=key):
                original = self.receipt[key]
                self.receipt[key] = 'd'*40
                with self.assertRaisesRegex(ValueError, 'conflicting_aliases'):
                    self.check()
                self.receipt[key] = original

    def test_missing_or_extra_fields(self):
        self.receipt.pop('blob_sha')
        with self.assertRaisesRegex(ValueError, 'matrix_receipt_fields'):
            self.check()
        self.receipt['blob_sha'] = self.receipt['blob']
        self.receipt['unrecognized'] = True
        with self.assertRaisesRegex(ValueError, 'matrix_receipt_fields'):
            self.check()

    def test_semantic_mismatch(self):
        for key in ('semantic_commit', 'semantic_blob'):
            with self.subTest(key=key):
                original = self.receipt[key]
                self.receipt[key] = 'd'*40
                with self.assertRaisesRegex(ValueError, 'semantic_identity_mismatch'):
                    self.check()
                self.receipt[key] = original

    def test_missing_external_pins(self):
        for key in self.pins.copy():
            original = self.pins.pop(key)
            with self.assertRaisesRegex(ValueError, 'external_pins_required'):
                self.check()
            self.pins[key] = original

    def test_parent_mismatch(self):
        self.receipt['previous_blob'] = 'd'*40
        with self.assertRaisesRegex(ValueError, 'parent_blob_mismatch'):
            self.check()

    def test_non_boolean_readback(self):
        for value in (False, 1, 'true'):
            self.receipt['exact_commit_and_branch_readback'] = value
            with self.assertRaisesRegex(ValueError, 'readback_missing'):
                self.check()

    def test_wrong_source(self):
        self.path = 'sources/manifests/Other.yml'
        with self.assertRaisesRegex(ValueError, 'matrix_manifest_required'):
            self.check()

    def test_production_adapter(self):
        outer = self

        class FixtureGit:
            def read(self, path, ref):
                return {'a'*40: outer.snapshot, 'e'*40: outer.parent}[ref]

        tx = {'index_commit': 'a'*40,
              'historical_index_receipt_artifact': artifact(json.dumps(self.receipt).encode()),
              'historical_index_snapshot_artifact': artifact(self.snapshot),
              'confirm': {'status': 'verified', 'commit_sha': 'b'*40,
                          'readback_blob_sha': 'c'*40}}
        transition = {'status': 'new_or_changed_verified_registration',
                      'index_commit': 'a'*40, 'index_parent': 'e'*40,
                      'index_pointer': '/correction/verified_semantic_records/0'}
        self.assertEqual(verify(FixtureGit(), self.path, tx, transition)['schema'],
                         'matrix-index-receipt/v1')
        tx['confirm']['commit_sha'] = 'd'*40
        with self.assertRaisesRegex(ValueError, 'semantic_identity_mismatch'):
            verify(FixtureGit(), self.path, tx, transition)
        tx['confirm']['status'] = 'preflighted'
        with self.assertRaisesRegex(ValueError, 'verified_confirm_required'):
            verify(FixtureGit(), self.path, tx, transition)


if __name__ == '__main__':
    unittest.main()
