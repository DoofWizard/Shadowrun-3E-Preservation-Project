"""Synthetic checks for five explicitly bound short-format R3R receipts."""
import copy
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes
from r3r_mm_index_receipts import R3R, R3R_SOURCE, R3R_SHA, R3R_NEW_TOYS_RECORDS


class NewToysReceiptTests(unittest.TestCase):
    def check(self, path, mutate=None, parent='f'*40, tamper=False):
        rid, printed, pdf, printed_range, pdf_range, cls = R3R_NEW_TOYS_RECORDS[path]
        confirm = dict(protocol='sr3-gate/v1', status='verified', source=R3R_SOURCE,
                       pdf_sha256=R3R_SHA, path=path, record_id=rid, commit_sha='a'*40,
                       expected_blob_sha='b'*40, readback_blob_sha='b'*40,
                       candidate_sha256='c'*64, immutable_sha256='d'*64,
                       printed_pages=printed, pdf_pages=pdf)
        entry = dict(id=rid, path=path, commit='a'*40, blob='b'*40, gate='verified',
                     baseline_sha256='9'*64, candidate_sha256='c'*64, immutable_sha256='d'*64,
                     range_printed=printed_range, range_pdf=pdf_range, content_class=cls,
                     original_source_sha256=R3R_SHA, contiguous_advance=False)
        doc = dict(id=R3R_SOURCE, source_pdf_sha256=R3R_SHA, catalog_number='FanPro10662',
                   edition='Shadowrun Third Edition', publisher='FanPro', verified_semantic_records=[entry])
        receipt = dict(status='indexed', semantic_commit='a'*40, semantic_blob='b'*40,
                       index_commit='e'*40, historical_and_live_exact_readback=True,
                       source_manifest_before_blob='f'*40)
        if mutate:
            mutate(doc, entry, receipt, confirm)
        snap = yaml.safe_dump(doc).encode()
        receipt['index_blob'] = blob(snap)
        return verify_bytes(json.dumps(receipt).encode(), snap + (b'\n' if tamper else b''),
                            R3R, 'e'*40, blob(snap), parent_blob=parent, confirm=confirm)

    def test_all_five(self):
        for path in R3R_NEW_TOYS_RECORDS:
            with self.subTest(path=path):
                r = self.check(path)
                self.assertEqual(r['status'], 'consistent_original_index_artifacts')
                self.assertTrue(r['receipt_prior_blob_checked'])
                self.assertFalse(r['formal_acceptance'])

    def test_parent_required(self):
        for path in R3R_NEW_TOYS_RECORDS:
            for parent in (None, '0'*40):
                with self.subTest(path=path,parent=parent), self.assertRaises(ValueError):
                    self.check(path, parent=parent)

    def test_source_class_and_page_bindings(self):
        for path, spec in R3R_NEW_TOYS_RECORDS.items():
            for key,value in [('content_class','rule_exact' if spec[-1]=='equipment_stat' else 'equipment_stat'),
                              ('range_printed',[0,0]), ('range_pdf',[0,0]), ('contiguous_advance',True),
                              ('original_source_sha256','0'*64)]:
                with self.subTest(path=path,key=key), self.assertRaises(ValueError):
                    self.check(path,lambda d,e,r,c:e.update({key:value}))
            with self.assertRaises(ValueError):
                self.check(path,lambda d,e,r,c:d.update(edition='SR2'))

    def test_no_receipt_shape_or_identity_expansion(self):
        for path in R3R_NEW_TOYS_RECORDS:
            for key,value in [('status','pending'),('semantic_commit','0'*40),('semantic_blob','0'*40),
                              ('historical_and_live_exact_readback',1),('extra',True)]:
                with self.subTest(path=path,key=key), self.assertRaises(ValueError):
                    self.check(path,lambda d,e,r,c:r.update({key:value}))
            for key,value in [('path','rules/other.yml'),('record_id','other'),('pdf_pages','0'),
                              ('source','source.other'),('candidate_sha256','0'*64),('immutable_sha256','0'*64)]:
                with self.subTest(path=path,key=key), self.assertRaises(ValueError):
                    self.check(path,lambda d,e,r,c:c.update({key:value}))

    def test_duplicate_and_tamper_rejected(self):
        for path in R3R_NEW_TOYS_RECORDS:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.check(path,lambda d,e,r,c:d.update(duplicate=[copy.deepcopy(e)]))
            with self.assertRaises(ValueError):
                self.check(path,tamper=True)


if __name__ == '__main__':
    unittest.main()
