"""Synthetic independent-input fixture; never a production source verdict."""
import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import fitz
from validator import PROTOCOL, blob, encoded, sha


def art(raw):
    return {'bytes_base64': base64.b64encode(raw).decode(), 'sha256': sha(raw),
            'original_locator': 'synthetic fixture only'}


class CurrentCLI(unittest.TestCase):
    def test_actual_cli_receipts_and_intrinsic_field(self):
        here = Path(__file__).resolve().parent
        gates = Path(os.environ.get('SR3_INGESTION_TOOLS', here.parent / 'ingestion'))
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            root = tmp / 'repo'
            root.mkdir()
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args]).decode().strip()
            def write(path, raw):
                p = root / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(raw)
            def commit(msg):
                git('add', '.')
                git('commit', '-qm', msg)
                return git('rev-parse', 'HEAD')
            git('init', '-q')
            git('config', 'user.name', 'Synthetic Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            for name in ('connector_preflight.py', 'ingestion_gate.py', 'preservation_method.py'):
                write('tools/ingestion/' + name, (gates / name).read_bytes())
            pdf = tmp / 'fixture.pdf'
            with fitz.open() as doc:
                doc.new_page()
                doc.save(pdf)
            source = {'id': 'source.fixture', 'sha256': sha(pdf.read_bytes()), 'edition': 'SR3',
                      'catalog': 'FIXTURE', 'publisher': 'Fixture', 'physical_pages': 1,
                      'manifest': 'sources/manifests/fixture.yml'}
            mp = source['manifest']
            manifest = {'id': source['id'], 'source_pdf_sha256': source['sha256'], 'edition': 'SR3',
                        'catalog_number': source['catalog'], 'publisher': source['publisher'], 'verified': []}
            original = encoded(manifest)
            write(mp, original)
            commit('initial fixture')
            path = 'entities/fixture.yml'
            record = {'id': 'entity.fixture', 'record_type': 'entity', 'status': 'reviewed',
                      'source': source['id'], 'printed_pages': '1', 'pdf_pages': '1',
                      'edition_scope': 'SR3', 'content_class': ['equipment_stat'], 'framing': 'reference_exact',
                      'data': {'name': 'fixture'}, 'intrinsic': {'mode': '-'}}
            raw = encoded(record)
            candidate, baseline = tmp / 'candidate.yml', tmp / 'baseline.yml'
            candidate.write_bytes(raw)
            baseline.write_bytes(raw)
            gate = root / 'tools/ingestion/ingestion_gate.py'
            def call(*args):
                return json.loads(subprocess.check_output([sys.executable, '-B', str(gate), *map(str, args)]))
            plan = call('prepare', baseline, candidate, path, source['id'], source['sha256'])
            write(path, raw)
            semantic = commit('fixture semantic')
            planfile = tmp / 'plan.json'
            planfile.write_bytes(encoded(plan))
            confirm = call('confirm', planfile, candidate, semantic, blob(raw))
            manifest['verified'].append({'id': record['id'], 'path': path, 'commit': semantic,
                                         'blob': blob(raw), 'gate': 'verified', 'content_class': 'equipment_stat'})
            snapshot = encoded(manifest)
            write(mp, snapshot)
            index = commit('fixture index')
            ed = {'source': source['id'], 'source_sha256': source['sha256'], 'edition': 'SR3',
                  'publisher': source['publisher'], 'catalog': source['catalog'], 'path': path,
                  'candidate_sha256': sha(raw), 'baseline_sha256': sha(raw),
                  'baseline_reviewed_independently': True, 'candidate_reviewed_independently': True,
                  'nested_text_reviewed': True, 'printed_pages': '1', 'pdf_pages': '1', 'reviewed_edition_scope': 'SR3'}
            receipt = {'commit_sha': index, 'blob_sha': blob(snapshot), 'manifest_path': mp,
                       'readback_exact': True, 'prior_blob_sha': blob(original)}
            transaction = {'plan': plan, 'confirm': confirm, 'index_commit': index, 'index_pointer': '/verified/0',
                           'baseline_sha256': sha(raw), 'prewrite_journal_artifact': {'baseline': art(raw),
                           'candidate': art(raw), 'plan': art(encoded(plan))}, 'historical_confirm_artifact': art(encoded(confirm)),
                           'editorial_review_artifact': art(encoded(ed)), 'historical_index_receipt_artifact': art(encoded(receipt)),
                           'historical_index_snapshot_artifact': art(snapshot)}
            evidence = {'protocol': PROTOCOL, 'custodian': 'fixture custodian', 'transactions': {path: transaction}}
            field = {'id': 'fixture.mode', 'heading': 'fixture table', 'class': 'equipment_stat',
                     'kind': 'row', 'lineage': 'sr3_effective', 'value': '-'}
            review = {'protocol': PROTOCOL, 'reviewer': 'fixture reviewer', 'source': source,
                      'unresolved_fields': [], 'expected_printed_folios': [1], 'unrepresented_printed': [],
                      'contradictions': [], 'pages': [{'pdf': 1, 'printed': 1, 'image_review': 'fixture only',
                      'heading': 'fixture table', 'disposition': 'mechanical', 'fields': [field]}]}
            bindings = {'fixture.mode': {'path': path, 'pointer': '/intrinsic/mode'}}
            def run():
                args = []
                for name, value in [('review', review), ('bindings', bindings), ('evidence', evidence)]:
                    p = tmp / (name + '.json')
                    p.write_bytes(encoded(value))
                    args.extend(['--' + name, str(p), '--' + name + '-sha', sha(p.read_bytes())])
                cmd = [sys.executable, str(here / 'validator.py'), '--repo', str(root), '--head', index,
                       '--pdf', str(pdf), *args]
                result = subprocess.run(cmd, capture_output=True, text=True)
                return result.returncode, json.loads(result.stdout)
            code, result = run()
            self.assertEqual((code, result['status']), (0, 'PASS'), result)
            self.assertFalse(result['formal_acceptance'])
            self.assertEqual(result['source_verification']['status'], 'source_pdf_hash_verified')
            self.assertEqual(result['present_day_prepare_rechecked'], 1)
            del transaction['historical_index_snapshot_artifact']
            code, result = run()
            self.assertEqual((code, result['status']), (1, 'BLOCKED'), result)
            transaction['historical_index_snapshot_artifact'] = art(snapshot)
            field['value'] = None
            code, result = run()
            self.assertEqual((code, result['status']), (1, 'BLOCKED'), result)


if __name__ == '__main__':
    unittest.main()
