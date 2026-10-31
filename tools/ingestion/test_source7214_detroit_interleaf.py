"""Regression for the catalog-hash-bound unnumbered Target: UCAS Detroit plate.

Physical PDF48 has no printed folio between numbered pp46 (PDF47) and
48 (PDF49). Source 7214 must not invent a printed p47 or award page credit.
"""
import copy
import sys
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ingestion_gate import authorize_advance, InvalidRecord
from transaction_recovery import authorize, render_manifest, parse_yaml, RecoveryError

SOURCE_SHA='dc016e418a24fad63d56fba4f2f7f657cb1c0d995cdabd648ba9c6109e33f8f8'
PLATE_BLOB='13321b9fd88d11d9eba455877012704cb7d2ce17'
PLATE_COMMIT='a1d724413ab9dfb042d80d912ba29866b8bb5c76'
PATH='references/target-ucas/detroit-unnumbered-art-pdf48.yml'
RECORD_ID='reference.target_ucas.detroit.unnumbered_illustration_pdf48'


def fixture():
    manifest={
        'id':'source.fasa-7214','status':'ingesting','source_pdf_sha256':SOURCE_SHA,
        'done':{'p':46,'pdf':47},'next':{'p':47,'pdf':48},
        'pending':[],'resolved_pending':[],'open_conflicts':[],
        'records':[],'routes':[[46,67,'detroit']],
    }
    checkpoint={'active_source':'source.fasa-7214',
                'completed_through':{'printed_page':46,'pdf_page':47},
                'resume_at':{'printed_page':47,'pdf_page':48},
                'pending_normalization':[],'open_conflicts':[]}
    receipt={'protocol':'sr3-gate/v1','status':'verified','path':PATH,
             'printed_pages':'unnumbered illustration between printed 46 and 48',
             'pdf_pages':'48','source':'source.fasa-7214','pdf_sha256':SOURCE_SHA,
             'record_id':RECORD_ID,'expected_blob_sha':PLATE_BLOB,
             'readback_blob_sha':PLATE_BLOB,'commit_sha':PLATE_COMMIT}
    return manifest,checkpoint,receipt

class DetroitInterleaf(unittest.TestCase):
    def test_zero_page_advance_and_manifest(self):
        m,c,r=fixture()
        g=authorize_advance(m,c,[r],47,48,48,49)
        self.assertTrue(g['unnumbered_plate_only'])
        self.assertEqual(g['new_printed_pages'],0)
        self.assertEqual(g['to'],[46,48])
        a=authorize(m,c,[r],'detroit.unnumbered.verified',47,48,48,49,[PATH])
        self.assertEqual(a['new_printed_pages'],0)
        original=yaml.safe_dump(m,sort_keys=False)
        proposal=render_manifest(original,a,{PATH:RECORD_ID})
        parsed=parse_yaml(proposal)
        self.assertEqual(parsed['done'],{'p':46,'pdf':48})
        self.assertEqual(parsed['next'],{'p':48,'pdf':49})
        self.assertEqual(parsed['records'],[[RECORD_ID,PLATE_COMMIT]])
    def test_source_hash_is_required(self):
        m,c,r=fixture();m['source_pdf_sha256']='0'*64
        with self.assertRaises(InvalidRecord):authorize_advance(m,c,[r],47,48,48,49)
    def test_byte_specific_readback_required(self):
        m,c,r=fixture();r['readback_blob_sha']='1'*40
        with self.assertRaises(InvalidRecord):authorize_advance(m,c,[r],47,48,48,49)
    def test_reject_arbitrary_illustration(self):
        m,c,r=fixture();r['path']='references/target-ucas/other-art.yml'
        with self.assertRaises(InvalidRecord):authorize_advance(m,c,[r],47,48,48,49)
    def test_reject_invented_numbered_p47(self):
        m,c,r=fixture()
        with self.assertRaises(InvalidRecord):authorize_advance(m,c,[r],47,48,49,50)
    def test_reject_wrong_boundary(self):
        m,c,r=fixture();m['done']={'p':45,'pdf':46};c['completed_through']={'printed_page':45,'pdf_page':46}
        with self.assertRaises(InvalidRecord):authorize_advance(m,c,[r],47,48,48,49)

if __name__=='__main__':unittest.main()
