"""Synthetic structural regression for the actual Wastelands row layout."""
import copy
import unittest
import test_validator
from validator import encoded
from binding_schema import wastelands_registration


class WastelandsRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.f = f = test_validator.AcceptanceTests()
        f.setUp()
        f.mp = 'sources/manifests/TargetWastelands.yml'
        f.pdf_sha = '31db497dcbe649eda35b596ed2dff9475241518027137c65f35ea720b03d0c6b'
        f.source.update(id='source.fanpro-10653', catalog='FanPro10653', publisher='FanPro',
                        manifest=f.mp, sha256=f.pdf_sha)
        f.record.update(source=f.source['id'], edition_scope='SR3')
        f.refresh()
        r, p, c = f.record, f.e['plan'], f.e['confirm']
        self.entry = dict(id=r['id'], path=p['path'], printed_pages=r['printed_pages'],
                          pdf_pages=r['pdf_pages'], content_class=r['content_class'][0],
                          commit_sha=c['commit_sha'], blob_sha=c['readback_blob_sha'],
                          candidate_sha256=p['candidate_sha256'], immutable_sha256=p['immutable_sha256'],
                          gate_status='verified')
        f.manifest.pop('verified')
        f.manifest['verified_semantic_records'] = [self.entry]
        f.e['index_pointer'] = '/verified_semantic_records/0'
        self.sync()

    def sync(self):
        for ref in (self.f.git.head, 'c'*40):
            self.f.git.files[(ref, self.f.mp)] = encoded(self.f.manifest)

    def test_structural_integration(self):
        result = self.f.run_assess()
        self.assertEqual(result['status'], 'PASS')
        self.assertFalse(result['formal_acceptance'])

    def test_missing_and_conflicting_aliases(self):
        for key in list(self.entry):
            with self.subTest(key=key):
                old = self.entry.pop(key)
                self.sync()
                self.f.blocked()
                self.entry[key] = old
        self.entry['commit'] = self.entry['commit_sha']
        self.sync()
        self.f.blocked()

    def test_typed_record_pins(self):
        for key, value in [('printed_pages', 1), ('pdf_pages', '1'), ('content_class', 'equipment_stat'),
                           ('commit_sha', 'e'*40), ('blob_sha', 'e'*40), ('candidate_sha256', 'e'*64),
                           ('immutable_sha256', 'e'*64), ('gate_status', 'pending')]:
            old = self.entry[key]
            self.entry[key] = value
            self.sync()
            with self.subTest(key=key):
                self.f.blocked()
            self.entry[key] = old

    def test_moved_exact_row(self):
        m = copy.deepcopy(self.f.manifest)
        m['verified_semantic_records'].insert(0, {'id': 'other'})
        self.f.git.files[(self.f.git.head, self.f.mp)] = encoded(m)
        self.f.e.update(index_pointer='/verified_semantic_records/1',
                        historical_index_pointer='/verified_semantic_records/0')
        self.assertEqual(self.f.run_assess()['status'], 'PASS')
        m['verified_semantic_records'][1]['gate_status'] = 'pending'
        self.f.git.files[(self.f.git.head, self.f.mp)] = encoded(m)
        self.f.blocked()

    def test_wrong_source_and_pointer(self):
        f = self.f
        args = [f.source, f.record, f.e['plan'], f.e['confirm'], self.entry, f.e['index_pointer']]
        for n, v in ((0, dict(f.source, id='source.other')), (1, dict(f.record, edition_scope='SR2')),
                     (5, '/unreviewed/0')):
            trial = list(args)
            trial[n] = v
            with self.subTest(arg=n), self.assertRaises(ValueError):
                wastelands_registration(*trial)


if __name__ == '__main__':
    unittest.main()
