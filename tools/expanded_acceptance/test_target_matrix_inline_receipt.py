"""Synthetic receipt-schema regressions; not historical evidence."""
import json
import unittest
from inline_index_receipt import verify_bytes, blob


class TargetMatrixReceiptTests(unittest.TestCase):
    def setUp(self):
        self.path = 'sources/manifests/TargetMatrix.yml'
        self.snapshot = b'new synthetic manifest\n'
        self.parent = blob(b'old synthetic manifest\n')
        self.receipt = {'path': self.path, 'commit': 'a'*40,
                        'blob': blob(self.snapshot), 'previous_blob': self.parent,
                        'semantic_commit': 'b'*40, 'semantic_blob': 'c'*40,
                        'exact_commit_and_branch_readback': True,
                        'commit_sha': 'a'*40, 'blob_sha': blob(self.snapshot)}
        self.confirm = {'protocol': 'sr3-gate/v1', 'status': 'verified',
                        'source': 'source.fasa-7219',
                        'pdf_sha256': 'dc9fbba78b9eb5efc60941213a90dfa0be190275dc92ea671631ddb7db154c4b',
                        'record_id': 'synthetic.fixture', 'path': 'rules/synthetic.yml',
                        'commit_sha': 'b'*40, 'readback_blob_sha': 'c'*40,
                        'expected_blob_sha': 'c'*40}

    def check(self, **kw):
        return verify_bytes(json.dumps(self.receipt).encode(),
                            kw.get('snapshot', self.snapshot), self.path, 'a'*40,
                            blob(self.snapshot), kw.get('parent', self.parent),
                            semantic_commit='b'*40, semantic_blob='c'*40,
                            confirm=kw.get('confirm', self.confirm))

    def test_positive(self):
        r = self.check()
        self.assertEqual(r['schema'], 'target-matrix-index-receipt/v1')
        self.assertFalse(r['formal_acceptance'])
        self.assertTrue(r['receipt_prior_blob_checked'])

    def test_wrong_confirm(self):
        for key, value in [('protocol','wrong'), ('status','preflighted'),
                           ('source','source.wrong'), ('pdf_sha256','0'*64),
                           ('record_id',''), ('path','rules/../bad.yml'),
                           ('commit_sha','d'*40), ('readback_blob_sha','d'*40),
                           ('expected_blob_sha','d'*40)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(confirm={**self.confirm, key:value})
        with self.assertRaisesRegex(ValueError, 'verified_confirm_required'):
            self.check(confirm=None)

    def test_alias_and_readback(self):
        for key, value in [('commit_sha','d'*40), ('blob_sha','d'*40),
                           ('exact_commit_and_branch_readback',1),
                           ('semantic_commit','d'*40), ('semantic_blob','d'*40)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                original = self.receipt[key]
                try:
                    self.receipt[key] = value
                    self.check()
                finally:
                    self.receipt[key] = original

    def test_parent_and_snapshot(self):
        with self.assertRaisesRegex(ValueError, 'parent_blob_mismatch'):
            self.check(parent='d'*40)
        with self.assertRaisesRegex(ValueError, 'snapshot_blob_mismatch'):
            self.check(snapshot=b'changed')

    def test_extra_field(self):
        self.receipt['unrecognized'] = True
        with self.assertRaisesRegex(ValueError, 'matrix_receipt_fields'):
            self.check()
