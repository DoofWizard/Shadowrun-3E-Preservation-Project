import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'/'ingestion'))
import transaction_recovery as tr

SOURCE='source.fasa-7117'
PDF='a'*64
COMMIT='b'*40
SHA='c'*40
MANIFEST='''id: source.fasa-7117
status: ingesting
source_pdf_sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
done: {p: 102, pdf: 111}
next: {p: 103, pdf: 112}
pending:
  - id: pending.source7117.p103-106-semantic
    printed_range: [103, 106]
    pdf_range: [112, 115]
    reason: awaiting_semantic_records
resolved_pending: []
open_conflicts: []
routes:
  - [85, 125, directed]
records:
  - ["96-102-ghoultown-world", bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb]
source_end:
  printed_page: 160
  pdf_page: 169
'''
CHECKPOINT='''state_protocol_version: 2
phase: pass_b
active_source: source.fasa-7117
source_status: ingesting
completed_through: {printed_page: 102, pdf_page: 111}
resume_at: {printed_page: 103, pdf_page: 112}
last_commit: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
pending_normalization:
  - pending.source7117.p103-106-semantic
open_conflicts: []
next_sources: [source.fasa-7116]
'''
RECEIPTS=[]
for name,start,end in [('guidance',103,103),('world',104,106),('claims',104,106)]:
    RECEIPTS.append(dict(protocol='sr3-gate/v1',status='verified',source=SOURCE,pdf_sha256=PDF,
        path=f'world/chicago/{name}.yml',printed_pages=str(start) if start==end else f'{start}-{end}',
        pdf_pages=str(start+9) if start==end else f'{start+9}-{end+9}',
        commit_sha=COMMIT,readback_blob_sha=SHA,expected_blob_sha=SHA))
KEYS={r['path']:r['path'].split('/')[-1][:-4] for r in RECEIPTS}

class RecoveryTests(unittest.TestCase):
    def auth(self,receipts=RECEIPTS,manifest=MANIFEST,checkpoint=CHECKPOINT):
        with patch.object(tr,'_gate_authorize',return_value={'authorized':True}):
            return tr.authorize(tr.parse_yaml(manifest),tr.parse_yaml(checkpoint),receipts,
                   'pending.source7117.p103-106-semantic',103,112,107,116,[r['path'] for r in RECEIPTS])
    def test_authorize_full_page_coverage(self):
        self.assertTrue(self.auth()['authorized'])
    def test_missing_page_rejected(self):
        modified=copy.deepcopy(RECEIPTS);modified[1]['printed_pages']='104-105';modified[1]['pdf_pages']='113-114'
        modified[2]['printed_pages']='104-105';modified[2]['pdf_pages']='113-114'
        with self.assertRaisesRegex(tr.RecoveryError,'uncovered_pages'):self.auth(modified)
    def test_missing_or_extra_receipt_rejected(self):
        with self.assertRaisesRegex(tr.RecoveryError,'receipt_count_mismatch'):self.auth(RECEIPTS[:2])
    def test_denied_unverified_not_authorized(self):
        modified=copy.deepcopy(RECEIPTS);modified[1]['status']='preflighted'
        with self.assertRaisesRegex(tr.RecoveryError,'unverified_receipt'):self.auth(modified)
    def test_mismatched_readback_rejected(self):
        modified=copy.deepcopy(RECEIPTS);modified[1]['readback_blob_sha']='d'*40
        with self.assertRaisesRegex(tr.RecoveryError,'readback_not_verified'):self.auth(modified)
    def test_mismatched_source_hash_rejected(self):
        modified=copy.deepcopy(RECEIPTS);modified[2]['pdf_sha256']='f'*64
        with self.assertRaisesRegex(tr.RecoveryError,'source_pdf_mismatch'):self.auth(modified)
    def test_checkpoint_pending_mirror_mismatch(self):
        with self.assertRaisesRegex(tr.RecoveryError,'pending_mirror_mismatch'):self.auth(checkpoint=CHECKPOINT.replace('pending_normalization:\n  - pending.source7117.p103-106-semantic','pending_normalization: []'))
    def test_checkpoint_page_mismatch(self):
        with self.assertRaisesRegex(tr.RecoveryError,'boundary_mismatch'):self.auth(checkpoint=CHECKPOINT.replace('printed_page: 102','printed_page: 101'))
    def test_stale_start(self):
        m=tr.parse_yaml(MANIFEST);c=tr.parse_yaml(CHECKPOINT)
        with self.assertRaisesRegex(tr.RecoveryError,'stale_boundary'):
            tr.authorize(m,c,RECEIPTS,'pending.source7117.p103-106-semantic',105,114,107,116,list(KEYS))
    def test_duplicate_record_index(self):
        m=MANIFEST.replace('source_end:', '  - ["96-102-ghoultown-world", cccccccccccccccccccccccccccccccccccccccc]\nsource_end:')
        with self.assertRaisesRegex(tr.RecoveryError,'duplicate_record_index'):self.auth(manifest=m)
    def test_malformed_yaml_and_duplicate_mapping_key(self):
        with self.assertRaises(tr.RecoveryError):tr.parse_yaml('id: one\nid: two\n')
        with self.assertRaises(tr.RecoveryError):tr.parse_yaml('id: [unclosed\n')
    def test_manifest_render_and_checkpoint_repair_after_manifest_write(self):
        auth=self.auth();m=tr.render_manifest(MANIFEST,auth,KEYS);parsed=tr.parse_yaml(m)
        self.assertEqual(parsed['next'],{'p':107,'pdf':116})
        self.assertEqual(parsed['done'],{'p':106,'pdf':115})
        self.assertEqual(parsed['pending'],[])
        self.assertIn('pending.source7117.p103-106-semantic',parsed['resolved_pending'])
        self.assertEqual(len(parsed['records']),4)
        c=tr.render_checkpoint(m,CHECKPOINT,COMMIT);tr.state(tr.parse_yaml(m),tr.parse_yaml(c))
        self.assertIn(f'last_commit: {COMMIT}',c)
    def test_repaired_checkpoint_can_mirror_pending_manifest_without_advancement(self):
        c=tr.render_checkpoint(MANIFEST,CHECKPOINT.replace('pending_normalization:\n  - pending.source7117.p103-106-semantic','pending_normalization: []'),COMMIT)
        self.assertEqual(tr.parse_yaml(c)['pending_normalization'],['pending.source7117.p103-106-semantic'])
    def test_conflicting_record_index_rejected(self):
        m=MANIFEST.replace('source_end:',f'  - ["guidance", {"d"*40}]\nsource_end:')
        with self.assertRaisesRegex(tr.RecoveryError,'record_index_conflict'):
            tr.render_manifest(m,self.auth(),KEYS)
    def test_failure_classification_is_evidence_based(self):
        r=tr.classify_failure('manifest','This tool call was blocked by OpenAI\'s safety checks.')
        self.assertEqual(r['category'],'ambiguous_tool_layer_rejection');self.assertIsNone(r['github_http_status'])
        self.assertFalse(r['cause_proved'])
        self.assertEqual(tr.classify_failure('create','explicit',403,True)['next_action'],'stop_preserve_pending')
        self.assertEqual(tr.classify_failure('update','sha mismatch',409)['category'],'stale_sha')
    def test_stage_exact_candidate_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);b=root/'b.yml';c=root/'c.yml';gate=root/'fake_gate.py'
            payload=b'id: test\ncontent_class: [world_fact]\ndata: {magic: true}\n'
            b.write_bytes(payload);c.write_bytes(payload)
            gate.write_text('''import hashlib,json,sys\nfrom pathlib import Path\nc=Path(sys.argv[3]).read_bytes()\nblob=hashlib.sha1(("blob %s\\0"%len(c)).encode()+c).hexdigest()\nprint(json.dumps(dict(protocol="sr3-gate/v1",status="preflighted",source=sys.argv[5],path=sys.argv[4],pdf_sha256=sys.argv[6],record_id="test",printed_pages="103",pdf_pages="112",candidate_sha256=hashlib.sha256(c).hexdigest(),expected_blob_sha=blob)))\n''')
            journal=root/'journal'
            tr.stage(b,c,'world/chicago/test.yml',SOURCE,PDF,journal,gate)
            tr.stage(b,c,'world/chicago/test.yml',SOURCE,PDF,journal,gate)
            self.assertEqual(tr.inspect(journal,None,None)['status'],'absent')
            self.assertEqual(tr.inspect(journal,tr.git_blob(payload),None)['status'],'matching_blob_commit_unknown')
            self.assertEqual(tr.inspect(journal,tr.git_blob(payload),COMMIT)['receipt']['status'],'verified')
            self.assertEqual(tr.inspect(journal,'d'*40,COMMIT)['status'],'divergent_blob')
            c.write_bytes(payload+b'new: changed\n')
            with self.assertRaisesRegex(tr.RecoveryError,'journal_collision_or_corruption'):
                tr.stage(b,c,'world/chicago/test.yml',SOURCE,PDF,journal,gate)
            (journal/'candidate.yml').write_bytes(b'corrupted')
            with self.assertRaisesRegex(tr.RecoveryError,'journal_bytes_changed'):tr.inspect(journal,None,None)

if __name__=='__main__':unittest.main()
