"""Synthetic tests for observed compact R3R index receipts, not acceptance."""
import copy
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes
from r3r_mm_index_receipts import R3R, R3R_SOURCE, R3R_SHA

RECORDS = (
    ('rules/drones/r3-revised-snake-eyes-sensory-qualifications-p93-94.yml', 'rule.drones.r3-revised-snake-eyes-sensory-qualifications-p93-94', [93,94], [95,96], 'rule_exact'),
    ('rules/gear/r3-revised-remote-control-accessory-ports-p95.yml', 'rule.gear.r3-revised-remote-control-accessory-ports-p95', [95,95], [97,97], 'rule_exact'),
    ('equipment/gear/r3-revised-snake-eyes-full-x-market-dashes-p95.yml', 'equipment.gear.r3-revised-snake-eyes-full-x-market-dashes-p95', [95,95], [97,97], 'equipment_stat'),
    ('rules/gear/r3-revised-scre-game-eligibility-p94.yml', 'rule.gear.r3-revised-scre-game-eligibility-p94', [94,94], [96,96], 'rule_exact'),
    ('equipment/gear/r3-revised-new-toys-p90-lower-table-dashes.yml', 'equipment.gear.r3-revised-new-toys-p90-lower-table-dashes', [90,90], [92,92], 'equipment_stat'),
)


def folios(span):
    return str(span[0]) if span[0] == span[1] else f'{span[0]}-{span[1]}'


class CompactCountTests(unittest.TestCase):
    def fixture(self, record):
        path, record_id, printed, pdf, kind = record
        entry = dict(id=record_id, path=path, commit='a'*40, blob='b'*40,
                     gate='verified', range_printed=printed, range_pdf=pdf,
                     content_class=kind, original_source_sha256=R3R_SHA,
                     baseline_sha256='c'*64, candidate_sha256='d'*64,
                     immutable_sha256='e'*64, contiguous_advance=False)
        doc = dict(id=R3R_SOURCE, source_pdf_sha256=R3R_SHA, catalog_number='FanPro10662',
                   edition='Shadowrun Third Edition', publisher='FanPro', verified_semantic_records=[entry])
        confirm = dict(protocol='sr3-gate/v1', status='verified', source=R3R_SOURCE,
                       pdf_sha256=R3R_SHA, path=path, record_id=record_id,
                       printed_pages=folios(printed), pdf_pages=folios(pdf), commit_sha='a'*40,
                       expected_blob_sha='b'*40, readback_blob_sha='b'*40,
                       candidate_sha256='d'*64, immutable_sha256='e'*64)
        if record == RECORDS[-1]:
            receipt = dict(index_commit='f'*40, manifest_blob='', live_blob='', previous_manifest_blob='1'*40,
                           semantic_commit='a'*40, semantic_blob='b'*40, historical_and_live_readbacks_match=True)
        else:
            receipt = dict(commit_sha='f'*40, blob_sha='', exact_commit_and_live_readback=True, verified_semantic_records=1)
        return doc, entry, receipt, confirm

    def check(self, record=RECORDS[0], mutate=None, tamper=False, parent='1'*40):
        doc, entry, receipt, confirm = self.fixture(record)
        if mutate:
            mutate(doc, entry, receipt, confirm)
        snap = yaml.safe_dump(doc).encode()
        pin = blob(snap)
        if record == RECORDS[-1]:
            receipt.update(manifest_blob=pin, live_blob=pin)
        else:
            receipt['blob_sha'] = pin
        return verify_bytes(json.dumps(receipt).encode(), snap + (b'\n' if tamper else b''),
                            R3R, 'f'*40, pin, parent, confirm=confirm)

    def test_positive_all_five(self):
        for record in RECORDS:
            with self.subTest(record=record[0]):
                out = self.check(record)
                self.assertFalse(out['formal_acceptance'])
                self.assertEqual(out['status'], 'consistent_original_index_artifacts')
                self.assertEqual(out['receipt_prior_blob_checked'], record == RECORDS[-1])

    def test_false_readback_or_extra_field(self):
        for key,val in [('exact_commit_and_live_readback', False), ('exact_commit_and_live_readback', 1),
                        ('verified_semantic_records', True), ('verified_semantic_records', 2), ('extra', 'x')]:
            with self.subTest(key=key,val=val), self.assertRaises(ValueError):
                self.check(mutate=lambda d,e,r,c: r.update({key:val}))

    def test_missing_receipt_field(self):
        with self.assertRaises(ValueError):
            self.check(mutate=lambda d,e,r,c: r.pop('exact_commit_and_live_readback'))

    def test_wrong_record_scope_or_digest(self):
        for key,val in [('source','wrong'),('pdf_sha256','0'*64),('status','pending'),('protocol','wrong'),
                        ('path','rules/unknown.yml'),('record_id','wrong'),('printed_pages','92'),('pdf_pages','94'),
                        ('expected_blob_sha','0'*40),('readback_blob_sha','0'*40),('commit_sha','0'*40),
                        ('candidate_sha256','0'*64),('immutable_sha256','0'*64)]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.check(mutate=lambda d,e,r,c: c.update({key:val}))

    def test_wrong_source_metadata(self):
        for key,val in [('id','wrong'),('source_pdf_sha256','0'*64),('edition','SR2'),('publisher','wrong'),('catalog_number','wrong')]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.check(mutate=lambda d,e,r,c: d.update({key:val}))

    def test_wrong_registration(self):
        for key,val in [('gate','pending'),('commit','0'*40),('blob','0'*40),('candidate_sha256','0'*64),
                        ('baseline_sha256','bad'),('immutable_sha256','0'*64),('range_printed',[93,93]),
                        ('range_pdf',[95,95]),('content_class','equipment_stat'),('original_source_sha256','0'*64),
                        ('contiguous_advance',True),('record_id','contradictory')]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.check(mutate=lambda d,e,r,c: e.update({key:val}))

    def test_duplicate_registration(self):
        with self.assertRaises(ValueError):
            self.check(mutate=lambda d,e,r,c: d.update(duplicate=[copy.deepcopy(e)]))

    def test_snapshot_tamper(self):
        with self.assertRaisesRegex(ValueError, 'snapshot_blob_mismatch'):
            self.check(tamper=True)

    def test_index_commit_mismatch(self):
        with self.assertRaises(ValueError):
            self.check(mutate=lambda d,e,r,c: r.update(commit_sha='0'*40))

    def test_parent_required_only_for_parent_receipt(self):
        self.assertFalse(self.check(parent=None)['receipt_prior_blob_checked'])
        for parent in (None,'0'*40):
            with self.subTest(parent=parent), self.assertRaises(ValueError):
                self.check(RECORDS[-1], parent=parent)

    def test_wrong_class_for_lower_table(self):
        with self.assertRaises(ValueError):
            self.check(RECORDS[-1], mutate=lambda d,e,r,c: e.update(content_class='rule_exact'))


if __name__ == '__main__':
    unittest.main()
