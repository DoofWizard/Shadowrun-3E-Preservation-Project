"""Synthetic negative tests for reference-only Companion Actions p130.

The SR3 core p105 qualifications stay authoritative; these tests never certify
an original page, a historical transaction, or a sourcebook.
"""
import json
import unittest
import test_core_equivalence as fixtures
from core_equivalence import (CORE_RECEIPT, CORE_QUEUE, CORE_MANIFEST, CORE_SHA,
                              PROTOCOL, git_blob)


class ActionIndexReferenceTests(unittest.TestCase):
    def setUp(self):
        f = fixtures.CoreEquivalenceTests(methodName='test_match_is_not_acceptance')
        f.setUp()
        self.f = f
        f.source['sha256'] = '8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5'
        f.field.update({'id':'comp.actions.free.general.1',
                        'heading':'Actions / Free / General',
                        'class':'rule_procedure',
                        'kind':'row',
                        'lineage':'sr3_effective',
                        'value':'Activate Cyberware'})
        f.path = 'rules/actions/sr3-core-combat-phase-action-timing-p104-108.yml'
        f.obligation = 'obligation.rule.actions.sr3-core-combat-phase-action-timing-p104-108.selected_free_actions'
        f.record = {'id':'rule.actions.sr3-core-combat-phase-action-timing-p104-108',
                    'source':'source.sr3-core','content_class':['rule_procedure'],
                    'data':{'selected_free_actions':[
                        {'action':'Activate Cyberware',
                         'condition':'Cyberware without continuous active control.'},
                        {'action':'Observe',
                         'condition':'Only immediately obvious information; detail requires a Simple Action.'},
                        {'action':'Speak a Word',
                         'condition':'Beyond one word, dialogue is at gamemaster discretion.'}]}}
        f.binding={'mode':PROTOCOL, 'path':f.path,
                   'pointer':'/data/selected_free_actions/0/action',
                   'core_obligation':f.obligation}
        f.manifest['postscan_verified_mechanics_recovery']['verified_semantic_records']=[
            {'id':f.record['id'], 'path':f.path, 'blob':git_blob(fixtures.dump(f.record)), 'gate':'verified'}]
        f.queue['core_acceptance_inventory']['bindings']={f.obligation:{
            'record_id':f.record['id'], 'record_pointer':'/data/selected_free_actions'}}
        self.d = {'source_field_id':f.field['id'], 'core_obligation':f.obligation,
            'source_id':f.source['id'], 'source_sha256':f.source['sha256'],
            'core_source_sha256':CORE_SHA, 'source_printed':130,'source_pdf':131,
            'original_heading':f.field['heading'], 'lineage':f.field['lineage'],
            'relation':'indexed_action_reference', 'indexed_action_class':'Free',
            'indexed_action_group':'General', 'appendix_is_reference_only':True,
            'no_new_or_conflicting_rules_on_appendix_page':True,
            'preserve_core_conditions_without_weakening':True,
            'rule_scope':'core_procedure_controls',
            'conditions':'core_conditions_preserved',
            'exceptions':'core_exceptions_preserved',
            'optional_status':'core_status_preserved',
            'core_condition_pointer':'/data/selected_free_actions/0/condition',
            'full_core_condition':f.record['data']['selected_free_actions'][0]['condition'],
            'accepted_core_group_pointer':'/data/selected_free_actions',
            'reviewed_subfield_pointer':'/data/selected_free_actions/0/action',
            'core_group_original_review':'Synthetic core p105 image read',
            'reviewer':'independent third reviewer',
            'source_image_review':'synthetic FASA7905a p130 image',
            'core_image_review':'synthetic FASA7001 p105 image'}
        f.proof['comparisons'] = {f.field['id']:self.d}
        self.refresh()

    def refresh(self):
        f = self.f
        raw = fixtures.dump(f.record)
        mr, qr = fixtures.dump(f.manifest), fixtures.dump(f.queue)
        f.receipt['assessment']['manifest_blob']=git_blob(mr)
        f.receipt['assessment']['closure_queue_blob']=git_blob(qr)
        rr=json.dumps(f.receipt).encode()
        f.proof.update(receipt_blob=git_blob(rr))
        f.git.bytes[(f.commit, f.path)] = raw
        f.git.bytes[(f.git.head, f.path)] = raw
        f.git.bytes[(f.commit, CORE_MANIFEST)] = mr
        f.git.bytes[(f.commit, CORE_QUEUE)] = qr
        f.git.bytes[(f.commit, CORE_RECEIPT)] = rr

    def set_action(self, idx):
        f=self.f
        row=f.record['data']['selected_free_actions'][idx]
        f.field['value']=row['action']
        f.binding['pointer']=f'/data/selected_free_actions/{idx}/action'
        self.d.update(core_condition_pointer=f'/data/selected_free_actions/{idx}/condition',
                      full_core_condition=row['condition'],
                      reviewed_subfield_pointer=f'/data/selected_free_actions/{idx}/action')
        self.refresh()

    def test_activate_cyberware_index_reference_only(self):
        v=self.f.run_it()
        self.assertEqual(v['status'],'CORE_ACTION_INDEX_REFERENCE_CANDIDATE')
        self.assertFalse(v['formal_acceptance'])

    def test_observe_index_reference_only(self):
        self.set_action(1)
        self.assertEqual(self.f.run_it()['status'],'CORE_ACTION_INDEX_REFERENCE_CANDIDATE')

    def test_speak_word_index_reference_only(self):
        self.set_action(2)
        self.assertEqual(self.f.run_it()['status'],'CORE_ACTION_INDEX_REFERENCE_CANDIDATE')

    def test_rejects_original_page_mismatch(self):
        self.f.original_page['pdf']=132
        self.f.reject()

    def test_rejects_previous_erroneous_companion_digest(self):
        # The former fixture duplicated the adapter's typo; original PDF verification
        # now pins the genuine digest and must reject the previous value.
        wrong = '8c52409108459a130ff6292722d98dc1f7a65cf870e63a363c34dc1dc299afd5'
        self.f.source['sha256'] = wrong
        self.d['source_sha256'] = wrong
        self.f.reject()

    def test_rejects_other_companion_action_not_reviewed(self):
        self.f.field['value']='Observe in Detail'
        self.f.reject()

    def test_rejects_different_action_class(self):
        self.d['indexed_action_class']='Simple'
        self.f.reject()

    def test_rejects_source_adding_exception(self):
        self.d['no_new_or_conflicting_rules_on_appendix_page']=False
        self.f.reject()

    def test_rejects_dropped_core_qualification(self):
        self.d['full_core_condition']='Any cyberware can be activated in free action'
        self.f.reject()

    def test_rejects_missing_original_group_review(self):
        self.d['core_group_original_review']=''
        self.f.reject()

    def test_rejects_wrong_source(self):
        self.f.source['id']='source.elsewhere'
        self.f.reject()

    def test_rejects_unaccepted_core_group_pointer(self):
        self.f.binding['pointer']='/data/other_actions/0/action'
        self.f.reject()

    def test_rejects_supplement_rule_override(self):
        self.d['conditions']='sourcebook_replaces_core'
        self.f.reject()

    def test_rejects_implied_automatic_acceptance(self):
        self.assertTrue(self.f.run_it()['independent_review_still_required'])
        self.assertFalse(self.f.run_it()['original_source_page_authorized'])


if __name__=='__main__':
    unittest.main()
