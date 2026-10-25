"""Source-specific preservation gate regression: FASA7116 color-plate interleaf.

No connector calls or production data mutations. Tests fail closed on wrong
source, missing plates, wrong source hash and mis-mapped semantic receipts.
"""
import copy
import unittest
from ingestion_gate import authorize_advance, InvalidRecord
from transaction_recovery import authorize, RecoveryError

PDF_SHA='85656be71abc5583b671cc1613c12c07db77239611a90cbb95f4faa168ec1d30'

def fixture():
    m={'id':'source.fasa-7116','status':'ingesting','done':{'p':63,'pdf':64},
       'next':{'p':64,'pdf':65},'pending':[],'routes':[[8,78,'directed_deep_npc_stats']],
       'source_pdf_sha256':PDF_SHA,'records':[],
       'source_integrity':{'page_mapping':'printed_plus_one_through_p64; eight_unnumbered_color_plates_at_pdf66-73; printed_plus_nine_from_p65_to_at_least_p75',
                           'visually_checked_mapping':{'printed_64':65,'printed_65':74,'unnumbered_color_plates_pdf':[66,73]}},
       'verified_ahead_of_contiguous_boundary':[
           {'path':'references/prime-runners/unnumbered-color-plates-visual-index-pdf66-73.yml','range_printed':[],'range_pdf':[66,73],'gate':'verified'},
           {'path':'world/prime-runners/unnumbered-color-plates-character-voices-pdf67-73.yml','range_printed':[],'range_pdf':[67,73],'gate':'verified'}]}
    c={'active_source':'source.fasa-7116','completed_through':{'printed_page':63,'pdf_page':64},
       'resume_at':{'printed_page':64,'pdf_page':65},'pending_normalization':[],'open_conflicts':[]}
    def receipt(path,printed,pdf,n):
        return {'protocol':'sr3-gate/v1','status':'verified','source':'source.fasa-7116',
                'path':path,'printed_pages':str(printed),'pdf_pages':str(pdf),
                'pdf_sha256':PDF_SHA,'commit_sha':str(n)*40,'expected_blob_sha':str(n+2)*40,
                'readback_blob_sha':str(n+2)*40}
    rr=[receipt('world/prime-runners/test-profile-p64.yml',64,65,1),
        receipt('references/prime-runners/test-hooks-p65.yml',65,74,2)]
    return m,c,rr

class ColorPlateTests(unittest.TestCase):
    def gate(self,m,c,rr,next_printed=66,next_pdf=75):
        return authorize_advance(m,c,rr,64,65,next_printed,next_pdf)
    def recovery(self,m,c,rr,next_printed=66,next_pdf=75):
        return authorize(m,c,rr,'pending.synthetic',64,65,next_printed,next_pdf,[r['path'] for r in rr])
    def test_approved_transition(self):
        m,c,rr=fixture()
        self.assertTrue(self.gate(m,c,rr)['authorized'])
        self.assertTrue(self.recovery(m,c,rr)['authorized'])
    def test_missing_color_plate_evidence(self):
        m,c,rr=fixture();m['verified_ahead_of_contiguous_boundary'].pop()
        with self.assertRaises(InvalidRecord):self.gate(m,c,rr)
        with self.assertRaises(RecoveryError):self.recovery(m,c,rr)
    def test_bad_offset(self):
        m,c,rr=fixture();rr[1]['pdf_pages']='66'
        with self.assertRaises(InvalidRecord):self.gate(m,c,rr)
        with self.assertRaises(RecoveryError):self.recovery(m,c,rr)
    def test_wrong_next_page(self):
        m,c,rr=fixture()
        with self.assertRaises(InvalidRecord):self.gate(m,c,rr,66,67)
        with self.assertRaises(RecoveryError):self.recovery(m,c,rr,66,67)
    def test_missing_source_hash(self):
        m,c,rr=fixture();m['source_pdf_sha256']='0'*64
        with self.assertRaises(InvalidRecord):self.gate(m,c,rr)
        with self.assertRaises(RecoveryError):self.recovery(m,c,rr)
    def test_non_source_rejected(self):
        m,c,rr=fixture();m['id']=c['active_source']='source.another'
        for r in rr:r['source']='source.another'
        with self.assertRaises(InvalidRecord):self.gate(m,c,rr)
        with self.assertRaises(RecoveryError):self.recovery(m,c,rr)
    def test_record_spanning_interleaf_rejected(self):
        m,c,rr=fixture();rr[0]['printed_pages']='64-65';rr[0]['pdf_pages']='65-74'
        with self.assertRaises(InvalidRecord):self.gate(m,c,rr)
        with self.assertRaises(RecoveryError):self.recovery(m,c,rr)

if __name__=='__main__':unittest.main()
