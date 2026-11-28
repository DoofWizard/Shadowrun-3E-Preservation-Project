"""Synthetic regressions for the two original R3R qualification schemas."""
import copy
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes, verify
from r3r_mm_index_receipts import R3R, R3R_SOURCE, R3R_SHA, R3R_QUAL_RECORDS

PARENT = 'f'*40
INDEX = 'e'*40


def fixture(path):
    printed, pdf, pr, ph = R3R_QUAL_RECORDS[path]
    record_id = 'rule.vehicles.' + path.rsplit('/', 1)[-1][:-4]
    confirm = dict(protocol='sr3-gate/v1', status='verified', source=R3R_SOURCE,
                   pdf_sha256=R3R_SHA, path=path, record_id=record_id, commit_sha='a'*40,
                   expected_blob_sha='b'*40, readback_blob_sha='b'*40,
                   candidate_sha256='c'*64, immutable_sha256='d'*64,
                   printed_pages=printed, pdf_pages=pdf)
    entry = dict(id=record_id, path=path, commit='a'*40, blob='b'*40, gate='verified',
                 baseline_sha256='f'*64, candidate_sha256='c'*64, immutable_sha256='d'*64,
                 range_printed=pr, range_pdf=ph, content_class='rule_exact',
                 original_source_sha256=R3R_SHA, contiguous_advance=False)
    doc = dict(id=R3R_SOURCE, source_pdf_sha256=R3R_SHA, catalog_number='FanPro10662',
               edition='Shadowrun Third Edition', publisher='FanPro', verified_semantic_records=[entry])
    receipt = dict(status='indexed', semantic_commit='a'*40, semantic_blob='b'*40, index_commit=INDEX)
    if 'ship-' in path:
        receipt.update(source=R3R_SOURCE, path=R3R, record_path=path, record_id=record_id,
                       prior_blob=PARENT, commit_readback_exact=True, live_readback_exact=True,
                       contiguous_advance=False)
    else:
        receipt.update(historical_and_live_exact_readback=True, source_manifest_before_blob=PARENT)
    return doc, entry, receipt, confirm


def check(doc, receipt, confirm, parent=PARENT, tamper=False):
    snap = yaml.safe_dump(doc).encode()
    receipt['index_blob'] = blob(snap)
    return verify_bytes(json.dumps(receipt).encode(), snap + (b'\n' if tamper else b''),
                        R3R, INDEX, blob(snap), parent, confirm=confirm)


class QualificationReceipts(unittest.TestCase):
    def test_every_observed_scope(self):
        for path in R3R_QUAL_RECORDS:
            with self.subTest(path=path):
                d,e,r,c = fixture(path)
                result = check(d,r,c)
                self.assertTrue(result['receipt_prior_blob_checked'])
                self.assertFalse(result['formal_acceptance'])

    def test_parent_missing_or_wrong(self):
        for path in R3R_QUAL_RECORDS:
            for parent in (None, '0'*40):
                d,e,r,c = fixture(path)
                with self.subTest(path=path, parent=parent), self.assertRaisesRegex(ValueError,'original_parent_mismatch'):
                    check(d,r,c,parent)

    def test_confirm_mutations(self):
        for path in R3R_QUAL_RECORDS:
            for key,val in [('status','pending'), ('source','other'), ('pdf_sha256','0'*64),
                            ('path','rules/vehicles/other.yml'), ('record_id','other'),
                            ('pdf_pages','1'), ('printed_pages','1'), ('commit_sha','0'*40),
                            ('readback_blob_sha','0'*40), ('candidate_sha256','0'*64)]:
                d,e,r,c = fixture(path); c[key]=val
                with self.subTest(path=path,key=key), self.assertRaises(ValueError): check(d,r,c)

    def test_registration_mutations(self):
        for path in R3R_QUAL_RECORDS:
            for key,val in [('gate','pending'), ('blob','0'*40), ('range_pdf',[1,1]),
                            ('range_printed',[1,1]), ('original_source_sha256','0'*64),
                            ('contiguous_advance',True), ('content_class','equipment_stat')]:
                d,e,r,c = fixture(path); e[key]=val
                with self.subTest(path=path,key=key), self.assertRaises(ValueError): check(d,r,c)
            d,e,r,c = fixture(path); d['verified_semantic_records'].append(copy.deepcopy(e))
            with self.assertRaises(ValueError): check(d,r,c)

    def test_receipt_mutations(self):
        for path in R3R_QUAL_RECORDS:
            d,e,r,c = fixture(path)
            keys = [('status','pending'), ('semantic_commit','0'*40), ('extra',True)]
            keys += ([('record_id','other'), ('record_path','other'), ('source','other'),
                      ('path','other'), ('contiguous_advance',0), ('commit_readback_exact',1),
                      ('live_readback_exact',False)] if 'ship-' in path else
                     [('historical_and_live_exact_readback',1)])
            for key,val in keys:
                d,e,r,c = fixture(path); r[key]=val
                with self.subTest(path=path,key=key), self.assertRaises(ValueError): check(d,r,c)

    def test_snapshot_identity_and_bytes(self):
        for path in R3R_QUAL_RECORDS:
            for key,val in [('edition','SR2'), ('publisher','other'), ('id','other')]:
                d,e,r,c = fixture(path); d[key]=val
                with self.assertRaises(ValueError): check(d,r,c)
            d,e,r,c = fixture(path)
            with self.assertRaisesRegex(ValueError,'snapshot_blob_mismatch'): check(d,r,c,tamper=True)

    def test_cross_layout_rejected(self):
        paths = list(R3R_QUAL_RECORDS)
        d,e,r,c = fixture(paths[0]); _,_,naval,_ = fixture(paths[-1]); naval.update(record_id=c['record_id'],record_path=c['path'])
        with self.assertRaisesRegex(ValueError,'qualification_layout_mismatch'): check(d,naval,c)
        d,e,r,c = fixture(paths[-1]); _,_,short,_ = fixture(paths[0])
        with self.assertRaisesRegex(ValueError,'qualification_layout_mismatch'): check(d,short,c)

    def test_production_verify_reads_actual_parent(self):
        import base64, hashlib
        for path in (list(R3R_QUAL_RECORDS)[0], list(R3R_QUAL_RECORDS)[-1]):
            d,e,r,c = fixture(path); snap=yaml.safe_dump(d).encode(); parent=b'actual parent manifest bytes\n'
            r['source_manifest_before_blob' if 'ship-' not in path else 'prior_blob'] = blob(parent)
            r['index_blob']=blob(snap)
            def artifact(raw):
                return dict(original_locator='synthetic-fixture',sha256=hashlib.sha256(raw).hexdigest(),bytes_base64=base64.b64encode(raw).decode())
            tx=dict(index_commit=INDEX,confirm=c,historical_index_receipt_artifact=artifact(json.dumps(r).encode()),historical_index_snapshot_artifact=artifact(snap))
            class Git:
                def read(self, path, ref):
                    return snap if ref==INDEX else parent
            result=verify(Git(),R3R,tx,dict(index_commit=INDEX,index_parent='parent',status='new_or_changed_verified_registration'))
            self.assertTrue(result['receipt_prior_blob_checked'])


if __name__ == '__main__': unittest.main()
