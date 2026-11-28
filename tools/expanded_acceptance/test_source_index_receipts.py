import copy
import hashlib
import unittest

from source_index_receipts import adapt, MM, CC, MM_SOURCE, CC_SOURCE, MM_SHA, CC_SHA


class SourceIndexReceipts(unittest.TestCase):
    def setUp(self):
        self.snapshot = b'original manifest snapshot\n'
        self.commit, self.blob, self.prior = 'a'*40, 'b'*40, 'c'*40
        self.sem, self.semblob = 'd'*40, 'e'*40
        self.confirm = dict(protocol='sr3-gate/v1', status='verified', source=MM_SOURCE,
                            pdf_sha256=MM_SHA, commit_sha=self.sem, readback_blob_sha=self.semblob,
                            expected_blob_sha=self.semblob, path='rules/example.yml', record_id='rule.example')
        self.short = dict(status='indexed', path=MM, commit=self.commit, blob=self.blob,
                          branch_and_commit_readbacks_equal=True, exact_local_proposal_match=True)
        self.full = dict(status='indexed', source=MM_SOURCE, path=self.confirm['path'],
                         record_id=self.confirm['record_id'], semantic_commit=self.sem,
                         semantic_blob=self.semblob, manifest_commit=self.commit, manifest_blob=self.blob,
                         manifest_sha256=hashlib.sha256(self.snapshot).hexdigest(),
                         branch_and_commit_readback_equal=True, exact_index_proposal_readback_equal=True,
                         global_contiguous_page_credit=0, blob_sha=self.blob, commit_sha=self.commit)
        self.ccconfirm = dict(self.confirm, source=CC_SOURCE, pdf_sha256=CC_SHA)
        self.cc = dict(semantic_commit=self.sem, semantic_blob=self.semblob, index_commit=self.commit,
                       index_blob=self.blob, exact_live_readback=True, exact_commit_readback=True, path=CC,
                       record_id=self.confirm['record_id'], record_path=self.confirm['path'], status='indexed',
                       source=CC_SOURCE, manifest_commit=self.commit, manifest_blob=self.blob,
                       source_pdf_sha256=CC_SHA, commit_sha=self.commit, blob_sha=self.blob, prior_blob=self.prior,
                       exact_committed_and_live_bytes_match=True, commit_readback_blob=self.blob,
                       live_readback_blob=self.blob)

    def test_observed_schema_shapes(self):
        for receipt, path, confirm, prior, schema in (
            (self.short, MM, self.confirm, None, 'mm-reservoir-index-receipt/v1'),
            (self.full, MM, self.confirm, None, 'mm-device-index-receipt/v1'),
            (self.cc, CC, self.ccconfirm, self.prior, 'cc-index-receipt/v1')):
            with self.subTest(schema=schema):
                self.assertEqual(adapt(receipt, self.snapshot, path, confirm, prior),
                                 (self.commit, self.blob, path, prior, schema))

    def test_missing_or_nonboolean_attestations(self):
        for value in (False, 1, 'true', None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                adapt(dict(self.short, exact_local_proposal_match=value), self.snapshot, MM, self.confirm, None)
        bad = dict(self.full)
        del bad['branch_and_commit_readback_equal']
        with self.assertRaises(ValueError):
            adapt(bad, self.snapshot, MM, self.confirm, None)

    def test_conflicting_aliases(self):
        for receipt, path, confirm, prior in ((self.full, MM, self.confirm, None), (self.cc, CC, self.ccconfirm, self.prior)):
            with self.subTest(path=path), self.assertRaises(ValueError):
                adapt(dict(receipt, blob_sha='f'*40), self.snapshot, path, confirm, prior)

    def test_semantic_mismatch(self):
        with self.assertRaises(ValueError):
            adapt(dict(self.full, semantic_blob='f'*40), self.snapshot, MM, self.confirm, None)
        with self.assertRaises(ValueError):
            adapt(dict(self.cc, record_path='rules/other.yml'), self.snapshot, CC, self.ccconfirm, self.prior)

    def test_snapshot_digest(self):
        with self.assertRaises(ValueError):
            adapt(self.full, b'wrong snapshot', MM, self.confirm, None)

    def test_parent_pin(self):
        for prior in (None, 'f'*40):
            with self.subTest(prior=prior), self.assertRaises(ValueError):
                adapt(self.cc, self.snapshot, CC, self.ccconfirm, prior)

    def test_source_and_confirm_pins(self):
        for confirm in (None, dict(self.confirm, status='preflighted'), dict(self.confirm, pdf_sha256='f'*64), dict(self.confirm, expected_blob_sha='f'*40), self.ccconfirm):
            with self.subTest(confirm=confirm), self.assertRaises(ValueError):
                adapt(self.short, self.snapshot, MM, confirm, None)

    def test_no_extra_keys_or_credit(self):
        for receipt in (dict(self.short, blob_sha=self.blob), dict(self.full, global_contiguous_page_credit=False), dict(self.full, global_contiguous_page_credit=1)):
            with self.subTest(receipt=receipt), self.assertRaises(ValueError):
                adapt(receipt, self.snapshot, MM, self.confirm, None)

    def test_wrong_manifest(self):
        with self.assertRaises(ValueError):
            adapt(self.short, self.snapshot, 'sources/manifests/Other.yml', self.confirm, None)


if __name__ == '__main__':
    unittest.main()
