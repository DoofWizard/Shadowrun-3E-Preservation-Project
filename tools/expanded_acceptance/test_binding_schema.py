import tempfile
import subprocess
from pathlib import Path
import unittest

from binding_schema import safe_git_path, substantive_pointer, mm_registration
from source_index_receipts import MM, MM_SOURCE, MM_SHA


class BindingSchemaTests(unittest.TestCase):
    def setUp(self):
        self.s = dict(manifest=MM, id=MM_SOURCE, sha256=MM_SHA)
        self.r = dict(id='rule.test', source=MM_SOURCE, edition_scope='SR3', content_class=['rule_exact'], printed_pages='41-42', pdf_pages='41-42')
        self.p = dict(path='rules/test.yml', candidate_sha256='a'*64, immutable_sha256='b'*64)
        self.c = dict(commit_sha='c'*40, readback_blob_sha='d'*40)
        self.base = 'e'*64
        self.entry = dict(id=self.r['id'], path=self.p['path'], printed='41-42', pdf='41-42', commit=self.c['commit_sha'], blob=self.c['readback_blob_sha'], baseline_sha256=self.base, candidate_sha256=self.p['candidate_sha256'], immutable_sha256=self.p['immutable_sha256'], gate='verified', fields='Fixture scope')
        self.pointer = '/source_field_review/confirmed_fixture/records/0'

    def test_literal_ampersand_path(self):
        self.assertTrue(safe_git_path(MM))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/MM
            p.parent.mkdir(parents=True)
            p.write_bytes(b'fixture\n')
            subprocess.run(['git', 'init', '-q', d], check=True)
            subprocess.run(['git', '-C', d, 'add', '.'], check=True)
            subprocess.run(['git', '-C', d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture'], check=True)
            self.assertEqual(subprocess.check_output(['git', '-C', d, 'show', 'HEAD:'+MM]), b'fixture\n')
        for path in ('../M&M.yml', 'sources/manifests/Other&Name.yml', 'sources/../manifests/M&M.yml', '/tmp/x', 'a/./b'):
            self.assertFalse(safe_git_path(path))

    def test_intrinsic_only_source_local_equipment(self):
        b = dict(path='entities/gear/x.yml', pointer='/intrinsic/mode')
        f = dict(**{'class': 'equipment_stat'})
        self.assertTrue(substantive_pointer(b, f))
        self.assertFalse(substantive_pointer(dict(b, path='rules/x.yml'), f))
        self.assertFalse(substantive_pointer(b, {'class': 'rule_exact'}))
        self.assertFalse(substantive_pointer(dict(b, mode='sr3-accepted-core-equivalence/v1'), f))
        self.assertFalse(substantive_pointer(dict(b, pointer='/headline'), f))
        self.assertFalse(substantive_pointer(dict(b, pointer='/intrinsic/'), f))
        self.assertTrue(substantive_pointer(dict(b, pointer='/data/row'), f))

    def test_exact_nested_registration(self):
        self.assertTrue(mm_registration(self.s, self.r, self.p, self.c, self.base, self.entry, self.pointer))
        for k, v in [('printed', '41'), ('blob', '0'*40), ('baseline_sha256', '0'*64), ('gate', 'pending'), ('content_class', 'rule_exact')]:
            with self.subTest(field=k), self.assertRaises(ValueError):
                mm_registration(self.s, self.r, self.p, self.c, self.base, dict(self.entry, **{k: v}), self.pointer)

    def test_wrong_source_class_or_pointer(self):
        for s, r, p in [(dict(self.s, sha256='0'*64), self.r, self.pointer), (self.s, dict(self.r, edition_scope='SR2'), self.pointer), (self.s, dict(self.r, content_class=['rule_exact', 'equipment_stat']), self.pointer), (self.s, self.r, '/unreviewed/0')]:
            with self.subTest(pointer=p), self.assertRaises(ValueError):
                mm_registration(s, r, self.p, self.c, self.base, self.entry, p)


if __name__ == '__main__':
    unittest.main()
