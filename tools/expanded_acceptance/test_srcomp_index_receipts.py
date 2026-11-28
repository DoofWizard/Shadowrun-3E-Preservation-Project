"""Synthetic receipt tests; these fixtures assert no historical evidence."""
import copy
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes
from srcomp_index_receipts import (SOURCE, SHA, MANIFEST, DISCLOSURE_KEY,
                                  DISCLOSURE_ID, DISCLOSURE_PATH, LAW_ID, LAW_PATH)


class CompanionReceiptTests(unittest.TestCase):
    def fixtures(self, law=False):
        rid, path, pages, pdfs = ((LAW_ID, LAW_PATH, [117, 118], [118, 119]) if law else
                                 (DISCLOSURE_ID, DISCLOSURE_PATH, [67, 68], [68, 69]))
        c = dict(protocol='sr3-gate/v1', status='verified', source=SOURCE, pdf_sha256=SHA,
                 record_id=rid, path=path, printed_pages='-'.join(map(str, pages)),
                 pdf_pages='-'.join(map(str, pdfs)), commit_sha='a'*40, readback_blob_sha='b'*40,
                 expected_blob_sha='b'*40, candidate_sha256='c'*64, immutable_sha256='d'*64)
        m = dict(id=SOURCE, source_pdf_sha256=SHA, edition='SR3', catalog_number='FASA7905a',
                 publisher='FASA Corporation')
        e = dict(candidate_sha256='c'*64, immutable_sha256='d'*64, gate='verified')
        r = dict(manifest_path=MANIFEST, index_commit='e'*40, semantic_commit='a'*40, semantic_blob='b'*40)
        if law:
            e.update(id=rid, path=path, commit='a'*40, blob='b'*40, original_source_sha256=SHA,
                     content_class='character_option', contiguous_advance=False, range_printed=pages, range_pdf=pdfs)
            m['postcompletion_mechanics_recovery'] = {'verified_semantic_records': [e]}
            r.update(exact_commit_live_readback=True, registration_matched=True, global_pages_advanced=0)
        else:
            e.update(record_id=rid, record_path=path, current_commit='a'*40, current_blob='b'*40,
                     source_id=SOURCE, original_pdf_sha256=SHA, actual_confirm='verified',
                     exact_commit_and_live_bytes=True, content_class='rule_exact', global_contiguous_pages=0,
                     printed_pages=pages, physical_pdf_pages=pdfs)
            m[DISCLOSURE_KEY] = e
            r.update(registration_key=DISCLOSURE_KEY, exact_commit_and_live_bytes=True)
        return c, m, e, r

    def check(self, c, m, r):
        raw = yaml.safe_dump(m).encode()
        receipt = dict(r, index_blob=blob(raw))
        return verify_bytes(json.dumps(receipt).encode(), raw, MANIFEST, 'e'*40, blob(raw), confirm=c)

    def test_both_actual_shapes(self):
        for law in (False, True):
            c,m,e,r = self.fixtures(law)
            got = self.check(c,m,r)
            self.assertEqual(got['schema'], 'srcomp-law-campaign-index-receipt/v1' if law else 'srcomp-disclosure-index-receipt/v1')
            self.assertFalse(got['formal_acceptance']); self.assertIsNone(got['receipt_prior_blob'])

    def test_wrong_receipt_fields(self):
        for law in (False, True):
            for k,val in [('semantic_commit','f'*40),('semantic_blob','f'*40),('index_commit','f'*40),('manifest_path','wrong'),('unknown',True)]:
                c,m,e,r = self.fixtures(law);r[k]=val
                with self.subTest(law=law,key=k),self.assertRaises(ValueError): self.check(c,m,r)

    def test_wrong_source_and_scope(self):
        for law in (False, True):
            for k,val in [('status','prepared'),('source','wrong'),('record_id','wrong'),('printed_pages','1-2'),('pdf_pages','2-3'),('pdf_sha256','f'*64),('immutable_sha256','f'*64)]:
                c,m,e,r = self.fixtures(law);c[k]=val
                with self.subTest(law=law,key=k),self.assertRaises(ValueError): self.check(c,m,r)

    def test_original_readback_flags_and_count(self):
        for law in (False, True):
            c,m,e,r = self.fixtures(law)
            r['exact_commit_live_readback' if law else 'exact_commit_and_live_bytes']=False
            with self.assertRaises(ValueError):self.check(c,m,r)
        for invalid in (False,0.0,1):
            c,m,e,r = self.fixtures(True);r['global_pages_advanced']=invalid
            with self.assertRaises(ValueError):self.check(c,m,r)

    def test_wrong_entry_or_alias(self):
        for law in (False, True):
            for k,val in [('gate','pending'),('candidate_sha256','f'*64),('commit_sha','f'*40),('content_class','campaign_guidance')]:
                c,m,e,r = self.fixtures(law);e[k]=val
                with self.subTest(law=law,key=k),self.assertRaises(ValueError):self.check(c,m,r)
            c,m,e,r = self.fixtures(law);e['range_pdf' if law else 'physical_pdf_pages']=[1,2]
            with self.assertRaises(ValueError):self.check(c,m,r)

    def test_duplicate_law_registration(self):
        c,m,e,r=self.fixtures(True)
        m['postcompletion_mechanics_recovery']['verified_semantic_records'].append(copy.deepcopy(e))
        with self.assertRaises(ValueError): self.check(c,m,r)

    def test_disclosure_registration_key_and_snapshot(self):
        c,m,e,r=self.fixtures();r['registration_key']='other'
        with self.assertRaises(ValueError):self.check(c,m,r)
        c,m,e,r=self.fixtures();m['edition']='SR2'
        with self.assertRaises(ValueError):self.check(c,m,r)


if __name__ == '__main__':
    unittest.main()
