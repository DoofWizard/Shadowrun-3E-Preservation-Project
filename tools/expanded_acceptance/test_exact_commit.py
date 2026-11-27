"""Synthetic Git topology regressions; no original source or acceptance claim."""
import subprocess
import tempfile
import unittest
from pathlib import Path

from validator import Blocked, Git


class ExactCommitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run_git('init', '-q')
        self.run_git('config', 'user.name', 'Synthetic fixture')
        self.run_git('config', 'user.email', 'fixture@example.invalid')
        self.write('rules/r.yml', 'original\n')
        self.write('sources/manifests/m.yml', 'original\n')
        self.base = self.commit('base')

    def run_git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, path, value):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value, encoding='utf-8')
        self.run_git('add', '--', path)

    def commit(self, msg):
        self.run_git('commit', '-qm', msg)
        return self.run_git('rev-parse', 'HEAD')

    def test_single_record_and_separate_index(self):
        self.write('rules/r.yml', 'corrected\n')
        semantic = self.commit('semantic')
        self.write('sources/manifests/m.yml', 'indexed\n')
        index = self.commit('index')
        reader = Git(self.root, index)
        reader.changed('rules/r.yml', semantic)
        reader.changed('sources/manifests/m.yml', index)
        reader.ancestor(semantic, index)

    def test_combined_semantic_and_index_rejected(self):
        self.write('rules/r.yml', 'corrected\n')
        self.write('sources/manifests/m.yml', 'indexed\n')
        head = self.commit('combined semantic and index')
        for path in ('rules/r.yml', 'sources/manifests/m.yml'):
            with self.subTest(path=path), self.assertRaisesRegex(Blocked, 'exact_path_commit_required'):
                Git(self.root, head).changed(path, head)

    def test_unrelated_path_change_rejected(self):
        self.write('rules/r.yml', 'corrected\n')
        self.write('unrelated.yml', 'another record\n')
        head = self.commit('two paths')
        with self.assertRaisesRegex(Blocked, 'exact_path_commit_required'):
            Git(self.root, head).changed('rules/r.yml', head)

    def test_rename_is_not_single_path_write(self):
        self.run_git('mv', 'rules/r.yml', 'rules/renamed.yml')
        head = self.commit('rename')
        with self.assertRaisesRegex(Blocked, 'exact_path_commit_required'):
            Git(self.root, head).changed('rules/renamed.yml', head)

    def test_unchanged_path_rejected(self):
        self.write('other.yml', 'unrelated\n')
        head = self.commit('other only')
        with self.assertRaisesRegex(Blocked, 'exact_path_commit_required'):
            Git(self.root, head).changed('rules/r.yml', head)


if __name__ == '__main__':
    unittest.main()
