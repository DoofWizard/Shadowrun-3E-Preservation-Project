import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from mm_successor import PATH, verify_link, verify
from source_index_receipts import MM, MM_SOURCE, MM_SHA
from validator import Git, blob, parse, ptr, sha, encoded, artifact, pairs


class SuccessorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run_git('init', '-q')
        self.run_git('config', 'user.email', 'fixture@example.invalid')
        self.run_git('config', 'user.name', 'Fixture')
        self.write(MM, {'records': []})
        self.commit('initial')
        self.record_id = 'rule.fixture'
        self.old_raw = self.write(PATH, {'id': self.record_id, 'data': {'value': 1}})
        self.old = (self.record_id, PATH, self.commit('old semantic'), blob(self.old_raw))
        self.old_entry = self.entry(self.old)
        self.write(MM, {'records': [self.old_entry]})
        self.old_index = self.commit('old index')
        self.new_raw = self.write(PATH, {'id': self.record_id, 'data': {'value': 2}})
        self.new = (self.record_id, PATH, self.commit('new semantic'), blob(self.new_raw))
        self.new_entry = self.entry(self.new)
        self.write('unrelated.txt', {'metadata': True})
        self.commit('unrelated')
        self.write(MM, {'records': [self.old_entry, self.new_entry]})
        self.new_index = self.commit('new index')
        self.git = Git(self.root, self.new_index)

    def run_git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args]).decode().strip()

    def write(self, path, obj):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        raw = json.dumps(obj).encode()
        p.write_bytes(raw)
        return raw

    def commit(self, message):
        self.run_git('add', '.')
        self.run_git('commit', '-qm', message)
        return self.run_git('rev-parse', 'HEAD')

    @staticmethod
    def entry(identity):
        return dict(zip(('id', 'path', 'commit', 'blob'), identity), gate='verified')

    def link(self, old=None, new=None, git=None):
        return verify_link(git or self.git, old or self.old, new or self.new,
                           self.old_index, self.new_index, '/records/0', '/records/1', parse, ptr, blob)

    def test_actual_git_history(self):
        a, b, parent = self.link()
        self.assertEqual(parent, self.old_index)
        self.assertEqual(a['prior_same_record_registrations'], 0)
        self.assertEqual(b['prior_same_record_registrations'], 1)

    def test_changed_live_path(self):
        self.write(PATH, {'id': self.record_id, 'data': {'value': 3}})
        with self.assertRaises(ValueError):
            self.link(git=Git(self.root, self.commit('unindexed successor')))

    def test_missing_predecessor_registration(self):
        self.write(MM, {'records': [self.new_entry]})
        with self.assertRaises(ValueError):
            self.link(git=Git(self.root, self.commit('lost history')))

    def test_duplicate_registration(self):
        self.write(MM, {'records': [self.old_entry, self.new_entry, self.new_entry]})
        with self.assertRaises(ValueError):
            self.link(git=Git(self.root, self.commit('duplicate')))

    def test_old_blob_wrong(self):
        with self.assertRaises(ValueError):
            self.link(old=self.old[:3] + ('0' * 40,))

    def test_missing_independent_review_and_predecessor(self):
        with self.assertRaisesRegex(ValueError, 'original_predecessor_and_review_required'):
            verify(self.git, {'id': MM_SOURCE, 'sha256': MM_SHA, 'manifest': MM}, {},
                   'reviewer', 'custodian', parse, ptr, blob, sha, encoded, artifact, pairs)


if __name__ == '__main__':
    unittest.main()
