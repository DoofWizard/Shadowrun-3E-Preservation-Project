import json
from pathlib import Path
import tempfile
import unittest

import fitz
import source_cache as sc


class CacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pdf = self.root / 'fixture.pdf'
        with fitz.open() as doc:
            p = doc.new_page()
            p.insert_text((50, 80), 'A fictional test uses 2D6 and a modifier of +3.')
            doc.new_page()
            doc.save(self.pdf)
        self.sha = sc.digest(self.pdf.read_bytes())

    def run_cache(self, select='all', dpi=0):
        return sc.run(self.pdf, self.sha, 2, self.root / 'cache', select, dpi)

    def test_cold_warm_no_credit(self):
        a, b = self.run_cache(), self.run_cache()
        self.assertEqual((a['extracted_pages'], b['cache_hits']), (2, 2))
        self.assertFalse(a['mechanical_acceptance'])
        self.assertEqual(b['page_credit'], 0)
        data = json.loads((Path(b['cache_path']) / 'p0001/layout.json').read_text())['payload']
        self.assertIn('2D6', data['embedded_text'])
        self.assertTrue(data['words'])
        self.assertEqual(data['mechanical_status'], 'unreviewed')
        self.assertTrue(data['review_required'])

    def test_select_and_render(self):
        a = self.run_cache('2', 120)
        b = self.run_cache('2', 120)
        self.assertEqual((a['selected_pages'], a['new_images'], b['new_images']), (1, 1, 0))
        self.assertTrue((Path(a['cache_path']) / 'p0002/image-120.png').is_file())
        self.assertFalse((Path(a['cache_path']) / 'p0001').exists())
        self.assertIn('sparse_text_inspect_image', a['routing_hints'])

    def test_tampered_layout_rebuild(self):
        a = self.run_cache('1')
        p = Path(a['cache_path']) / 'p0001/layout.json'
        data = json.loads(p.read_text())
        data['payload']['embedded_text'] = 'tampered'
        p.write_text(json.dumps(data))
        self.assertEqual(self.run_cache('1')['extracted_pages'], 1)

    def test_tampered_render_rebuild(self):
        a = self.run_cache('1', 120)
        (Path(a['cache_path']) / 'p0001/image-120.png').write_bytes(b'bad')
        self.assertEqual(self.run_cache('1', 120)['new_images'], 1)

    def test_wrong_hash(self):
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            sc.run(self.pdf, '0' * 64, 2, self.root / 'cache')

    def test_wrong_page_count(self):
        with self.assertRaisesRegex(ValueError, 'unexpected physical page count'):
            sc.run(self.pdf, self.sha, 3, self.root / 'cache')

    def test_page_selection(self):
        self.assertEqual(sc.select_pages('2,1-2', 2), [1, 2])
        for bad in ('0', '3', '2-1', '1,', '../1'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                sc.select_pages(bad, 2)

    def test_invalid_dpi(self):
        with self.assertRaisesRegex(ValueError, 'render DPI'):
            self.run_cache('1', 1000)


if __name__ == '__main__':
    unittest.main()
