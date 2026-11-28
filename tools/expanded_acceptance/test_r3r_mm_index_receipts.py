"""Synthetic adversarial tests; no private archived source material."""
import copy
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes
from r3r_mm_index_receipts import MM, MM_SOURCE, MM_SHA, MM_RECORDS, R3R, R3R_SOURCE, R3R_SHA, R3R_RECORDS


class ReceiptTests(unittest.TestCase):
    def fixture(self, mm):
        path = next(iter(MM_RECORDS if mm else R3R_RECORDS))
        record = (MM_RECORDS if mm else R3R_RECORDS)[path]
        source, sha, catalog, edition, publisher = (
            (MM_SOURCE, MM_SHA, 'FASA7126', 'SR3', 'FASA Corporation') if mm else
            (R3R_SOURCE, R3R_SHA, 'FanPro10662', 'Shadowrun Third Edition', 'FanPro'))
        confirm = dict(protocol='sr3-gate/v1', status='verified', source=source,
                       pdf_sha256=sha, path=path, record_id=record[0], commit_sha='a'*40,
                       expected_blob_sha='b'*40, readback_blob_sha='b'*40,
                       candidate_sha256='c'*64, immutable_sha256='d'*64,
                       printed_pages='154' if mm else record[1], pdf_pages='155' if mm else record[2])
        entry = dict(id=record[0], path=path, commit='a'*40, blob='b'*40, gate='verified',
                     baseline_sha256='f'*64, candidate_sha256='c'*64, immutable_sha256='d'*64)
        doc = dict(id=source, source_pdf_sha256=sha, catalog_number=catalog, edition=edition, publisher=publisher)
        receipt = dict(semantic_commit='a'*40, semantic_blob='b'*40)
        if mm:
            entry.update(printed='154', pdf='155')
            doc['source_field_review'] = {record[1]: dict(source_pdf_sha256=sha, records=[entry])}
            receipt.update(source=source, index_commit='e'*40, semantic_live_and_commit_exact=True,
                           manifest_live_and_commit_exact=True, gate='verified', status='indexed')
        else:
            entry.update(range_printed=record[3], range_pdf=record[4], content_class='rule_exact',
                         original_source_sha256=sha, contiguous_advance=False)
            doc['verified_semantic_records'] = [entry]
            receipt.update(manifest_commit='e'*40, commit_readback_exact=True,
                           live_readback_exact=True, registration_count=1)
        return doc, entry, receipt, confirm

    def check(self, mm, mutation=None, tamper=False):
        doc, entry, receipt, confirm = self.fixture(mm)
        if mutation:
            mutation(doc, entry, receipt, confirm)
        snap = yaml.safe_dump(doc).encode()
        receipt['index_blob' if mm else 'manifest_blob'] = blob(snap)
        return verify_bytes(json.dumps(receipt).encode(), snap + (b'\n' if tamper else b''),
                            MM if mm else R3R, 'e'*40, blob(snap), confirm=confirm)

    def test_positive(self):
        for mm in (True, False):
            with self.subTest(mm=mm):
                result = self.check(mm)
                self.assertEqual(result['status'], 'consistent_original_index_artifacts')
                self.assertFalse(result['formal_acceptance'])
                self.assertFalse(result['receipt_prior_blob_checked'])

    def test_confirm_mutations(self):
        for mm in (True, False):
            for key, value in [('status', 'pending'), ('protocol', 'wrong'), ('source', 'wrong'),
                               ('pdf_sha256', '0'*64), ('path', 'rules/other.yml'), ('record_id', 'other'),
                               ('commit_sha', '0'*40), ('readback_blob_sha', '0'*40),
                               ('printed_pages', '0'), ('pdf_pages', '0'),
                               ('candidate_sha256', '0'*64), ('immutable_sha256', '0'*64)]:
                with self.subTest(mm=mm, key=key), self.assertRaises(ValueError):
                    self.check(mm, lambda d,e,r,c: c.update({key:value}))

    def test_receipt_mutations(self):
        for mm in (True, False):
            keys = [('semantic_commit','0'*40), ('semantic_blob','0'*40), ('extra',True)]
            keys += ([('gate','pending'), ('status','pending'), ('source','wrong'),
                      ('semantic_live_and_commit_exact',1), ('manifest_live_and_commit_exact',False)] if mm else
                     [('commit_readback_exact',1), ('live_readback_exact',False), ('registration_count',True),
                      ('registration_count',2)])
            for key, value in keys:
                with self.subTest(mm=mm,key=key), self.assertRaises(ValueError):
                    self.check(mm, lambda d,e,r,c: r.update({key:value}))

    def test_snapshot_and_registration_mutations(self):
        for mm in (True, False):
            for key, value in [('edition','SR2'), ('publisher','wrong'), ('catalog_number','wrong'),
                               ('source_pdf_sha256','0'*64)]:
                with self.subTest(mm=mm,key=key), self.assertRaises(ValueError):
                    self.check(mm, lambda d,e,r,c: d.update({key:value}))
            for key, value in [('gate','pending'), ('commit','0'*40), ('blob','0'*40),
                               ('candidate_sha256','0'*64), ('baseline_sha256','x'), ('immutable_sha256','0'*64),
                               ('printed' if mm else 'range_pdf','0')]:
                with self.subTest(mm=mm,key=key), self.assertRaises(ValueError):
                    self.check(mm, lambda d,e,r,c: e.update({key:value}))
            with self.assertRaises(ValueError):
                self.check(mm, lambda d,e,r,c: d.update(duplicate=[copy.deepcopy(e)]))
            with self.assertRaisesRegex(ValueError,'snapshot_blob_mismatch'):
                self.check(mm, tamper=True)

    def test_unrecognized_or_missing_fields(self):
        for mm in (True, False):
            with self.assertRaises(ValueError):
                self.check(mm, lambda d,e,r,c: r.pop('semantic_blob'))


if __name__ == '__main__':
    unittest.main()
