"""Synthetic PDF, actual local Git commits and existing gates; no live source claim."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import fitz

from test_validator import AcceptanceTests, art
from validator import blob, encoded, sha


class IntegrationTests(unittest.TestCase):
    def test_cli_pinned_history_and_altered_record(self):
        here = Path(__file__).resolve().parent
        gates = Path(os.environ.get('SR3_INGESTION_TOOLS', here.parent / 'ingestion'))
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
            root = tmp / 'repo'
            root.mkdir()

            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args]).decode().strip()

            def write(path, raw):
                dest = root / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(raw)

            def commit(message):
                git('add', '.')
                git('commit', '-m', message)
                return git('rev-parse', 'HEAD')

            git('init', '-q')
            git('config', 'user.name', 'Synthetic Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            for name in ('connector_preflight.py', 'ingestion_gate.py', 'preservation_method.py'):
                write('tools/ingestion/' + name, (gates / name).read_bytes())
            pdf = tmp / 'fixture.pdf'
            with fitz.open() as doc:
                doc.new_page()
                doc.new_page()
                doc.save(pdf)
            fixture = AcceptanceTests()
            fixture.setUp()
            fixture.pdf_sha = sha(pdf.read_bytes())
            fixture.source['sha256'] = fixture.pdf_sha
            fixture.record.update(record_type='rule', status='reviewed', framing='reference_exact')
            fixture.refresh()
            raw = encoded(fixture.record)
            original = {**fixture.manifest, 'verified': []}
            write(fixture.mp, encoded(original))
            commit('Synthetic initial state')
            baseline, candidate = tmp / 'baseline.yml', tmp / 'candidate.yml'
            baseline.write_bytes(raw)
            candidate.write_bytes(raw)
            gate = root / 'tools/ingestion/ingestion_gate.py'

            def call(*args):
                return json.loads(subprocess.check_output([sys.executable, '-B', str(gate), *map(str, args)]))

            plan = call('prepare', baseline, candidate, fixture.path, fixture.source['id'], fixture.pdf_sha)
            write(fixture.path, raw)
            semantic = commit('Synthetic semantic transaction')
            planfile = tmp / 'plan.json'
            planfile.write_bytes(encoded(plan))
            receipt = call('confirm', planfile, candidate, semantic, blob(raw))
            fixture.manifest['verified'][0]['commit'] = semantic
            write(fixture.mp, encoded(fixture.manifest))
            index = commit('Synthetic source index')
            fixture.e.update(plan=plan, confirm=receipt, index_commit=index, historical_confirm_artifact=art(encoded(receipt)))
            fixture.e['prewrite_journal_artifact']['plan'] = art(encoded(plan))
            snapshot = encoded(fixture.manifest)
            index_receipt = {'commit_sha': index, 'blob_sha': blob(snapshot),
                             'manifest_path': fixture.mp, 'readback_exact': True,
                             'prior_blob_sha': blob(encoded(original))}
            fixture.e['historical_index_receipt_artifact'] = art(encoded(index_receipt))
            fixture.e['historical_index_snapshot_artifact'] = art(snapshot)
            args = []
            for name, value in [('review', fixture.review), ('bindings', fixture.bindings), ('evidence', fixture.evidence)]:
                path = tmp / (name + '.json')
                path.write_bytes(encoded(value))
                args.extend(['--' + name, str(path), '--' + name + '-sha', sha(path.read_bytes())])
            cmd = [sys.executable, str(here / 'validator.py'), '--repo', str(root), '--head', index, '--pdf', str(pdf), *args]
            passed = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            result = json.loads(passed.stdout)
            self.assertEqual(result['status'], 'PASS')
            self.assertEqual(result['source_verification']['status'], 'source_pdf_hash_verified')
            self.assertEqual(result['present_day_prepare_rechecked'], 1)
            self.assertFalse(result['formal_acceptance'])
            write(fixture.path, raw + b'\n')
            cmd[cmd.index('--head') + 1] = commit('Synthetic altered accepted bytes')
            blocked = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(blocked.returncode, 1, blocked.stdout + blocked.stderr)
            self.assertEqual(json.loads(blocked.stdout)['status'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
