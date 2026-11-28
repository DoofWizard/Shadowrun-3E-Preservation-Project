"""Synthetic tests for the source-local FanPro25003 compact index receipt."""
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes


class MJLBBInlineReceiptTests(unittest.TestCase):
    def setUp(self):
        self.path = 'sources/manifests/MrJohnsonsLittleBlackBook.yml'
        self.commit = 'a'*40
        self.confirm = {
            'protocol': 'sr3-gate/v1', 'status': 'verified',
            'source': 'source.fanpro-25003',
            'pdf_sha256': '2426699e60652473e1d1be3387c6baf45fa950d3b1ae05e8cfd07302bc34cd5d',
            'record_id': 'reference.mjlbb.synthetic',
            'path': 'references/campaign/mjlbb-synthetic.yml',
            'commit_sha': 'b'*40, 'expected_blob_sha': 'c'*40,
            'readback_blob_sha': 'c'*40, 'candidate_sha256': 'd'*64,
            'immutable_sha256': 'e'*64,
        }
        c = self.confirm
        self.entry = {'id': c['record_id'], 'path': c['path'],
                      'commit': c['commit_sha'], 'blob': c['readback_blob_sha'],
                      'gate': 'verified', 'candidate_sha256': c['candidate_sha256'],
                      'immutable_sha256': c['immutable_sha256']}
        self.manifest = {'id': c['source'], 'source_pdf_sha256': c['pdf_sha256'],
                         'catalog_number': 'FanPro25003', 'edition': 'SR3',
                         'verified_semantic_records': [self.entry]}
        self.receipt = {'commit': self.commit, 'exact': True}

    def check(self, *, raw=None):
        snapshot = yaml.safe_dump(self.manifest).encode() if raw is None else raw
        receipt = {'blob': blob(snapshot), **self.receipt}
        return verify_bytes(json.dumps(receipt).encode(), snapshot, self.path,
                            self.commit, blob(snapshot), confirm=self.confirm)

    def test_positive(self):
        result = self.check()
        self.assertEqual(result['schema'], 'mjlbb-compact-index-receipt/v1')
        self.assertFalse(result['receipt_prior_blob_checked'])
        self.assertFalse(result['formal_acceptance'])

    def test_missing_or_invalid_exact(self):
        for x in (False, 1, 'true'):
            self.receipt['exact'] = x
            with self.assertRaisesRegex(ValueError, 'readback_missing'):
                self.check()
        del self.receipt['exact']
        with self.assertRaisesRegex(ValueError, 'receipt_fields'):
            self.check()

    def test_unknown_fields(self):
        self.receipt['commit_sha'] = self.commit
        with self.assertRaisesRegex(ValueError, 'receipt_fields'):
            self.check()

    def test_wrong_source_or_edition(self):
        self.confirm['source'] = 'source.other'
        with self.assertRaisesRegex(ValueError, 'original_identity_mismatch'):
            self.check()
        self.confirm['source'] = 'source.fanpro-25003'
        self.manifest['edition'] = 'SR2'
        with self.assertRaisesRegex(ValueError, 'snapshot_identity_mismatch'):
            self.check()

    def test_missing_confirmation(self):
        self.confirm['status'] = 'preflighted'
        with self.assertRaisesRegex(ValueError, 'verified_confirm_required'):
            self.check()

    def test_mismatched_registration(self):
        for k, value in (('commit', 'f'*40), ('blob', 'f'*40),
                         ('gate', 'pending'), ('candidate_sha256', 'f'*64),
                         ('immutable_sha256', 'f'*64)):
            old = self.entry[k]; self.entry[k] = value
            with self.assertRaisesRegex(ValueError, 'registration_mismatch'):
                self.check()
            self.entry[k] = old

    def test_duplicate_registration(self):
        self.manifest['verified_semantic_records'].append(dict(self.entry))
        with self.assertRaisesRegex(ValueError, 'unique_registration_required'):
            self.check()

    def test_duplicate_yaml_key(self):
        raw = yaml.safe_dump(self.manifest).encode() + b'edition: SR3\n'
        with self.assertRaisesRegex(ValueError, 'duplicate_or_invalid_key'):
            self.check(raw=raw)

    def test_receipt_wrong_index_pin(self):
        self.receipt['commit'] = 'f'*40
        with self.assertRaisesRegex(ValueError, 'identity_mismatch'):
            self.check()

    def test_other_manifest_not_accepted(self):
        self.path = 'sources/manifests/Other.yml'
        with self.assertRaisesRegex(ValueError, 'unsupported_receipt_schema'):
            self.check()


if __name__ == '__main__':
    unittest.main()
