import unittest, tempfile
from pathlib import Path
import yaml
from ingestion_gate import *

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.b=self.root/'b.yml'
        self.c=self.root/'c.yml'
        self.record={'id':'reference.test','source':'source.test','record_type':'reference',
                     'status':'ingested','printed_pages':'62-65','pdf_pages':'63-66',
                     'edition_scope':'SR2','content_class':['equipment_stat'],
                     'framing':'reference_exact','data':{'tn':4,'damage':'5M','exceptions':['a','b']}}
        self.b.write_text(yaml.safe_dump(self.record))
        self.c.write_text(yaml.safe_dump(self.record))
        self.plan=prepare(self.b,self.c,'references/security/test.yml','source.test','a'*64)
        self.receipt=confirm(self.plan,self.c,'b'*40,self.plan['expected_blob_sha'])
        self.manifest={'id':'source.test','status':'ingesting','done':{'p':61,'pdf':62},
            'next':{'p':62,'pdf':63},'routes':[[62,65,'directed']],'pending':[]}
        self.checkpoint={'active_source':'source.test',
            'completed_through':{'printed_page':61,'pdf_page':62},
            'resume_at':{'printed_page':62,'pdf_page':63},
            'pending_normalization':[],'open_conflicts':[]}
    def tearDown(self): self.tmp.cleanup()
    def bad(self,fn):
        with self.assertRaises(InvalidRecord): fn()
    def test_good(self):
        self.assertTrue(authorize_advance(self.manifest,self.checkpoint,
            [self.receipt],62,63,66,67)['authorized'])
    def test_single_receipt(self):
        self.assertTrue(authorize_advance(self.manifest,self.checkpoint,
            self.receipt,62,63,66,67)['authorized'])
    def test_record_outside_slice(self):
        self.receipt['printed_pages']='70-71'
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,
            [self.receipt],62,63,66,67))
    def test_no_preflight(self):
        self.bad(lambda:confirm({'status':'ready'},self.c,'b'*40,'c'*40))
    def test_mutation(self):
        self.c.write_text(self.c.read_text()+'\n')
        self.bad(lambda:confirm(self.plan,self.c,'b'*40,self.plan['expected_blob_sha']))
    def test_bad_remote_hash(self):
        self.bad(lambda:confirm(self.plan,self.c,'b'*40,'0'*40))
    def test_missing_remote_hash(self):
        self.bad(lambda:confirm(self.plan,self.c,'b'*40,''))
    def test_changed_stat(self):
        self.record['data']['tn']=5
        self.c.write_text(yaml.safe_dump(self.record))
        self.bad(lambda:prepare(self.b,self.c,self.plan['path'],'source.test','a'*64))
    def test_changed_damage(self):
        self.record['data']['damage']='5L'
        self.c.write_text(yaml.safe_dump(self.record))
        self.bad(lambda:prepare(self.b,self.c,self.plan['path'],'source.test','a'*64))
    def test_changed_exception(self):
        self.record['data']['exceptions'].remove('b')
        self.c.write_text(yaml.safe_dump(self.record))
        self.bad(lambda:prepare(self.b,self.c,self.plan['path'],'source.test','a'*64))
    def test_missing_hash(self):
        self.bad(lambda:prepare(self.b,self.c,self.plan['path'],'source.test','missing'))
    def test_changed_source(self):
        self.bad(lambda:prepare(self.b,self.c,self.plan['path'],'source.other','a'*64))
    def test_stale(self):
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,[self.receipt],66,67,70,71))
    def test_pending(self):
        self.manifest['pending']=['pending.x']
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,[self.receipt],62,63,66,67))
    def test_missing_receipt(self):
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,[],62,63,66,67))
    def test_unverified_receipt(self):
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,[self.plan],62,63,66,67))
    def test_route_overflow(self):
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,[self.receipt],62,63,67,68))
    def test_mismatch(self):
        self.checkpoint['completed_through']['printed_page']=60
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,[self.receipt],62,63,66,67))
    def test_duplicate_path(self):
        self.bad(lambda:authorize_advance(self.manifest,self.checkpoint,
            [self.receipt,self.receipt],62,63,66,67))

if __name__=='__main__': unittest.main()
