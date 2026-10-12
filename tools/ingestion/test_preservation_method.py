import copy
import json
from pathlib import Path
import tempfile
import unittest
import yaml
from connector_preflight import InvalidRecord, canonical, validate_pair, load_text
from ingestion_gate import prepare, confirm
from preservation_method import (MethodError, initial_candidate, compose, load_stage,
                                 record_failure, decide, verify_source_pdf, digest, git_blob)

HASH = 'a'*64
COMMIT = 'b'*40
REJECTION = "This tool call was blocked by OpenAI's safety checks."

class PreservationMethodTests(unittest.TestCase):
    def setUp(self):
        self.root_tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.root_tmp.name)
        self.baseline = self.root/'baseline.yml'
        self.candidate = self.root/'candidate.yml'
        self.journal = self.root/'journal'
        self.record = {
            'id':'npc.example.source_history', 'record_type':'historical_world_profile',
            'status':'source_reviewed', 'source':'source.test',
            'printed_pages':'10-11','pdf_pages':'11-12','edition_scope':'SR2 historical',
            'content_class':['world_fact'],
            'data': {'person':'Example', 'events': [
                {'subject':'individual', 'action':'investigated', 'assertion':'arson involving children'},
                {'subject':'individual', 'action':'allegedly accepted', 'assertion':'targeted killing contracts'}],
                'claim':{'speaker':'Observer', 'certainty':'alleged', 'negated':True,
                         'voluntary':False},
                'rules':{'target_number':4,'modifier':'+2','damage':'6M'}}
        }
        self.baseline.write_text(yaml.safe_dump(self.record,sort_keys=False),encoding='utf-8')
    def tearDown(self):
        self.root_tmp.cleanup()
    def stage(self):
        if not self.candidate.exists():
            compose(self.baseline,self.candidate)
        plan=prepare(self.baseline,self.candidate,'world/fiction/test.yml','source.test',HASH)
        self.journal.mkdir()
        (self.journal/'baseline.yml').write_bytes(self.baseline.read_bytes())
        (self.journal/'candidate.yml').write_bytes(self.candidate.read_bytes())
        (self.journal/'plan.json').write_text(json.dumps(plan),encoding='utf-8')
        return plan
    def test_verify_source_uses_actual_fresh_bytes_and_live_manifest(self):
        pdf=self.root/'source.pdf'
        pdf.write_bytes(b'%PDF-1.7\nsynthetic test data\n%%EOF')
        manifest=self.root/'manifest.yml'
        manifest.write_text(yaml.safe_dump({'id':'source.test','source_pdf_sha256':digest(pdf.read_bytes())}))
        self.assertEqual(verify_source_pdf(pdf,manifest)['status'],'source_pdf_hash_verified')
        pdf.write_bytes(pdf.read_bytes()+b'changed')
        with self.assertRaisesRegex(MethodError,'fresh_source_pdf_sha256_mismatch'):
            verify_source_pdf(pdf,manifest)
    def test_first_pass_preserves_all_substance_and_claim_provenance(self):
        original=load_text(self.baseline.read_text())
        candidate=initial_candidate(original)
        self.assertEqual(candidate['data'],original['data'])
        self.assertEqual(validate_pair(original,candidate)['status'],'pass')
        self.assertEqual(candidate['content_class'],['world_fact'])
        self.assertEqual(candidate['framing'],'newsroom_neutral')
        self.assertIn('arson involving children',str(candidate['data']))
        self.assertIn('targeted killing contracts',str(candidate['data']))
        self.assertEqual(candidate['data']['rules']['damage'],'6M')
    def test_protected_mechanics_choose_reference_exact(self):
        self.record['content_class']=['rule_exact']
        c=initial_candidate(self.record)
        self.assertEqual(c['framing'],'reference_exact')
        self.assertEqual(c['data']['rules'],self.record['data']['rules'])
    def test_preserve_existing_presentation_by_default(self):
        self.record['headline']='A source-reviewed person'
        self.record['summary']='Existing source-reviewed context retained.'
        c=initial_candidate(self.record)
        self.assertEqual(c['headline'],self.record['headline'])
        self.assertEqual(c['summary'],self.record['summary'])
    def test_refuse_mixed_classes(self):
        self.record['content_class']=['world_fact','rule_exact']
        with self.assertRaises(InvalidRecord): initial_candidate(self.record)
    def test_refuse_empty_structured_data(self):
        self.record['data']={}
        with self.assertRaises(InvalidRecord): initial_candidate(self.record)
    def test_compose_never_overwrites_existing_candidate(self):
        compose(self.baseline,self.candidate)
        unchanged=self.candidate.read_bytes()
        with self.assertRaises(FileExistsError):compose(self.baseline,self.candidate)
        self.assertEqual(self.candidate.read_bytes(),unchanged)
    def test_stage_is_actual_prepare_plan(self):
        plan=self.stage()
        loaded,_=load_stage(self.journal)
        self.assertEqual(loaded['immutable_sha256'],plan['immutable_sha256'])
        self.assertEqual(loaded['candidate_sha256'],digest(self.candidate.read_bytes()))
        self.assertEqual(loaded['expected_blob_sha'],git_blob(self.candidate.read_bytes()))
    def test_missing_journal_cannot_be_invented(self):
        with self.assertRaisesRegex(MethodError,'missing_or_invalid_journal'):
            load_stage(self.root/'missing')
    def test_staged_payload_mutation_rejected(self):
        self.stage()
        (self.journal/'candidate.yml').write_bytes(self.candidate.read_bytes()+b'\n')
        with self.assertRaisesRegex(MethodError,'staged_candidate_bytes_changed'):
            load_stage(self.journal)
    def test_staged_fact_mutation_rejected(self):
        self.stage()
        baseline=load_text((self.journal/'baseline.yml').read_text())
        baseline['data']['rules']['target_number']=7
        (self.journal/'baseline.yml').write_text(yaml.safe_dump(baseline),encoding='utf-8')
        with self.assertRaises(InvalidRecord):load_stage(self.journal)
    def test_unknown_remote_never_assumed_absent(self):
        self.stage()
        self.assertEqual(decide(self.journal)['decision'],'fresh_readback_required')
    def test_first_write_requires_real_remote_absence_evidence(self):
        self.stage()
        self.assertEqual(decide(self.journal,remote_absent=True)['decision'],
                         'first_normal_github_contents_write_permitted')
    def test_ambiguous_denial_recorded_without_invented_http_status(self):
        self.stage()
        v=record_failure(self.journal,'create',REJECTION,None,False)
        self.assertEqual(v['category'],'ambiguous_tool_layer_rejection')
        self.assertIsNone(v['github_http_status'])
        self.assertEqual(decide(self.journal,remote_absent=True)['decision'],
                         'defer_identical_payload_review_actual_error_and_source')
        record_failure(self.journal,'create',REJECTION,None,False)
        self.assertEqual(len(json.loads((self.journal/'write_attempts.json').read_text())),1)
    def test_explicit_restriction_must_stop(self):
        self.stage()
        record_failure(self.journal,'create','Explicit restriction',403,True)
        self.assertEqual(decide(self.journal,remote_absent=True)['decision'],
                         'stop_preserve_pending_explicit_restriction')
    def test_stale_sha_requires_fresh_state(self):
        self.stage()
        record_failure(self.journal,'update','SHA mismatch',409,False)
        self.assertEqual(decide(self.journal,remote_absent=True)['decision'],
                         'refresh_current_sha_then_normal_update')
    def test_provider_denial_not_translated_into_content_guess(self):
        self.stage()
        record_failure(self.journal,'create','Forbidden',403,False)
        self.assertEqual(decide(self.journal,remote_absent=True)['decision'],
                         'check_permissions_no_alternate_api')
    def test_blob_readback_takes_precedence_over_old_ambiguous_error(self):
        plan=self.stage()
        record_failure(self.journal,'create',REJECTION,None,False)
        result=decide(self.journal,observed_blob=plan['expected_blob_sha'],commit_sha=COMMIT)
        self.assertEqual(result['decision'],'run_actual_ingestion_gate_confirm')
        self.assertEqual(confirm(plan,self.candidate,COMMIT,plan['expected_blob_sha'])['status'],'verified')
    def test_divergent_blob_never_overwrite(self):
        self.stage()
        self.assertEqual(decide(self.journal,observed_blob='c'*40)['decision'],
                         'divergent_remote_blob_investigate_no_overwrite')
    def test_invalid_or_conflicting_evidence_rejected(self):
        self.stage()
        with self.assertRaisesRegex(MethodError,'conflicting_remote_evidence'):
            decide(self.journal, remote_absent=True,observed_blob='c'*40)
        with self.assertRaisesRegex(MethodError,'invalid_commit_sha'):
            decide(self.journal,observed_blob='c'*40,commit_sha='abc')
        with self.assertRaisesRegex(MethodError,'commit_without_blob'):
            decide(self.journal,commit_sha=COMMIT)

if __name__=='__main__':unittest.main()
