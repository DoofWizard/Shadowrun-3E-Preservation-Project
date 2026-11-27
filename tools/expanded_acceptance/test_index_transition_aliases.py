"""Real local Git adversarial tests: register schema parity, never book acceptance."""
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from index_transition import verify


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\x00' + data).hexdigest()


def parse(data):
    return json.loads(data)


def ptr(data, pointer):
    for token in pointer.strip('/').split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        data = data[int(token)] if isinstance(data, list) else data[token]
    return data


class LocalGit:
    def __init__(self, directory, head):
        self.directory = directory
        self.head = head

    def run(self, *args):
        return subprocess.check_output(['git', '-C', str(self.directory), *args], stderr=subprocess.PIPE)

    def read(self, path, commit=None):
        return self.run('show', (commit or self.head) + ':' + path)

    def changed(self, path, commit):
        names = self.run('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines()
        if path not in names:
            raise ValueError('historical_commit_did_not_change_target_path')

    def ancestor(self, old, head):
        if subprocess.run(['git','-C',str(self.directory),'merge-base','--is-ancestor',old,head]).returncode != 0:
            raise ValueError('historical_commit_not_ancestor')


class TargetWastelandsAliasTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config','user.name','Fixture')
        self.git('config','user.email','fixture@example.invalid')
        self.manifest_path = 'sources/manifests/TargetWastelands.yml'
        self.record_path = 'rules/hazards/target-wastelands-navigation-test-qualifications.yml'
        self.write(self.manifest_path, {'verified_semantic_records': []})
        self.commit('base manifest')
        raw = self.write(self.record_path, {'id':'rule.hazards.target-wastelands-navigation-test-qualifications','data':{'tn':4}})
        self.semantic = self.commit('historical mechanical change')
        self.identity = ('rule.hazards.target-wastelands-navigation-test-qualifications', self.record_path, self.semantic, blob(raw))
        self.entry = dict(zip(('id','path','commit_sha','blob_sha'),self.identity), gate_status='verified')

    def git(self,*args):
        return subprocess.check_output(['git', '-C',str(self.root),*args],stderr=subprocess.PIPE).decode().strip()

    def write(self,path,obj):
        p = self.root / path
        p.parent.mkdir(parents=True,exist_ok=True)
        raw = json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
        p.write_bytes(raw)
        self.git('add','--',path)
        return raw

    def commit(self,message):
        self.git('commit','-qm',message)
        return self.git('rev-parse','HEAD')

    def check(self, after, before=None, pointer='/verified_semantic_records/0'):
        if before is not None:
            self.write(self.manifest_path,before)
            self.commit('older index snapshot')
        self.write(self.manifest_path,after)
        index=self.commit('new source registration')
        return verify(LocalGit(self.root,index),self.manifest_path,index,pointer,self.identity,parse,ptr,blob)

    def test_wastelands_actual_registration_schema(self):
        result=self.check({'verified_semantic_records':[self.entry]})
        self.assertEqual(result['status'],'new_or_changed_verified_registration')
        self.assertFalse(result['formal_acceptance'])

    def test_wastelands_change_is_not_metadata_only(self):
        before={'verified_semantic_records':[self.entry]}
        after={'verified_semantic_records':[self.entry], 'note':'cosmetic'}
        with self.assertRaisesRegex(ValueError,'registration_already_verified_in_index_parent'):
            self.check(after,before=before)

    def test_duplicates_across_old_and_wastelands_schemas_are_detected(self):
        old=dict(zip(('record_id','record_path','current_commit','current_blob'),self.identity),gate='verified')
        with self.assertRaisesRegex(ValueError,'duplicate_verified_registration'):
            self.check({'verified_semantic_records':[self.entry], 'legacy_registration':old})

    def test_conflicting_blob_alias_rejected(self):
        broken=dict(self.entry,blob='f'*40)
        with self.assertRaisesRegex(ValueError,'registration_missing_or_conflicting_alias:blob'):
            self.check({'verified_semantic_records':[broken]})

    def test_conflicting_commit_alias_rejected(self):
        broken=dict(self.entry,current_commit='f'*40)
        with self.assertRaisesRegex(ValueError,'registration_missing_or_conflicting_alias:commit'):
            self.check({'verified_semantic_records':[broken]})

    def test_conflicting_gate_alias_rejected(self):
        broken=dict(self.entry,gate='pending')
        with self.assertRaisesRegex(ValueError,'registration_conflicting_gate_status'):
            self.check({'verified_semantic_records':[broken]})

    def test_pending_gate_does_not_count_as_verified(self):
        broken=dict(self.entry,gate_status='pending')
        with self.assertRaisesRegex(ValueError,'index_target_identity_mismatch'):
            self.check({'verified_semantic_records':[broken]})

    def test_relocation_of_wastelands_registration_is_not_new_proof(self):
        with self.assertRaisesRegex(ValueError,'registration_already_verified_in_index_parent'):
            self.check({'moved':{'entries':[self.entry]}},before={'verified_semantic_records':[self.entry]},pointer='/moved/entries/0')

    def test_unverified_historical_entry_can_become_verified(self):
        previous=dict(self.entry,gate_status='pending')
        result=self.check({'verified_semantic_records':[self.entry]},before={'verified_semantic_records':[previous]})
        self.assertEqual(result['prior_same_record_registrations'],1)

    def test_forged_semantic_blob_rejected(self):
        self.entry['blob_sha']='f'*40
        with self.assertRaisesRegex(ValueError,'index_target_identity_mismatch'):
            self.check({'verified_semantic_records':[self.entry]})

    def test_original_old_style_still_supported(self):
        standard=dict(zip(('id','path','commit','blob'),self.identity),gate='verified')
        self.check({'verified_semantic_records':[standard]})

    def test_absent_gate_not_assumed_verified(self):
        broken=dict(self.entry)
        del broken['gate_status']
        with self.assertRaisesRegex(ValueError,'index_target_identity_mismatch'):
            self.check({'verified_semantic_records':[broken]})

if __name__ == '__main__':
    unittest.main()
