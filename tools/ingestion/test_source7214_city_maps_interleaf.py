#!/usr/bin/env python3
"""FASA7214 PDF104 original city-map interleaf, exact-source negative controls."""
import copy
import unittest

from ingestion_gate import InvalidRecord, authorize_advance, source7214_city_maps_interleaf
from transaction_recovery import RecoveryError, authorize, parse_yaml, render_manifest, render_checkpoint

SOURCE = 'source.fasa-7214'
SOURCE_SHA = 'dc016e418a24fad63d56fba4f2f7f657cb1c0d995cdabd648ba9c6109e33f8f8'
MAP_PATH = 'references/target-ucas/boston-detroit-unnumbered-city-maps-pdf104.yml'
MAP_BLOB = 'd3b7c2a2a043614961f592518f32b0a31896e200'
MAP_COMMIT = '550d3cdf845def96bd264a689fbc60be7760db2b'


def state():
    manifest = dict(id=SOURCE, status='ingesting', source_pdf_sha256=SOURCE_SHA,
                    done={'p': 102, 'pdf': 103}, next={'p': 103, 'pdf': 104},
                    routes=[[86, 104, 'game_information_and_index']],
                    records=[], resolved_pending=[], pending=[], open_conflicts=[],
                    verified_ahead_of_contiguous_boundary=[], source_end={'status': 'not_completed'})
    checkpoint = dict(active_source=SOURCE,
                      completed_through={'printed_page': 102, 'pdf_page': 103},
                      resume_at={'printed_page': 103, 'pdf_page': 104},
                      pending_normalization=[], open_conflicts=[], last_commit='a'*40)
    return manifest, checkpoint


def receipt():
    return dict(protocol='sr3-gate/v1', status='verified', source=SOURCE,
                path=MAP_PATH, printed_pages='unnumbered map page between printed p102 and p104',
                pdf_pages='104', pdf_sha256=SOURCE_SHA, expected_blob_sha=MAP_BLOB,
                readback_blob_sha=MAP_BLOB, commit_sha=MAP_COMMIT)


class CityMapsInterleafTest(unittest.TestCase):
    def test_exact_plate_zero_numbered_pages(self):
        manifest, checkpoint = state()
        r = receipt()
        self.assertTrue(source7214_city_maps_interleaf(manifest, 103, 104, 104, 105, [r]))
        gate = authorize_advance(manifest, checkpoint, [r], 103, 104, 104, 105)
        self.assertTrue(gate['authorized'])
        self.assertTrue(gate['unnumbered_plate_only'])
        self.assertEqual(gate['new_printed_pages'], 0)
        self.assertEqual(gate['to'], [102, 104])
        recovered = authorize(manifest, checkpoint, [r], 'test-city-maps', 103, 104, 104, 105, [MAP_PATH])
        self.assertTrue(recovered['unnumbered_plate_only'])
        self.assertEqual(recovered['new_printed_pages'], 0)
        original = ('id: source.fasa-7214\nstatus: ingesting\nsource_pdf_sha256: '+SOURCE_SHA+'\n'
                    'done: {p: 102, pdf: 103}\nnext: {p: 103, pdf: 104}\n'
                    'pending: []\nopen_conflicts: []\nverified_ahead_of_contiguous_boundary: []\n'
                    'resolved_pending: []\nrecords: []\nroutes:\n'
                    '  - [86, 104, game_information_and_index]\nsource_end:\n  status: not_completed\n')
        proposed = render_manifest(original, recovered, {MAP_PATH:'reference.target_ucas.boston_detroit_unnumbered_maps_pdf104'})
        result = parse_yaml(proposed)
        self.assertEqual(result['done'], {'p':102,'pdf':104})
        self.assertEqual(result['next'], {'p':104,'pdf':105})
        self.assertEqual(result['source_end'], {'status':'not_completed'})
        self.assertEqual(len(result['records']), 1)
        cp = ('active_source: source.fasa-7214\n'
              'completed_through: {printed_page: 102, pdf_page: 103}\n'
              'resume_at: {printed_page: 103, pdf_page: 104}\n'
              'pending_normalization: []\nopen_conflicts: []\nlast_commit: '+'a'*40+'\n')
        updated_cp = render_checkpoint(proposed, cp, 'b'*40)
        self.assertIn('completed_through: {printed_page: 102, pdf_page: 104}', updated_cp)
        self.assertIn('resume_at: {printed_page: 104, pdf_page: 105}', updated_cp)

    def test_bad_receipt_and_state_fail_closed(self):
        manifest, checkpoint = state()
        good = receipt()
        changes = [
            ('path', 'references/target-ucas/other.yml'),
            ('printed_pages', '103'),
            ('printed_pages', 'unnumbered illustration between printed 102 and 104'),
            ('pdf_pages', '105'),
            ('pdf_sha256', '0'*64),
            ('expected_blob_sha', '0'*40),
            ('readback_blob_sha', '0'*40),
            ('status', 'preflighted'),
            ('commit_sha', 'abc'),
            ('source', 'source.other')
        ]
        for key, value in changes:
            with self.subTest(key=key, value=value):
                bad = dict(good, **{key:value})
                self.assertFalse(source7214_city_maps_interleaf(manifest,103,104,104,105,[bad]))
                with self.assertRaises(InvalidRecord):
                    authorize_advance(manifest,checkpoint,[bad],103,104,104,105)
        wrong = copy.deepcopy(manifest)
        wrong['source_pdf_sha256'] = 'f'*64
        self.assertFalse(source7214_city_maps_interleaf(wrong,103,104,104,105,[good]))
        with self.assertRaises(InvalidRecord):
            authorize_advance(wrong,checkpoint,[good],103,104,104,105)
        wrong = copy.deepcopy(manifest)
        wrong['done'] = {'p':103,'pdf':103}
        self.assertFalse(source7214_city_maps_interleaf(wrong,103,104,104,105,[good]))
        with self.assertRaises(InvalidRecord):
            authorize_advance(wrong,checkpoint,[good],103,104,104,105)
        with self.assertRaises(InvalidRecord):
            authorize_advance(manifest,checkpoint,[good,good],103,104,104,105)
        with self.assertRaises(InvalidRecord):
            authorize_advance(manifest,checkpoint,[good],103,104,105,106)
        with self.assertRaises(RecoveryError):
            authorize(manifest,checkpoint,[good], 'test-city-maps',103,104,105,106,[MAP_PATH])

if __name__ == '__main__':
    unittest.main()
