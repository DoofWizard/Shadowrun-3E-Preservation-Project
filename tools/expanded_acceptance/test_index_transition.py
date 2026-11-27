"""Real Git synthetic fixtures: registration history, not source acceptance."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from index_transition import verify
from validator import Git, blob, encoded, parse, ptr


class IndexTransitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.mp = 'sources/manifests/m.yml'
        self.path = 'rules/r.yml'
        self.write(self.mp, {'verified': []})
        self.commit('base')
        raw = self.write(self.path, {'id': 'rule.test', 'data': {'tn': 4}})
        self.semantic = self.commit('semantic')
        self.identity = ('rule.test', self.path, self.semantic, blob(raw))
        self.entry = dict(zip(('id', 'path', 'commit', 'blob'), self.identity), gate='verified')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, path, obj):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        raw = encoded(obj)
        dest.write_bytes(raw)
        self.git('add', '--', path)
        return raw

    def commit(self, msg):
        self.git('commit', '-qm', msg)
        return self.git('rev-parse', 'HEAD')

    def check(self, after, pointer='/verified/0', before=None):
        if before is not None:
            self.write(self.mp, before)
            self.commit('previous index')
        self.write(self.mp, after)
        index = self.commit('claimed index')
        return verify(Git(self.root, index), self.mp, index, pointer,
                      self.identity, parse, ptr, blob)

    def test_new_registration(self):
        self.assertEqual(self.check({'verified': [self.entry]})['prior_same_record_registrations'], 0)

    def test_changed_registration(self):
        prior = {**self.entry, 'commit': 'a'*40, 'blob': 'b'*40}
        self.assertEqual(self.check({'verified': [self.entry]}, before={'verified': [prior]})['prior_same_record_registrations'], 1)

    def test_unverified_to_verified(self):
        self.check({'verified': [self.entry]}, before={'verified': [{**self.entry, 'gate': 'pending'}]})

    def test_metadata_only_rejected(self):
        with self.assertRaisesRegex(ValueError, 'registration_already_verified_in_index_parent'):
            self.check({'verified': [self.entry], 'note': 'new'}, before={'verified': [self.entry]})

    def test_pointer_move_and_alias_schema_rejected(self):
        prior = dict(zip(('record_id', 'record_path', 'current_commit', 'current_blob'), self.identity), gate='verified')
        with self.assertRaisesRegex(ValueError, 'registration_already_verified_in_index_parent'):
            self.check({'verified': [self.entry]}, before={'nested': {'old': prior}})

    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate_verified_registration'):
            self.check({'verified': [self.entry], 'another': self.entry})

    def test_conflicting_alias_rejected(self):
        with self.assertRaisesRegex(ValueError, 'registration_missing_or_conflicting_alias'):
            self.check({'verified': [{**self.entry, 'current_commit': 'f'*40}]})

    def test_correction_schema(self):
        e = dict(zip(('record_id', 'record_path', 'current_commit', 'current_blob'), self.identity), gate='verified')
        self.check({'correction': e}, '/correction')


if __name__ == '__main__':
    unittest.main()
