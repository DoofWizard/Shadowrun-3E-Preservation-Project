"""Synthetic original-evidence-shaped fixtures, never a production attestation."""
import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mm_successor import PATH, verify
from source_index_receipts import MM, MM_SOURCE, MM_SHA
from validator import Git, blob, parse, ptr, sha, encoded, artifact, pairs


def art(raw):
    return {'bytes_base64': base64.b64encode(raw).decode(), 'sha256': sha(raw),
            'original_locator': 'synthetic test only'}


class SuccessorEvidenceTests(unittest.TestCase):
    def test_full_successor_proof_with_real_git_and_gate(self):
        here = Path(__file__).resolve().parent
        gates = Path(os.environ.get('SR3_INGESTION_TOOLS', here.parent / 'ingestion'))
        with tempfile.TemporaryDirectory() as directory:
            tmp = Path(directory)
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
            for name in ('ingestion_gate.py', 'connector_preflight.py'):
                write('tools/ingestion/' + name, (gates / name).read_bytes())
            source = {'id': MM_SOURCE, 'sha256': MM_SHA, 'manifest': MM, 'edition': 'SR3',
                      'catalog': 'FASA7126', 'publisher': 'FASA Corporation'}
            manifest = {'id': MM_SOURCE, 'source_pdf_sha256': MM_SHA, 'edition': 'SR3',
                        'catalog_number': source['catalog'], 'publisher': source['publisher'], 'source_field_review': {}}
            write(MM, encoded(manifest))
            commit('initial synthetic fixture')
            record = {'id': 'rule.fixture', 'record_type': 'rule', 'status': 'reviewed', 'source': MM_SOURCE,
                      'printed_pages': '41-42', 'pdf_pages': '41-42', 'edition_scope': 'SR3',
                      'content_class': ['rule_exact'], 'framing': 'reference_exact', 'data': {'value': 1}}
            gate = root / 'tools/ingestion/ingestion_gate.py'
            def call(*args):
                return json.loads(subprocess.check_output([sys.executable, '-B', str(gate), *map(str, args)]))
            def transaction(key, value):
                record['data']['value'] = value
                raw = encoded(record)
                b, c, p = tmp/'baseline.yml', tmp/'candidate.yml', tmp/'plan.json'
                b.write_bytes(raw)
                c.write_bytes(raw)
                plan = call('prepare', b, c, PATH, MM_SOURCE, MM_SHA)
                write(PATH, raw)
                semantic = commit(key+' semantic')
                p.write_bytes(encoded(plan))
                confirm = call('confirm', p, c, semantic, blob(raw))
                entry = {'id': record['id'], 'path': PATH, 'printed': '41-42', 'pdf': '41-42',
                         'commit': semantic, 'blob': blob(raw), 'baseline_sha256': sha(raw),
                         'candidate_sha256': sha(raw), 'immutable_sha256': plan['immutable_sha256'],
                         'gate': 'verified', 'fields': 'synthetic fixture only'}
                manifest['source_field_review'][key] = {'records': [entry]}
                snap = encoded(manifest)
                write(MM, snap)
                index = commit(key+' index')
                receipt = {'status': 'indexed', 'path': MM, 'commit': index, 'blob': blob(snap),
                           'branch_and_commit_readbacks_equal': True, 'exact_local_proposal_match': True}
                editorial = {'source': MM_SOURCE, 'source_sha256': MM_SHA, 'edition': 'SR3',
                             'publisher': source['publisher'], 'catalog': source['catalog'], 'path': PATH,
                             'candidate_sha256': sha(raw), 'baseline_sha256': sha(raw),
                             'baseline_reviewed_independently': True, 'candidate_reviewed_independently': True,
                             'nested_text_reviewed': True, 'printed_pages': '41-42', 'pdf_pages': '41-42',
                             'reviewed_edition_scope': 'SR3'}
                return {'plan': plan, 'confirm': confirm, 'index_commit': index,
                        'index_pointer': '/source_field_review/'+key+'/records/0', 'baseline_sha256': sha(raw),
                        'prewrite_journal_artifact': {'baseline': art(raw), 'candidate': art(raw), 'plan': art(encoded(plan))},
                        'historical_confirm_artifact': art(encoded(confirm)), 'editorial_review_artifact': art(encoded(editorial)),
                        'historical_index_receipt_artifact': art(encoded(receipt)), 'historical_index_snapshot_artifact': art(snap)}
            old = transaction('confirmed_old', 1)
            new = transaction('confirmed_new', 2)
            new['predecessor_transaction'] = old
            att = {'protocol': 'sr3-mm-successor-review/v1', 'source': MM_SOURCE, 'source_sha256': MM_SHA,
                   'path': PATH, 'record_id': record['id'], 'previous_semantic_commit': old['confirm']['commit_sha'],
                   'previous_semantic_blob': old['confirm']['readback_blob_sha'], 'previous_index_commit': old['index_commit'],
                   'current_semantic_commit': new['confirm']['commit_sha'], 'current_semantic_blob': new['confirm']['readback_blob_sha'],
                   'current_index_commit': new['index_commit'], 'all_changed_fields_reviewed': True,
                   'same_edition_confirmed': True, 'current_controls': True,
                   'reviewer': 'synthetic lineage reviewer', 'original_review_locator': 'synthetic only'}
            new['successor_review_artifact'] = art(encoded(att))
            history = Git(root, new['index_commit'])
            def run():
                return verify(history, source, new, 'synthetic source reviewer', 'synthetic custodian',
                              parse, ptr, blob, sha, encoded, artifact, pairs)
            self.assertEqual(run()['status'], 'consistent_reviewed_successor_chain')
            new['successor_review_artifact'] = art(encoded(dict(att, reviewer='synthetic custodian')))
            with self.assertRaisesRegex(ValueError, 'independent_lineage_review_required'):
                run()
            new['successor_review_artifact'] = art(encoded(att))
            del old['historical_index_snapshot_artifact']
            with self.assertRaisesRegex(ValueError, 'inline_index_missing'):
                run()


if __name__ == '__main__':
    unittest.main()
