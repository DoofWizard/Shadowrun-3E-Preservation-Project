#!/usr/bin/env python3
"""FASA7214 1997 historic source: only exact Chicago PDF70 art can cross unnumbered p69."""
from __future__ import annotations
import copy, pathlib, sys, unittest
import yaml
HERE=pathlib.Path(__file__).resolve()
sys.path.insert(0,str(HERE.parents[1]))
from ingestion_gate import source7214_chicago_interleaf, authorize_advance
from transaction_recovery import authorize, render_manifest, state, RecoveryError

SOURCE='dc016e418a24fad63d56fba4f2f7f657cb1c0d995cdabd648ba9c6109e33f8f8'
BLOB='7ea366fabfd32b543069765b55783162eb7a6d08'
COMMIT='5dc54cfb5d2a4922d9cf2dcb3c80707012ed30c9'
PATH='references/target-ucas/chicago-unnumbered-art-pdf70.yml'
RECEIPT={'path':PATH,'printed_pages':'unnumbered illustration between printed 68 and 70',
 'pdf_pages':'70','protocol':'sr3-gate/v1','status':'verified','source':'source.fasa-7214',
 'pdf_sha256':SOURCE,'readback_blob_sha':BLOB,'expected_blob_sha':BLOB,'commit_sha':COMMIT}
class ChicagoInterleaf(unittest.TestCase):
 def setUp(self):
  self.m={'id':'source.fasa-7214','status':'ingesting','source_pdf_sha256':SOURCE,
          'done':{'p':68,'pdf':69},'next':{'p':69,'pdf':70},'pending':[],
          'records':[],'resolved_pending':[],'verified_ahead_of_contiguous_boundary':[],
          'routes':[[68,85,'chicago']]}
  self.c={'active_source':'source.fasa-7214','completed_through':{'printed_page':68,'pdf_page':69},
          'resume_at':{'printed_page':69,'pdf_page':70},'pending_normalization':[],'open_conflicts':[]}
  self.r=[dict(RECEIPT)]
 def test_only_genuine_illustration_crosses(self):
  self.assertTrue(source7214_chicago_interleaf(self.m,69,70,70,71,self.r))
  x=authorize_advance(self.m,self.c,self.r,69,70,70,71)
  self.assertTrue(x['unnumbered_plate_only']);self.assertEqual(x['new_printed_pages'],0)
  z=authorize(self.m,self.c,self.r,'source7214.test.plate',69,70,70,71,[PATH]);self.assertEqual(z['new_printed_pages'],0)
 def test_wrong_source_or_readback_rejected(self):
  for field,value in [('pdf_sha256','0'*64),('expected_blob_sha','0'*40),('readback_blob_sha','0'*40),('commit_sha','nope'),('pdf_pages','69'),('printed_pages','69'),('path','references/other.yml'),('status','preflighted')]:
   r=[dict(RECEIPT)];r[0][field]=value
   with self.subTest(field=field):self.assertFalse(source7214_chicago_interleaf(self.m,69,70,70,71,r))
 def test_wrong_boundary_or_extra_record_rejected(self):
  for b in [(68,69,70,71),(69,70,71,72),(69,70,70,72),(69,71,70,72)]:
   with self.subTest(boundary=b):self.assertFalse(source7214_chicago_interleaf(self.m,*b,self.r))
  self.assertFalse(source7214_chicago_interleaf(self.m,69,70,70,71,self.r*2))
  m=copy.deepcopy(self.m);m['source_pdf_sha256']='0'*64
  self.assertFalse(source7214_chicago_interleaf(m,69,70,70,71,self.r))
 def test_manifest_render_zero_printed(self):
  import io
  txt=yaml.safe_dump(self.m,sort_keys=False)
  z=authorize(self.m,self.c,self.r,'source7214.test.plate',69,70,70,71,[PATH])
  txt2=render_manifest(txt,z,{PATH:'reference.target_ucas.chicago.unnumbered_art_pdf70'})
  m2=yaml.safe_load(txt2)
  self.assertEqual(m2['done'],{'p':68,'pdf':70})
  self.assertEqual(m2['next'],{'p':70,'pdf':71})
  self.assertEqual(m2['records'],[['reference.target_ucas.chicago.unnumbered_art_pdf70',COMMIT]])
  self.assertEqual(m2['routes'],self.m['routes'])
 def test_no_reinterpretation_as_numbered_page(self):
  r=[dict(RECEIPT)];r[0]['printed_pages']='69'
  with self.assertRaises(Exception):authorize_advance(self.m,self.c,r,69,70,70,71)
if __name__=='__main__': unittest.main()