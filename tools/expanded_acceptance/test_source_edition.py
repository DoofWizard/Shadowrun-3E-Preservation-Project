"""Synthetic regression tests for exact source-specific edition identity."""
import copy
import unittest

from source_edition import manifest_edition_matches, record_edition_matches, RIGGER_SCOPE
import test_validator
from validator import encoded


class SourceEditionTests(unittest.TestCase):
    def setUp(self):
        self.source = {'id': 'source.fanpro-10662', 'catalog': 'FanPro10662',
                       'publisher': 'FanPro', 'manifest': 'sources/manifests/Rigger3Revised.yml',
                       'edition': 'SR3', 'sha256': 'a' * 64}
        self.manifest = {'id': self.source['id'], 'catalog_number': self.source['catalog'],
                         'publisher': 'FanPro', 'edition': 'Shadowrun Third Edition'}
        self.record = {'source': self.source['id'], 'edition_scope': RIGGER_SCOPE,
                       'data': {'publication': {'edition': 'Shadowrun Third Edition',
                                               'source_pdf_sha256': self.source['sha256']}}}

    def test_exact_long_label(self):
        self.assertTrue(manifest_edition_matches(self.source, self.manifest))
        self.assertTrue(record_edition_matches(self.source, self.record))

    def test_no_global_alias(self):
        for key in ('id', 'catalog', 'publisher', 'manifest'):
            with self.subTest(key=key):
                self.assertFalse(manifest_edition_matches({**self.source, key: 'different'}, self.manifest))

    def test_wrong_manifest_identity(self):
        for key in ('id', 'catalog_number', 'publisher'):
            with self.subTest(key=key):
                self.assertFalse(manifest_edition_matches(self.source, {**self.manifest, key: 'different'}))

    def test_wrong_edition_and_substrings(self):
        for label in ('SR2', 'Shadowrun Second Edition', 'Shadowrun Third Edition / SR2', 'shadowrun third edition', 'Shadowrun Third Edition '):
            with self.subTest(label=label):
                self.assertFalse(manifest_edition_matches(self.source, {**self.manifest, 'edition': label}))
        self.assertFalse(manifest_edition_matches({**self.source, 'edition': 'SR2'}, self.manifest))
        self.assertFalse(manifest_edition_matches({**self.source, 'edition': 'SR2'}, {**self.manifest, 'edition': 'SR2'}))

    def test_wrong_scope(self):
        for scope in ('FASA Rigger 3 (FASA7910), Shadowrun Third Edition', 'Rigger 2, Shadowrun Second Edition', RIGGER_SCOPE + ' / SR2'):
            with self.subTest(scope=scope):
                self.assertFalse(record_edition_matches(self.source, {**self.record, 'edition_scope': scope}))
        self.assertFalse(record_edition_matches(self.source, {**self.record, 'source': 'source.r3'}))

    def test_nested_conflicting_identity(self):
        for k in ('edition', 'source_pdf_sha256', 'original_file_sha256', 'source_id', 'catalog_number', 'publisher', 'title'):
            r = copy.deepcopy(self.record)
            r['data']['publication'][k] = 'different'
            with self.subTest(key=k):
                self.assertFalse(record_edition_matches(self.source, r))

    def test_unchanged_other_source(self):
        source = {'id': 'source.other', 'edition': 'SR2'}
        self.assertTrue(manifest_edition_matches(source, {'edition': 'SR2'}))
        self.assertFalse(manifest_edition_matches(source, {'edition': 'SR3'}))

    def fixture(self):
        f = test_validator.AcceptanceTests(); f.setUp()
        f.source.update(self.source); f.source['sha256'] = f.pdf_sha
        f.mp = self.source['manifest']
        f.record.update(source=self.source['id'], edition_scope=RIGGER_SCOPE)
        f.refresh()
        f.manifest['edition'] = self.manifest['edition']
        for ref in (f.git.head, 'c' * 40):
            f.git.files[(ref, f.mp)] = encoded(f.manifest)
        return f

    def test_validator_positive(self):
        f = self.fixture()
        self.assertEqual(f.run_assess()['status'], 'PASS')

    def test_validator_scope_and_lineage(self):
        f = self.fixture()
        f.field['lineage'] = 'sr2_unsuperseded'
        with self.assertRaisesRegex(ValueError, 'wrong_lineage_edition'):
            f.run_assess()
        f = self.fixture()
        f.record['edition_scope'] = 'Rigger 2, Shadowrun Second Edition'
        f.refresh()
        f.manifest['edition'] = self.manifest['edition']
        for ref in (f.git.head, 'c' * 40):
            f.git.files[(ref, f.mp)] = encoded(f.manifest)
        with self.assertRaisesRegex(ValueError, 'record_source_or_edition_mismatch'):
            f.run_assess()
