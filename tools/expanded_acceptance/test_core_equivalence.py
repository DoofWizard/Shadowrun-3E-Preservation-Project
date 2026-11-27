"""Synthetic adversarial contracts; never establishes real book acceptance."""
import copy
import json
import unittest
import yaml

from core_equivalence import (CORE_MANIFEST, CORE_QUEUE, CORE_RECEIPT,
    CORE_SHA, CORE_SOURCE, PROTOCOL, Blocked, git_blob, typed, verify)


class FakeGit:
    head = 'f' * 40

    def __init__(self):
        self.bytes = {}
        self.changed_paths = set()
        self.ancestry = set()

    def read(self, path, commit=None):
        return self.bytes[(commit or self.head, path)]

    def changed(self, path, commit):
        if (path, commit) not in self.changed_paths:
            raise Blocked('original_commit_did_not_change_receipt')

    def ancestor(self, old, head):
        if (old, head) not in self.ancestry:
            raise Blocked('core_acceptance_not_ancestor')


def dump(data):
    return yaml.safe_dump(data, sort_keys=False).encode()


class CoreEquivalenceTests(unittest.TestCase):
    def setUp(self):
        self.git = FakeGit()
        self.commit = 'a' * 40
        self.path = 'rules/tests/core.yml'
        self.obligation = 'obligation.rule.foo'
        self.source = {'id':'source.srcomp','sha256':'c'*64,'edition':'SR3'}
        self.original_page = {'pdf':131,'printed':130}
        self.field = {'id':'comp.action.001','heading':'Action reference / initiative',
            'class':'rule_exact','value':{'cost':'Simple','test':'Reaction'},'lineage':'sr3_effective'}
        self.binding={'mode':PROTOCOL,'path':self.path,'pointer':'/data/action',
            'core_obligation':self.obligation}
        self.record={'id':'rule.test.core','source':CORE_SOURCE,'content_class':['rule_exact'],
            'printed_pages':'102','pdf_pages':'103','data':{'action':copy.deepcopy(self.field['value'])}}
        self.manifest={'id':CORE_SOURCE,'source_pdf_sha256':CORE_SHA,
             'postscan_verified_mechanics_recovery':{'verified_semantic_records':[
                 {'id':self.record['id'],'path':self.path,'blob':git_blob(dump(self.record)),
                  'gate':'verified'}]}}
        self.queue={'core_acceptance_inventory':{'source':CORE_SOURCE,
            'independently_reviewed_original_headings_fields_and_classes':True,
            'unresolved_mechanical_fields':[],
            'bindings':{self.obligation:{'record_id':self.record['id'],
                                      'record_pointer':'/data/action'}}}}
        mr,qr=dump(self.manifest),dump(self.queue)
        self.receipt={'status':'verified_core_acceptance','source':CORE_SOURCE,
                      'assessment':{'status':'acceptance_evidence_validated',
                        'source_pdf_sha256':CORE_SHA,'authorized_printed_pages':0,
                        'manifest_blob':git_blob(mr),'closure_queue_blob':git_blob(qr)}}
        self.proof={'protocol':PROTOCOL,'core_source_id':CORE_SOURCE,
                    'original_pdf_sha256':CORE_SHA,'receipt_commit':self.commit,
                    'receipt_blob':git_blob(json.dumps(self.receipt).encode()),
                    'comparisons':{self.field['id']:{'source_field_id':self.field['id'],
                     'core_obligation':self.obligation,'source_id':self.source['id'],
                     'source_sha256':self.source['sha256'],'core_source_sha256':CORE_SHA,
                     'source_printed':130,'source_pdf':131,
                     'original_heading':self.field['heading'],'lineage':'sr3_effective',
                     'relation':'exact_restatement','rule_scope':'identical',
                     'conditions':'identical','exceptions':'identical','units':'identical',
                     'optional_status':'identical','reviewer':'independent third researcher',
                     'source_image_review':'fixture original p130 image',
                     'core_image_review':'fixture original core p102 image'}}}
        self.git.bytes[(self.commit,self.path)]=dump(self.record)
        self.git.bytes[(self.git.head,self.path)]=dump(self.record)
        self.git.bytes[(self.commit,CORE_MANIFEST)]=mr
        self.git.bytes[(self.commit,CORE_QUEUE)]=qr
        self.git.bytes[(self.commit,CORE_RECEIPT)]=json.dumps(self.receipt).encode()
        self.git.changed_paths.add((CORE_RECEIPT,self.commit))
        self.git.ancestry.add((self.commit,self.git.head))

    def run_it(self):
        return verify(self.git,self.source,self.field,self.original_page,
                      self.binding,self.proof,'inventory reviewer','receipt custodian')

    def reject(self):
        with self.assertRaises((Blocked, KeyError, IndexError)):
            self.run_it()

    def test_match_is_not_acceptance(self):
        r=self.run_it()
        self.assertEqual(r['status'],'CORE_FIELD_MATCH_CANDIDATE')
        self.assertFalse(r['formal_acceptance'])
        self.assertTrue(r['independent_review_still_required'])

    def test_same_number_different_type_refused(self):
        self.field['value']={'cost':'Simple','test':'4'}
        self.reject()

    def test_wrong_edition_refused(self):
        self.source['edition']='SR2'
        self.reject()

    def test_changed_or_unindexed_target_refused(self):
        self.manifest['postscan_verified_mechanics_recovery']['verified_semantic_records']=[]
        self.git.bytes[(self.commit,CORE_MANIFEST)]=dump(self.manifest)
        self.receipt['assessment']['manifest_blob']=git_blob(dump(self.manifest))
        self.git.bytes[(self.commit,CORE_RECEIPT)]=json.dumps(self.receipt).encode()
        self.proof['receipt_blob']=git_blob(self.git.bytes[(self.commit,CORE_RECEIPT)])
        self.reject()

    def test_modified_live_core_record_refused(self):
        self.git.bytes[(self.git.head,self.path)] += b'\n'
        self.reject()

    def test_fake_receipt_refused(self):
        self.receipt['status']='provisional'
        self.git.bytes[(self.commit,CORE_RECEIPT)]=json.dumps(self.receipt).encode()
        self.proof['receipt_blob']=git_blob(self.git.bytes[(self.commit,CORE_RECEIPT)])
        self.reject()

    def test_wrong_receipt_blob_refused(self):
        self.proof['receipt_blob']='0'*40
        self.reject()

    def test_missing_accepted_target_obligation_refused(self):
        self.binding['core_obligation']='obligation.not_accepted'
        self.reject()

    def test_different_target_pointer_refused(self):
        self.binding['pointer']='/data/other'
        self.reject()

    def test_optional_rule_not_auto_normalized(self):
        self.field['lineage']='sr3_optional'
        self.reject()

    def test_weaker_conditional_rule_never_equivalent(self):
        self.proof['comparisons'][self.field['id']]['conditions']='partially_overlap'
        self.reject()

    def test_missing_independent_original_review_refused(self):
        self.proof['comparisons'][self.field['id']]['source_image_review']=''
        self.reject()

    def test_same_reviewer_refused(self):
        self.proof['comparisons'][self.field['id']]['reviewer']='inventory reviewer'
        self.reject()

    def test_edition_variant_never_autoconverted(self):
        self.field['lineage']='preserved_variant'
        self.reject()

    def test_receipt_must_be_ancestor(self):
        self.git.ancestry.clear()
        self.reject()

    def test_unrelated_core_rules_not_valid_path(self):
        self.binding['path']='rules/tests/not-indexed.yml'
        self.reject()

    def test_original_source_binding_not_synthesized(self):
        self.proof['comparisons'][self.field['id']]['source_printed']=129
        self.reject()

if __name__=='__main__':unittest.main()
