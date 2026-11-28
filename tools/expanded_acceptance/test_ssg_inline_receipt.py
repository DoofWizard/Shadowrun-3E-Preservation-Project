"""Synthetic tests for the observed SSG lifestyle correction receipt schema."""
import json
import unittest
from inline_index_receipt import blob, verify_bytes


class SSGReceiptTests(unittest.TestCase):
    def setUp(self):
        self.path = 'sources/manifests/SprawlSurvivalGuide.yml'
        self.snapshot = b'synthetic index\n'
        self.parent = blob(b'prior synthetic index\n')
        self.confirm = {'protocol': 'sr3-gate/v1', 'status': 'verified',
                        'source': 'source.fanpro-10667',
                        'pdf_sha256': 'b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f',
                        'record_id': 'rule.lifestyle.ssg-detailed-lifestyle-edges-flaws-p137-144',
                        'path': 'rules/lifestyle/ssg-detailed-lifestyle-edges-flaws-p137-144.yml',
                        'commit_sha': 'a'*40, 'expected_blob_sha': 'b'*40,
                        'readback_blob_sha': 'b'*40, 'candidate_sha256': 'c'*64,
                        'immutable_sha256': 'd'*64}
        self.receipt = {'path': self.path, 'prior_blob_sha': self.parent,
                        'index_commit_sha': 'e'*40, 'index_blob_sha': blob(self.snapshot),
                        'record_id': self.confirm['record_id'], 'semantic_commit_sha': 'a'*40,
                        'semantic_blob_sha': 'b'*40, 'candidate_sha256': 'c'*64,
                        'immutable_sha256': 'd'*64, 'committed_exact': True, 'live_exact': True,
                        'semantic_committed_exact': True, 'semantic_live_exact': True, 'status': 'indexed'}

    def check(self, **kw):
        return verify_bytes(json.dumps(kw.get('receipt', self.receipt)).encode(),
                            kw.get('snapshot', self.snapshot), self.path, 'e'*40,
                            blob(self.snapshot), kw.get('parent', self.parent),
                            confirm=kw.get('confirm', self.confirm))

    def test_positive(self):
        r = self.check()
        self.assertEqual(r['schema'], 'ssg-lifestyle-p137-index-receipt/v1')
        self.assertTrue(r['receipt_prior_blob_checked'])
        self.assertFalse(r['formal_acceptance'])

    def test_wrong_confirm(self):
        for key, value in [('protocol','wrong'), ('status','preflighted'), ('source','wrong'),
                           ('pdf_sha256','0'*64), ('record_id','other'), ('path','rules/other.yml'),
                           ('expected_blob_sha','0'*40), ('commit_sha','0'*40),
                           ('candidate_sha256','0'*64), ('immutable_sha256','0'*64)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(confirm={**self.confirm, key:value})
        with self.assertRaises(ValueError):
            self.check(confirm=None)

    def test_wrong_receipt(self):
        for key, value in [('status','pending'), ('committed_exact',1), ('live_exact',False),
                           ('semantic_committed_exact',False), ('semantic_live_exact',False),
                           ('semantic_commit_sha','0'*40), ('semantic_blob_sha','0'*40),
                           ('candidate_sha256','0'*64), ('immutable_sha256','0'*64),
                           ('index_commit_sha','0'*40), ('index_blob_sha','0'*40),
                           ('record_id','other'), ('path','sources/manifests/Other.yml')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(receipt={**self.receipt, key:value})

    def test_original_snapshot_and_parent(self):
        with self.assertRaisesRegex(ValueError, 'snapshot_blob_mismatch'):
            self.check(snapshot=b'changed')
        with self.assertRaisesRegex(ValueError, 'parent_blob_mismatch'):
            self.check(parent='0'*40)

    def test_extra_field(self):
        with self.assertRaisesRegex(ValueError, 'ssg_receipt_fields'):
            self.check(receipt={**self.receipt, 'unrecognized': True})
