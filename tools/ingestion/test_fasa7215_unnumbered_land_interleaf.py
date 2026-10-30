#!/usr/bin/env python3
"""Source-hash-bound FASA7215 PDF82 interleaf regression; no printed p81 fabricated."""
import copy
import unittest
import yaml

from ingestion_gate import InvalidRecord, authorize_advance
from transaction_recovery import RecoveryError, authorize, render_checkpoint, render_manifest, parse_yaml, state

SOURCE = '6d7e2f400eefd2c1edb99babe4cb7ed1ec3237be00c3c5423fc9428a23afc636'
PLATE = 'references/smuggler-havens/smuggling-on-land-unnumbered-plate-pdf82.yml'
BLOB = 'dfd05d7c8ab6c9202d79987b672c02a322de5bd5'
COMMIT = '4ea0bd64aa47cfa445ef0ce97c136a48d3965503'


def fixtures():
    manifest = {
        'id': 'source.fasa-7215', 'status': 'ingesting', 'source_pdf_sha256': SOURCE,
        'done': {'p': 80, 'pdf': 81}, 'next': {'p': 81, 'pdf': 82},
        'pending': [], 'open_conflicts': [], 'resolved_pending': [], 'records': [],
        'routes': [[79, 89, 'land_smuggling']],
        'source_integrity': {'visually_checked_mapping': {
            'printed_80': 81, 'unnumbered_land_interleaf_pdf': 82, 'printed_82': 83}},
    }
    checkpoint = {
        'active_source': 'source.fasa-7215', 'completed_through': {'printed_page': 80, 'pdf_page': 81},
        'resume_at': {'printed_page': 81, 'pdf_page': 82}, 'pending_normalization': [],
        'open_conflicts': [], 'last_commit': COMMIT,
    }
    receipt = {
        'protocol': 'sr3-gate/v1', 'status': 'verified', 'source': 'source.fasa-7215',
        'path': PLATE, 'printed_pages': 'unnumbered illustration between pp80 and 82',
        'pdf_pages': '82', 'pdf_sha256': SOURCE, 'commit_sha': COMMIT,
        'expected_blob_sha': BLOB, 'readback_blob_sha': BLOB,
    }
    return manifest, checkpoint, receipt


class LandInterleafTests(unittest.TestCase):
    def test_exact_original_plate_credits_zero_numbered_pages(self):
        m, c, r = fixtures()
        gate = authorize_advance(m, c, [r], 81, 82, 82, 83)
        self.assertTrue(gate['unnumbered_plate_only'])
        self.assertEqual(gate['new_printed_pages'], 0)
        self.assertEqual(gate['to'], [80, 82])
        tx = authorize(m, c, [r], 'source7215.unnumbered-land-interleaf-pdf82',
                       81, 82, 82, 83, [PLATE])
        after = render_manifest(yaml.safe_dump(m, sort_keys=False), tx,
                                {PLATE: 'reference.test.unnumbered_plate'})
        parsed = parse_yaml(after)
        self.assertEqual(parsed['done'], {'p': 80, 'pdf': 82})
        self.assertEqual(parsed['next'], {'p': 82, 'pdf': 83})
        cp = render_checkpoint(after, yaml.safe_dump(c, sort_keys=False), '1'*40)
        self.assertEqual(state(parsed, parse_yaml(cp))['status'], 'consistent')

    def test_rejects_all_altered_source_or_receipt_preconditions(self):
        for field, val in (
            ('printed_pages', '81'), ('pdf_pages', '83'), ('status', 'preflighted'),
            ('source', 'source.fasa-7116'), ('pdf_sha256', '0'*64),
            ('path', 'references/smuggler-havens/another.yml'),
            ('readback_blob_sha', '0'*40), ('commit_sha', 'invalid')):
            with self.subTest(field=field):
                m, c, r = fixtures()
                r[field] = val
                with self.assertRaises(InvalidRecord):
                    authorize_advance(m, c, [r], 81, 82, 82, 83)
        for field, val in (
            ('id', 'source.fasa-7116'), ('source_pdf_sha256', '0'*64),
            ('done', {'p': 81, 'pdf': 81})):
            with self.subTest(field=field):
                m, c, r = fixtures()
                m[field] = val
                with self.assertRaises(InvalidRecord):
                    authorize_advance(m, c, [r], 81, 82, 82, 83)
        m, c, r = fixtures()
        del m['source_integrity']['visually_checked_mapping']['unnumbered_land_interleaf_pdf']
        with self.assertRaises(InvalidRecord):
            authorize_advance(m, c, [r], 81, 82, 82, 83)

    def test_cannot_authorize_unnumbered_plate_as_fictitious_printed_page(self):
        m, c, r = fixtures()
        for end, end_pdf in ((82, 84), (83, 84), (83, 85)):
            with self.subTest(end=end, end_pdf=end_pdf):
                with self.assertRaises(InvalidRecord):
                    authorize_advance(m, c, [r], 81, 82, end, end_pdf)
        with self.assertRaises(InvalidRecord):
            authorize_advance(m, c, [r, copy.deepcopy(r)], 81, 82, 82, 83)
        with self.assertRaises(RecoveryError):
            authorize(m, c, [r], 'plate-test', 81, 82, 82, 83, ['another.yml'])


if __name__ == '__main__':
    unittest.main()
