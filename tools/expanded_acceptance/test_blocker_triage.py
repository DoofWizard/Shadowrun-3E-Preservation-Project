"""Synthetic prerequisite reports only, never source or historical evidence."""
import base64
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from blocker_triage import scan, load_pinned


def b64(data):
    return base64.b64encode(data).decode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


class TriageTests(unittest.TestCase):
    def setUp(self):
        self.field={'id':'a','heading':'Table row','class':'rule_exact','kind':'row','lineage':'sr3_effective','value':4}
        self.review={'protocol':'sr3-expanded-acceptance/v1','reviewer':'synthetic R','source':{'id':'source.demo','sha256':'a'*64,'manifest':'sources/manifests/demo.yml','catalog':'DEMO','publisher':'Test','edition':'SR3','physical_pages':2},'unresolved_fields':[],'unrepresented_printed':[],'expected_printed_folios':[1],'contradictions':[],'pages':[{'pdf':1,'printed':None,'heading':'front','image_review':'fixture','disposition':'zero_rules','reason':'art','fields':[]},{'pdf':2,'printed':1,'heading':'Table','image_review':'fixture','disposition':'mechanical','fields':[self.field]}]}
        self.bindings={'a':{'path':'rules/demo.yml','pointer':'/data/tn'}}
        self.journal={'baseline':{'bytes_base64':b64(b'a')},'candidate':{'bytes_base64':b64(b'b')},'plan':{'bytes_base64':b64(b'c')}}
        self.tx={'plan':{'status':'preflighted'},'confirm':{'status':'verified'},'baseline_sha256':'a'*64,'prewrite_journal_artifact':self.journal,'historical_confirm_artifact':{'x':1},'editorial_review_artifact':{'x':1},'index_commit':'b'*40,'index_pointer':'/verified/0'}
        self.evidence={'protocol':'sr3-expanded-acceptance/v1','custodian':'synthetic C','transactions':{'rules/demo.yml':self.tx}}

    def test_all_obvious_prerequisites_present_is_still_only_triage(self):
        r=scan(self.review,self.bindings,self.evidence)
        self.assertEqual(r['blocker_counts'],{})
        self.assertEqual(r['status'],'TRIAGE_ONLY')
        self.assertFalse(r['formal_acceptance'])

    def test_all_missing_historical_artifacts_are_reported_together(self):
        del self.tx['confirm']; del self.tx['index_commit']; del self.journal['candidate']
        r=scan(self.review,self.bindings,self.evidence)
        codes={i['code'] for i in r['blockers']}
        self.assertIn('missing_historical_confirm',codes)
        self.assertIn('missing_historical_index_commit',codes)
        self.assertIn('missing_original_prewrite_candidate',codes)

    def test_bad_source_page_and_binding_rejections_aggregate(self):
        self.review['pages'][1]['fields']=[]
        self.bindings['b']=self.bindings['a']
        r=scan(self.review,self.bindings,self.evidence)
        c={i['code'] for i in r['blockers']}
        self.assertIn('mechanical_page_has_no_original_derived_fields',c)
        self.assertIn('binding_not_justified_by_original_source',c)

    def test_cross_source_never_passes_silently(self):
        self.bindings['a']['mode']='external_equivalence'
        self.assertIn('equivalence',scan(self.review,self.bindings,self.evidence)['blocker_counts'])

    def test_split_archives_bad_and_missing_pins_aggregate(self):
        self.evidence['transactions']['rules/demo.yml']={'layout':'split_archive/v1','pre_base64':b64(b'a'),'pre_sha256':sha(b'not a'),'post_base64':b64(b'b'),'post_sha256':sha(b'b')}
        codes={i['code'] for i in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('missing_split_archive_attestation_base64',codes)
        self.assertIn('missing_split_archive_attestation_sha256',codes)
        self.assertIn('split_archive_pin_mismatch_pre_base64',codes)

    def test_required_original_pages_and_fields_never_inferred(self):
        self.review['pages']=[]
        errors={i['code'] for i in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('finite_original_page_inventory_missing',errors)
        self.assertIn('physical_page_coverage_unproven',errors)

    def test_independent_input_pin(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'review.json'; raw=json.dumps(self.review).encode(); p.write_bytes(raw)
            self.assertEqual(load_pinned(p,sha(raw)),self.review)
            with self.assertRaises(ValueError):load_pinned(p,'0'*64)

    def test_missing_folio_and_contradiction_inventories(self):
        del self.review['expected_printed_folios']
        del self.review['contradictions']
        codes={i['code'] for i in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('expected_printed_folios_not_reconciled',codes)
        self.assertIn('explicit_contradiction_inventory_missing',codes)

    def test_unreviewed_legacy_equivalence_blocked(self):
        self.review['source']['edition']='SR2'
        self.field['lineage']='sr2_superseded'
        codes={i['code'] for i in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('sr2_precedence_or_named_successor_unresolved',codes)

    def test_zero_rules_without_reason_flagged(self):
        del self.review['pages'][0]['reason']
        codes={i['code'] for i in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('no_rule_page_not_justified',codes)

    def test_omission_requires_explicit_authority(self):
        p=self.review['pages'][0]
        p.update(disposition='owner_omission',reason='source gap')
        codes={i['code'] for i in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('omission_lacks_owner_authority',codes)

    def test_orphan_transaction_is_not_silent(self):
        self.evidence['transactions']['rules/orphan.yml']=copy.deepcopy(self.tx)
        codes={i['code'] for i in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('orphan_transaction_not_bound_to_original_field',codes)



    def test_accepted_core_reference_without_independent_proof(self):
        self.bindings['a'].update(mode='sr3-accepted-core-equivalence/v1', core_obligation='obligation.core.a')
        self.evidence['transactions']={}
        errors={e['code'] for e in scan(self.review,self.bindings,self.evidence)['blockers']}
        self.assertIn('accepted_core_receipt_proof_missing',errors)
        self.assertIn('independent_original_page_comparison_missing',errors)
        self.assertNotIn('no_accepted_transaction_evidence',errors)

    def test_accepted_core_reference_is_only_triage_candidate(self):
        self.bindings['a'].update(mode='sr3-accepted-core-equivalence/v1', core_obligation='obligation.core.a')
        self.evidence['transactions']={}
        self.evidence['accepted_core_equivalence']={
            'protocol':'sr3-accepted-core-equivalence/v1',
            'receipt_commit':'a'*40, 'receipt_blob':'b'*40,
            'comparisons':{'a':{'reviewer':'fixture'}}}
        r=scan(self.review,self.bindings,self.evidence)
        self.assertEqual(r['status'],'TRIAGE_ONLY')
        self.assertEqual(r['blocker_counts'],{})
        self.assertFalse(r['formal_acceptance'])

if __name__=='__main__':
    unittest.main()
