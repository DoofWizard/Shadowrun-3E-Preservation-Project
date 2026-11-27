"""Synthetic rejection fixtures; actual archives must remain outside Git."""
import io
import json
import unittest
import warnings
import zipfile
from archive_adapter import PRE, POST, blob, inspect, load_json, read_archive, sha


def archive(entries):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        for name, raw in entries:
            z.writestr(name, raw)
    return out.getvalue()


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.pre = {n: b'fixture' for n in PRE}
        self.post = {**self.pre, **{n: b'fixture' for n in POST if n not in PRE}}
        self.post['journal/readback-receipt.json'] = json.dumps({'commit': 'a'*40, 'blob': blob(b'fixture'), 'candidate_bytes': 7, 'exact_commit_live_bytes': True}).encode()
        self.post['journal/index-receipt.json'] = json.dumps({'commit': 'b'*40, 'blob': blob(b'fixture'), 'exact_commit_live_bytes': True}).encode()
        for n in ('journal/plan.json', 'journal/verified.json'):
            self.post[n] = b'{}'
        self.pre['journal/plan.json'] = b'{}'

    def assess(self, live=None):
        pre, post = archive(self.pre.items()), archive(self.post.items())
        return inspect(pre, post, sha(pre), sha(post), 'not_called.py', blob(b'fixture'), live or blob(b'fixture'), blob(b'fixture'))

    def test_exact_members(self):
        raw = archive(self.pre.items())
        self.assertEqual(read_archive(raw, sha(raw), PRE), self.pre)

    def test_wrong_pin(self):
        raw = archive(self.pre.items())
        with self.assertRaisesRegex(ValueError, 'archive_pin_mismatch'):
            read_archive(raw, '0'*64, PRE)

    def test_duplicate_member(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            raw = archive([*self.pre.items(), (PRE[0], b'different')])
        with self.assertRaisesRegex(ValueError, 'duplicate_zip_member'):
            read_archive(raw, sha(raw), PRE)

    def test_missing_confirm(self):
        del self.post['journal/verified.json']
        with self.assertRaisesRegex(ValueError, 'unsupported_or_missing_archive_members'):
            self.assess()

    def test_prewrite_changed(self):
        self.post['journal/baseline.yml'] = b'other'
        with self.assertRaisesRegex(ValueError, 'prewrite_archive_changed'):
            self.assess()

    def test_changed_live_blob(self):
        with self.assertRaisesRegex(ValueError, 'record_blob_mismatch'):
            self.assess('0'*40)

    def test_duplicate_json_key(self):
        with self.assertRaisesRegex(ValueError, 'duplicate_or_invalid_key'):
            load_json(b'{"status":"verified","status":"blocked"}')

    def test_unexpected_member(self):
        raw = archive([*self.pre.items(), ('../outside', b'other')])
        with self.assertRaisesRegex(ValueError, 'unsupported_or_missing_archive_members'):
            read_archive(raw, sha(raw), PRE)


if __name__ == '__main__':
    unittest.main()
