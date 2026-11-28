"""Synthetic regression for the exact archived Alter Pressure receipt schema."""
import base64
import json
import unittest
from inline_index_receipt import blob, digest, verify, verify_bytes


def artifact(raw):
    return {'bytes_base64': base64.b64encode(raw).decode(), 'sha256': digest(raw),
            'original_locator': 'SYNTHETIC fixture'}


class WastelandsInlineReceiptTests(unittest.TestCase):
    def setUp(self):
        self.path = 'sources/manifests/TargetWastelands.yml'
        self.snapshot, self.parent = b'new manifest\n', b'old manifest\n'
        self.confirm = dict(protocol='sr3-gate/v1', status='verified',
                            source='source.fanpro-10653',
                            pdf_sha256='31db497dcbe649eda35b596ed2dff9475241518027137c65f35ea720b03d0c6b',
                            record_id='entity.spell.alter-pressure', commit_sha='a'*40,
                            readback_blob_sha='b'*40, expected_blob_sha='b'*40)
        self.receipt = dict(source=self.confirm['source'], record_id=self.confirm['record_id'],
                            index_commit='c'*40, manifest_blob_sha=blob(self.snapshot),
                            previous_manifest_blob_sha=blob(self.parent),
                            readback_commit_and_main_blob_match=True,
                            semantic_commit=self.confirm['commit_sha'])

    def check(self):
        return verify_bytes(json.dumps(self.receipt).encode(), self.snapshot, self.path,
                            'c'*40, blob(self.snapshot), blob(self.parent), confirm=self.confirm)

    def test_positive(self):
        result = self.check()
        self.assertEqual(result['schema'], 'wastelands-alter-pressure-index-receipt/v1')
        self.assertTrue(result['receipt_prior_blob_checked'])
        self.assertFalse(result['formal_acceptance'])

    def test_each_receipt_field_required(self):
        for key in self.receipt.copy():
            with self.subTest(key=key):
                val = self.receipt.pop(key)
                with self.assertRaises(ValueError):
                    self.check()
                self.receipt[key] = val

    def test_conflicting_alias(self):
        self.receipt['blob_sha'] = 'f'*40
        with self.assertRaises(ValueError):
            self.check()

    def test_non_boolean_readback(self):
        for value in (False, 1, 'true', None):
            self.receipt['readback_commit_and_main_blob_match'] = value
            with self.assertRaises(ValueError):
                self.check()

    def test_wrong_pins_and_source(self):
        for key, value in (('source', 'source.cc'), ('record_id', 'entity.other'),
                           ('semantic_commit', 'f'*40), ('previous_manifest_blob_sha', 'f'*40),
                           ('manifest_blob_sha', 'f'*40), ('index_commit', 'f'*40)):
            original = self.receipt[key]
            self.receipt[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check()
            self.receipt[key] = original

    def test_wrong_confirm(self):
        for key, value in (('protocol', 'other'), ('status', 'preflighted'),
                           ('pdf_sha256', 'f'*64), ('readback_blob_sha', 'f'*40),
                           ('expected_blob_sha', 'f'*40), ('commit_sha', 'short')):
            original = self.confirm[key]
            self.confirm[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check()
            self.confirm[key] = original

    def test_wrong_manifest_and_polar_no_attestation(self):
        self.path = 'sources/manifests/Other.yml'
        with self.assertRaises(ValueError):
            self.check()
        self.path = 'sources/manifests/TargetWastelands.yml'
        self.receipt = dict(record_id=self.confirm['record_id'], semantic_commit='a'*40,
                            semantic_blob='b'*40, manifest_path=self.path,
                            previous_manifest_blob=blob(self.parent), index_commit='c'*40,
                            manifest_blob=blob(self.snapshot), status='verified', global_pages_advanced=0)
        with self.assertRaises(ValueError):
            self.check()

    def test_production_adapter(self):
        outer = self

        class FixtureGit:
            def read(self, path, ref):
                if path != outer.path:
                    raise AssertionError(path)
                return {'c'*40: outer.snapshot, 'd'*40: outer.parent}[ref]

        tx = dict(index_commit='c'*40, confirm=self.confirm,
                  historical_index_receipt_artifact=artifact(json.dumps(self.receipt).encode()),
                  historical_index_snapshot_artifact=artifact(self.snapshot))
        transition = dict(index_commit='c'*40, index_parent='d'*40,
                          status='new_or_changed_verified_registration')
        self.assertTrue(verify(FixtureGit(), self.path, tx, transition)['receipt_prior_blob_checked'])
        tx['historical_index_snapshot_artifact'] = artifact(b'tampered')
        with self.assertRaises(ValueError):
            verify(FixtureGit(), self.path, tx, transition)


if __name__ == '__main__':
    unittest.main()
