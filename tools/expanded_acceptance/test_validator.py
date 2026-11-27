"""Synthetic evidence only; no source acceptance is asserted by these tests."""
import base64
import copy
import json
import unittest

from validator import PROTOCOL, assess, blob, encoded, sha


class FixtureGit:
    head = 'a' * 40

    def __init__(self):
        self.files = {}

    def read(self, path, ref=None):
        return self.files[(ref or self.head, path)]

    def changed(self, path, ref):
        if (ref, path) not in self.files:
            raise ValueError('path not changed')

    def ancestor(self, old, new):
        if (old, new) not in [('b' * 40, 'c' * 40), ('c' * 40, self.head)]:
            raise ValueError('not ancestor')


def art(raw):
    return {'bytes_base64': base64.b64encode(raw).decode(), 'sha256': sha(raw), 'original_locator': 'SYNTHETIC'}


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.git = FixtureGit()
        self.pdf_sha = 'd' * 64
        self.path = 'rules/example.yml'
        self.mp = 'sources/manifests/example.yml'
        self.source = {'id': 'source.fixture', 'sha256': self.pdf_sha, 'edition': 'SR3', 'catalog': 'FIXTURE', 'publisher': 'Fixture', 'physical_pages': 2, 'manifest': self.mp}
        self.field = {'id': 'f1', 'heading': 'Table', 'class': 'rule_exact', 'kind': 'row', 'lineage': 'sr3_optional', 'value': 4}
        self.review = {'protocol': PROTOCOL, 'reviewer': 'synthetic reviewer', 'source': self.source, 'unresolved_fields': [], 'expected_printed_folios': [1], 'unrepresented_printed': [], 'contradictions': [], 'pages': [{'pdf': 1, 'printed': None, 'image_review': 'fixture', 'heading': 'Cover', 'disposition': 'zero_rules', 'reason': 'art', 'fields': []}, {'pdf': 2, 'printed': 1, 'image_review': 'fixture', 'heading': 'Table', 'disposition': 'mechanical', 'fields': [self.field]}]}
        self.record = {'id': 'rule.fixture', 'source': 'source.fixture', 'edition_scope': 'Fixture Third Edition', 'printed_pages': '1', 'pdf_pages': '2', 'content_class': ['rule_exact'], 'data': {'tn': 4, 'alternative': 5}, 'summary': '4'}
        self.bindings = {'f1': {'path': self.path, 'pointer': '/data/tn'}}
        self.evidence = {'protocol': PROTOCOL, 'custodian': 'synthetic custodian', 'transactions': {}}
        self.refresh()

    def refresh(self):
        raw = encoded(self.record)
        plan = {'protocol': 'sr3-gate/v1', 'status': 'preflighted', 'record_id': self.record['id'], 'source': self.record['source'], 'path': self.path, 'printed_pages': '1', 'pdf_pages': '2', 'pdf_sha256': self.pdf_sha, 'candidate_sha256': sha(raw), 'expected_blob_sha': blob(raw), 'immutable_sha256': sha(encoded({k: v for k, v in self.record.items() if k not in {'headline', 'summary', 'framing'}}))}
        receipt = {**plan, 'status': 'verified', 'commit_sha': 'b' * 40, 'readback_blob_sha': blob(raw)}
        ed = {'source': self.source['id'], 'source_sha256': self.pdf_sha, 'edition': self.source['edition'], 'publisher': self.source['publisher'], 'catalog': self.source['catalog'], 'path': self.path, 'candidate_sha256': sha(raw), 'baseline_sha256': sha(raw), 'baseline_reviewed_independently': True, 'candidate_reviewed_independently': True, 'nested_text_reviewed': True, 'printed_pages': '1', 'pdf_pages': '2', 'reviewed_edition_scope': self.record['edition_scope']}
        self.e = {'plan': plan, 'confirm': receipt, 'historical_confirm_artifact': art(encoded(receipt)), 'prewrite_journal_artifact': {'baseline': art(raw), 'candidate': art(raw), 'plan': art(encoded(plan))}, 'editorial_review_artifact': art(encoded(ed)), 'baseline_sha256': sha(raw), 'index_commit': 'c' * 40, 'index_pointer': '/verified/0'}
        self.evidence['transactions'][self.path] = self.e
        self.manifest = {'id': self.source['id'], 'source_pdf_sha256': self.pdf_sha, 'edition': self.source['edition'], 'catalog_number': self.source['catalog'], 'publisher': self.source['publisher'], 'verified': [{'id': self.record['id'], 'path': self.path, 'commit': 'b' * 40, 'blob': blob(raw), 'gate': 'verified', 'content_class': 'rule_exact'}]}
        for ref in (self.git.head, 'b' * 40):
            self.git.files[(ref, self.path)] = raw
        for ref in (self.git.head, 'c' * 40):
            self.git.files[(ref, self.mp)] = encoded(self.manifest)

    def run_assess(self):
        return assess(self.git, self.review, self.bindings, self.evidence, self.pdf_sha, 2)

    def blocked(self):
        with self.assertRaises((ValueError, KeyError, IndexError)):
            self.run_assess()

    def test_positive(self):
        r = self.run_assess()
        self.assertEqual(r['status'], 'PASS')
        self.assertFalse(r['formal_acceptance'])
        self.assertEqual(r['global_pages_advanced'], 0)

    def test_omitted_page(self):
        self.review['pages'].pop(0)
        self.blocked()

    def test_omitted_rule(self):
        del self.bindings['f1']
        self.blocked()

    def test_empty_page_inventory(self):
        self.review['pages'][1]['fields'] = []
        self.blocked()

    def test_wrong_edition(self):
        self.source['edition'] = 'SR2'
        self.blocked()

    def test_wrong_legacy_lineage(self):
        self.field['lineage'] = 'sr2_unsuperseded'
        self.blocked()

    def test_missing_path(self):
        del self.git.files[(self.git.head, self.path)]
        self.blocked()

    def test_altered_path(self):
        self.git.files[(self.git.head, self.path)] += b'\n'
        self.blocked()

    def test_missing_historical_receipt(self):
        del self.e['historical_confirm_artifact']
        self.blocked()

    def test_bad_journal(self):
        self.e['prewrite_journal_artifact']['baseline']['sha256'] = '0' * 64
        self.blocked()

    def test_frozen_baseline_changed(self):
        bad = {**self.record, 'data': {'tn': 99}}
        self.e['prewrite_journal_artifact']['baseline'] = art(encoded(bad))
        self.e['baseline_sha256'] = sha(encoded(bad))
        self.blocked()

    def test_unindexed_forward(self):
        self.manifest['verified'] = []
        self.git.files[(self.git.head, self.mp)] = encoded(self.manifest)
        self.blocked()

    def test_cosmetic_summary(self):
        self.bindings['f1']['pointer'] = '/summary'
        self.blocked()

    def test_typed_value(self):
        self.field['value'] = '4'
        self.blocked()

    def test_incomplete_editorial(self):
        del self.e['editorial_review_artifact']
        self.blocked()

    def test_known_contradiction(self):
        self.field['lineage'] = 'preserved_variant'
        other = {**copy.deepcopy(self.field), 'id': 'f2', 'value': 5}
        self.review['pages'][1]['fields'].append(other)
        self.review['contradictions'] = [{'fields': ['f1', 'f2'], 'disposition': 'preserve_distinct_variants', 'reason': 'distinct original variants'}]
        self.bindings['f2'] = {'path': self.path, 'pointer': '/data/alternative'}
        self.assertEqual(self.run_assess()['status'], 'PASS')
        self.bindings['f2']['pointer'] = '/data/tn'
        self.blocked()

    def test_missing_printed_folio(self):
        self.review['expected_printed_folios'] = [1, 2]
        self.blocked()


if __name__ == '__main__':
    unittest.main()
