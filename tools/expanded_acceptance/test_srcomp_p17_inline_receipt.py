"""Synthetic tests for the observed FASA7905a p17 archive shape; not original evidence."""
import copy
import json
import unittest

import yaml
from inline_index_receipt import blob, verify_bytes

MP = 'sources/manifests/SRComp.yml'
RID = 'option.character-creation.srcomp-custom-edge-flaw-worked-example-p17'
RP = 'options/character-creation/srcomp-custom-edge-flaw-worked-example-p17.yml'
SRC = '8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5'


class SRCompP17ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.c = dict(protocol='sr3-gate/v1', status='verified', source='source.srcomp',
                      pdf_sha256=SRC, printed_pages='17', pdf_pages='18',
                      record_id=RID, path=RP, commit_sha='a'*40,
                      readback_blob_sha='b'*40, expected_blob_sha='b'*40,
                      candidate_sha256='c'*64, immutable_sha256='d'*64)
        self.e = dict(id=RID, path=RP, commit='a'*40, blob='b'*40, gate='verified',
                      content_class='character_option', original_source_sha256=SRC,
                      range_printed=[17,17], range_pdf=[18,18], contiguous_advance=False,
                      candidate_sha256='c'*64, immutable_sha256='d'*64)
        self.m = dict(id='source.srcomp', edition='SR3', publisher='FASA Corporation',
                      catalog_number='FASA7905a', source_pdf_sha256=SRC,
                      postcompletion_mechanics_recovery=dict(verified_semantic_records=[self.e]))
        self.r = dict(path=MP, commit='e'*40, record_id=RID,
                      exact_commit_and_live_readback=True, registration_delta=1)

    def verify(self, **kwargs):
        raw = yaml.safe_dump(self.m).encode()
        receipt = dict(self.r, blob=blob(raw))
        receipt.update(kwargs)
        return verify_bytes(json.dumps(receipt).encode(), raw, MP, 'e'*40,
                            blob(raw), confirm=self.c)

    def test_valid_no_invented_parent(self):
        v = self.verify()
        self.assertEqual(v['schema'], 'srcomp-p17-index-receipt/v1')
        self.assertIsNone(v['receipt_prior_blob'])
        self.assertFalse(v['receipt_prior_blob_checked'])
        self.assertFalse(v['formal_acceptance'])

    def test_false_readback_or_noninteger_delta_rejected(self):
        for changes in (dict(exact_commit_and_live_readback=False), dict(registration_delta=True),
                        dict(registration_delta=0), dict(registration_delta=1.0)):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.verify(**changes)

    def test_receipt_wrong_identity_or_extra_fields_rejected(self):
        for changes in (dict(record_id='other'), dict(blob='f'*40),
                        dict(path='sources/manifests/MitS.yml'), dict(prior_blob='f'*40)):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.verify(**changes)

    def test_confirm_missing_wrong_source_page_status_rejected(self):
        for field, value in [('source','source.mits'),('pdf_sha256','f'*64),
                             ('printed_pages','18'),('pdf_pages','17'),('status','preflighted'),
                             ('expected_blob_sha','f'*40),('record_id','different')]:
            old = self.c[field]; self.c[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.verify()
            self.c[field] = old
        self.c = None
        with self.assertRaises(ValueError):
            self.verify()

    def test_wrong_snapshot_edition_or_publisher_rejected(self):
        self.m['edition']='SR2'
        with self.assertRaises(ValueError): self.verify()
        self.m['edition']='SR3'; self.m['publisher']='other'
        with self.assertRaises(ValueError): self.verify()

    def test_registration_wrong_fields_types_and_aliases_rejected(self):
        for field,value in [('commit','f'*40),('blob','f'*40),('candidate_sha256','f'*64),
                            ('range_printed',[17.0,17.0]),('range_pdf',[17,18]),
                            ('contiguous_advance',True),('gate','pending'),
                            ('original_source_sha256','f'*64),('content_class','rule_exact')]:
            old=self.e[field];self.e[field]=value
            with self.subTest(field=field), self.assertRaises(ValueError): self.verify()
            self.e[field]=old
        self.e['commit_sha']='f'*40
        with self.assertRaises(ValueError): self.verify()

    def test_duplicate_registration_rejected(self):
        self.m['postcompletion_mechanics_recovery']['verified_semantic_records'].append(copy.deepcopy(self.e))
        with self.assertRaises(ValueError): self.verify()

    def test_duplicate_receipt_key_rejected(self):
        raw = yaml.safe_dump(self.m).encode()
        receipt = json.dumps(dict(self.r, blob=blob(raw))).encode()
        receipt = receipt[:-1] + b',"registration_delta":1}'
        with self.assertRaises(ValueError):
            verify_bytes(receipt, raw, MP, 'e'*40, blob(raw), confirm=self.c)


if __name__ == '__main__':
    unittest.main()
