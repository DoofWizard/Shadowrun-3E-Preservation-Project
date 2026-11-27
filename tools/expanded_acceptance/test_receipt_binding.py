"""Synthetic Git and actual gate integration; no production acceptance evidence."""
import base64
import copy
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

import yaml
from archive_adapter import blob, sha
from validator import Git, PROTOCOL, assess


def archive(entries):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        for name, raw in entries.items():
            z.writestr(name, raw)
    return out.getvalue()


def j(v):
    return json.dumps(v, sort_keys=True).encode()


def b64(raw):
    return base64.b64encode(raw).decode()


class ReceiptBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Synthetic fixture')
        gates = Path(os.environ.get('SR3_INGESTION_DIR', Path(__file__).resolve().parents[1]/'ingestion'))
        for n in ('ingestion_gate.py', 'connector_preflight.py', 'preservation_method.py'):
            self.write('tools/ingestion/'+n, (gates/n).read_bytes())
        self.commit('fixture gates')
        self.path = 'rules/test/example.yml'
        self.mp = 'sources/manifests/TEST.yml'
        self.source = {'id':'source.test', 'sha256':'a'*64, 'edition':'SR3', 'catalog':'TEST', 'publisher':'Fixture', 'physical_pages':1, 'manifest':self.mp}
        record = {'id':'rule.test', 'source':'source.test', 'record_type':'rule', 'status':'ingested', 'printed_pages':'1', 'pdf_pages':'1', 'edition_scope':'SR3', 'content_class':['rule_exact'], 'framing':'reference_exact', 'data':{'tn':4}}
        raw = yaml.safe_dump(record).encode()
        self.write(self.path, raw)
        scratch = self.root/'baseline.yml'
        scratch.write_bytes(raw)
        gate = self.root/'tools/ingestion/ingestion_gate.py'
        plan = json.loads(subprocess.check_output([sys.executable, str(gate), 'prepare', str(scratch), str(self.root/self.path), self.path, self.source['id'], self.source['sha256']]))
        semantic = self.commit('synthetic semantic write')
        self.semantic = semantic
        plan_path = self.root/'plan.json'
        plan_path.write_bytes(j(plan))
        receipt = json.loads(subprocess.check_output([sys.executable, str(gate), 'confirm', str(plan_path), str(self.root/self.path), semantic, blob(raw)]))
        reg = {'source_id':self.source['id'], 'original_pdf_sha256':self.source['sha256'], 'record_id':record['id'], 'record_path':self.path, 'current_commit':semantic, 'current_blob':blob(raw), 'baseline_sha256':sha(raw), 'candidate_sha256':sha(raw), 'immutable_sha256':plan['immutable_sha256'], 'gate':'verified', 'actual_confirm':'verified', 'content_class':'rule_exact'}
        self.manifest = {'id':self.source['id'], 'source_pdf_sha256':self.source['sha256'], 'edition':'SR3', 'catalog_number':'TEST', 'publisher':'Fixture', 'registration':reg}
        mr = yaml.safe_dump(self.manifest).encode()
        self.write(self.mp, mr)
        index = self.commit('synthetic index write')
        self.index = index
        self.head = index
        self.pre = {'journal/baseline.yml':raw, 'journal/candidate.yml':raw, 'journal/plan.json':j(plan), 'source-review.txt':b'Synthetic review, no real source evidence.'}
        self.post = {**self.pre, 'journal/verified.json':j(receipt), 'journal/readback-receipt.json':j({'commit':semantic, 'blob':blob(raw), 'candidate_bytes':len(raw), 'exact_commit_live_bytes':True}), 'journal/index-receipt.json':j({'commit':index, 'blob':blob(mr), 'exact_commit_live_bytes':True, 'path':self.mp, 'registration_key':'registration'}), 'journal/indexed-manifest.yml':mr}
        self.att = {'protocol':'sr3-expanded-editorial-binding/v1', 'source':self.source['id'], 'source_sha256':self.source['sha256'], 'edition':'SR3', 'publisher':'Fixture', 'catalog':'TEST', 'path':self.path, 'record_id':record['id'], 'printed_pages':'1', 'pdf_pages':'1', 'reviewed_edition_scope':'SR3', 'content_class':['rule_exact'], 'baseline_sha256':sha(raw), 'candidate_sha256':sha(raw), 'historical_review_sha256':sha(self.pre['source-review.txt']), 'semantic_commit':semantic, 'index_commit':index, 'baseline_reviewed_independently':True, 'candidate_reviewed_independently':True, 'nested_text_reviewed':True, 'historical_custody_and_chronology_reviewed':True, 'reviewer':'fixture third reviewer', 'original_review_locator':'fixture only'}
        self.review = {'protocol':PROTOCOL, 'reviewer':'fixture inventory', 'source':self.source, 'unresolved_fields':[], 'pages':[{'pdf':1, 'printed':1, 'heading':'Fixture', 'image_review':'fixture image', 'disposition':'mechanical', 'fields':[{'id':'tn', 'heading':'Fixture', 'class':'rule_exact', 'kind':'rule', 'lineage':'sr3_effective', 'value':4}]}], 'unrepresented_printed':[], 'expected_printed_folios':[1], 'contradictions':[]}
        self.bindings = {'tn':{'path':self.path,'pointer':'/data/tn'}}

    def git(self, *args):
        return subprocess.check_output(['git','-C',str(self.root),*args],stderr=subprocess.PIPE).decode().strip()

    def write(self, path, raw):
        p = self.root/path
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(raw)
        self.git('add',path)

    def commit(self, msg):
        self.git('commit','-qm',msg)
        return self.git('rev-parse','HEAD')

    def run_assess(self, alter=None):
        pre, post = archive(self.pre), archive(self.post)
        self.att.update(pre_sha256=sha(pre), post_sha256=sha(post))
        att = j(self.att)
        e = {'layout':'split_archive/v1','pre_base64':b64(pre),'post_base64':b64(post),'pre_sha256':sha(pre),'post_sha256':sha(post),'attestation_base64':b64(att),'attestation_sha256':sha(att)}
        if alter:
            alter(e)
        return assess(Git(self.root,self.head), self.review, self.bindings, {'protocol':PROTOCOL,'custodian':'fixture custodian','transactions':{self.path:e}},self.source['sha256'],1)

    def test_positive_actual_gates(self):
        r = self.run_assess()
        self.assertEqual(r['status'],'PASS')
        self.assertFalse(r['formal_acceptance'])
        self.assertTrue(r['archive_diagnostics'][self.path]['present_day_confirm_rechecked'])

    def test_changed_live_record(self):
        self.write(self.path,self.pre['journal/candidate.yml']+b'\n')
        self.head = self.commit('changed record')
        with self.assertRaisesRegex(ValueError,'archive_exact_git_bytes_mismatch'):
            self.run_assess()

    def test_changed_live_registration(self):
        self.manifest['registration']['actual_confirm'] = 'unknown'
        self.write(self.mp,yaml.safe_dump(self.manifest).encode())
        self.head = self.commit('changed registration')
        with self.assertRaisesRegex(ValueError,'archive_live_registration_changed'):
            self.run_assess()

    def test_wrong_edition(self):
        self.att['edition'] = 'SR2'
        with self.assertRaisesRegex(ValueError,'archive_editorial_binding_mismatch'):
            self.run_assess()

    def test_wrong_review_digest(self):
        self.att['historical_review_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError,'archive_editorial_binding_mismatch'):
            self.run_assess()

    def test_same_reviewer(self):
        self.att['reviewer'] = self.review['reviewer']
        with self.assertRaisesRegex(ValueError,'archive_independent_attestation_required'):
            self.run_assess()

    def test_missing_confirm(self):
        del self.post['journal/verified.json']
        with self.assertRaisesRegex(ValueError,'unsupported_or_missing_archive_members'):
            self.run_assess()

    def test_wrong_attestation_pin(self):
        with self.assertRaisesRegex(ValueError,'editorial_attestation_pin_mismatch'):
            self.run_assess(lambda e:e.update(attestation_sha256='0'*64))

    def test_typed_mismatch(self):
        self.review['pages'][0]['fields'][0]['value'] = '4'
        with self.assertRaisesRegex(ValueError,'typed_field_mismatch'):
            self.run_assess()

    def test_unindexed_head(self):
        self.head = self.semantic
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_assess()

    def test_unknown_layout(self):
        with self.assertRaisesRegex(ValueError,'unsupported_transaction_layout'):
            self.run_assess(lambda e:e.update(layout='unknown'))


if __name__ == '__main__':
    unittest.main()
