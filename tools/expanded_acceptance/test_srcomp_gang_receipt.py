"""Synthetic checks for the observed gang-scenario index receipt; no archival claims."""
import copy
import json
import unittest
import yaml
from inline_index_receipt import blob, verify_bytes
from srcomp_index_receipts import SOURCE, SHA, MANIFEST, GANG_ID, GANG_PATH


class GangScenarioReceiptTests(unittest.TestCase):
    def fixtures(self):
        c = dict(protocol='sr3-gate/v1', status='verified', source=SOURCE, pdf_sha256=SHA,
                 record_id=GANG_ID, path=GANG_PATH, printed_pages='124-129', pdf_pages='125-130',
                 commit_sha='a'*40, readback_blob_sha='b'*40, expected_blob_sha='b'*40,
                 candidate_sha256='c'*64, immutable_sha256='d'*64)
        e = dict(id=GANG_ID, path=GANG_PATH, commit='a'*40, blob='b'*40, gate='verified',
                 original_source_sha256=SHA, content_class='rule_exact', contiguous_advance=False,
                 range_printed=[124,129], range_pdf=[125,130], candidate_sha256='c'*64,
                 immutable_sha256='d'*64)
        m = dict(id=SOURCE, source_pdf_sha256=SHA, edition='SR3', catalog_number='FASA7905a',
                 publisher='FASA Corporation', postcompletion_mechanics_recovery={'verified_semantic_records':[e]})
        r = dict(path=MANIFEST, commit_sha='e'*40, semantic_commit='a'*40, semantic_blob='b'*40,
                 exact_commit_readback=True, exact_live_readback=True)
        return c,e,m,r

    def check(self,c,m,r):
        raw=yaml.safe_dump(m).encode(); r=dict(r,blob_sha=blob(raw))
        return verify_bytes(json.dumps(r).encode(),raw,MANIFEST,'e'*40,blob(raw),confirm=c)

    def test_gang_original_shape(self):
        c,e,m,r=self.fixtures(); got=self.check(c,m,r)
        self.assertEqual(got['schema'],'srcomp-gang-scenario-index-receipt/v1')
        self.assertFalse(got['formal_acceptance']); self.assertIsNone(got['receipt_prior_blob'])

    def test_gang_rejects_missing_or_false_flags_and_aliases(self):
        for k,val in [('exact_commit_readback',False),('exact_live_readback',1),('path','wrong'),
                      ('commit_sha','f'*40),('semantic_blob','f'*40),('manifest_path',MANIFEST)]:
            c,e,m,r=self.fixtures();r[k]=val
            with self.subTest(key=k),self.assertRaises(ValueError):self.check(c,m,r)
        c,e,m,r=self.fixtures();del r['exact_live_readback']
        with self.assertRaises(ValueError):self.check(c,m,r)

    def test_gang_rejects_wrong_scope_or_index(self):
        for k,val in [('record_id','other'),('printed_pages','124'),('pdf_pages','124-129'),('source','other')]:
            c,e,m,r=self.fixtures();c[k]=val
            with self.subTest(key=k),self.assertRaises(ValueError):self.check(c,m,r)
        for k,val in [('content_class','character_option'),('contiguous_advance',True),('range_printed',[124.0,129.0]),('commit_sha','f'*40),('gate','pending')]:
            c,e,m,r=self.fixtures();e[k]=val
            with self.subTest(key=k),self.assertRaises(ValueError):self.check(c,m,r)
        c,e,m,r=self.fixtures();m['postcompletion_mechanics_recovery']['verified_semantic_records'].append(copy.deepcopy(e))
        with self.assertRaises(ValueError):self.check(c,m,r)


if __name__ == '__main__':
    unittest.main()
