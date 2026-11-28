"""Synthetic adversarial fixtures for compact original R3R index receipts."""
import copy
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes
from r3r_mm_index_receipts import R3R, R3R_SOURCE, R3R_SHA


class CompactParentTests(unittest.TestCase):
    def fixture(self, equipment=False):
        record_id = ('equipment.gear.r3-revised-new-toys-weight-dashes-p98-101' if equipment
                     else 'rule.vehicles.r3-revised-intermediate-design-examples-p111')
        path = ('equipment/gear/r3-revised-new-toys-weight-dashes-p98-101.yml' if equipment
                else 'rules/vehicles/r3-revised-intermediate-design-examples-p111.yml')
        printed, pdf = ([98, 101], [100, 103]) if equipment else ([111, 111], [113, 113])
        confirm = dict(protocol='sr3-gate/v1', status='verified', source=R3R_SOURCE,
                       pdf_sha256=R3R_SHA, path=path, record_id=record_id, commit_sha='a'*40,
                       expected_blob_sha='b'*40, readback_blob_sha='b'*40,
                       candidate_sha256='c'*64, immutable_sha256='d'*64,
                       printed_pages='98-101' if equipment else '111', pdf_pages='100-103' if equipment else '113')
        entry = dict(id=record_id, path=path, commit='a'*40, blob='b'*40, gate='verified',
                     baseline_sha256='f'*64, candidate_sha256='c'*64, immutable_sha256='d'*64,
                     range_printed=printed, range_pdf=pdf, content_class='equipment_stat' if equipment else 'rule_exact',
                     original_source_sha256=R3R_SHA, contiguous_advance=False)
        doc = dict(id=R3R_SOURCE, source_pdf_sha256=R3R_SHA, catalog_number='FanPro10662',
                   edition='Shadowrun Third Edition', publisher='FanPro', verified_semantic_records=[entry])
        receipt = dict(semantic_commit='a'*40, semantic_blob='b'*40, index_commit='e'*40,
                       previous_manifest_blob='f'*40, historical_and_live_readbacks_match=True)
        return doc, entry, receipt, confirm

    def check(self, equipment=False, mutation=None, parent='f'*40, tamper=False):
        doc, entry, receipt, confirm = self.fixture(equipment)
        if mutation:
            mutation(doc, entry, receipt, confirm)
        snapshot = yaml.safe_dump(doc).encode()
        receipt['manifest_blob'] = blob(snapshot)
        receipt.setdefault('live_blob', blob(snapshot))
        return verify_bytes(json.dumps(receipt).encode(), snapshot + (b'\n' if tamper else b''), R3R,
                            'e'*40, blob(snapshot), parent, confirm=confirm)

    def test_both_classes(self):
        for equipment in (False, True):
            with self.subTest(equipment=equipment):
                result = self.check(equipment)
                self.assertEqual(result['schema'], 'r3r-compact-parent-index-receipt/v1')
                self.assertTrue(result['receipt_prior_blob_checked'])
                self.assertFalse(result['formal_acceptance'])

    def test_receipt_mutations(self):
        for key, value in [('semantic_blob','0'*40), ('semantic_commit','0'*40), ('live_blob','0'*40),
                           ('previous_manifest_blob','0'*40), ('historical_and_live_readbacks_match',1),
                           ('extra',True), ('index_commit','0'*40)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(mutation=lambda d,e,r,c: r.update({key:value}))

    def test_missing_parent_and_tampered_bytes(self):
        for parent in (None,'0'*40):
            with self.subTest(parent=parent), self.assertRaises(ValueError):
                self.check(parent=parent)
        with self.assertRaises(ValueError):
            self.check(tamper=True)

    def test_confirm_mutations(self):
        for key, value in [('status','pending'), ('protocol','wrong'), ('source','wrong'), ('pdf_sha256','0'*64),
                           ('path','rules/other.yml'), ('record_id','other'), ('pdf_pages','111'),
                           ('printed_pages','113'), ('expected_blob_sha','0'*40), ('candidate_sha256','0'*64)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(mutation=lambda d,e,r,c: c.update({key:value}))

    def test_registration_mutations(self):
        for key, value in [('gate','pending'), ('content_class','rule_exact'), ('original_source_sha256','0'*64),
                           ('range_pdf',[100,102]), ('contiguous_advance',True), ('immutable_sha256','0'*64),
                           ('baseline_sha256','bad'), ('blob_sha','0'*40)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.check(True, mutation=lambda d,e,r,c: e.update({key:value}))
        with self.assertRaises(ValueError):
            self.check(mutation=lambda d,e,r,c: d.update(duplicate=[copy.deepcopy(e)]))
        with self.assertRaises(ValueError):
            self.check(mutation=lambda d,e,r,c: d.update(edition='SR2'))


if __name__ == '__main__':
    unittest.main()
