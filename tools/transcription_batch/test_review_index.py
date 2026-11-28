import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import review_index as ri


class ReviewIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.put("sources/catalog.yml", {"sources": [{"id": "source.test",
                 "catalog_number": "TEST", "drive_id": "PRIVATE-FIXTURE",
                 "corpus_role": "rules_primary"}]})
        self.put("rules/a.yml", {"id": "rule.test.a", "record_type": "rule",
                 "name": "Test vehicle", "source": "source.alias",
                 "printed_pages": "10-11", "pdf_pages": "12-13",
                 "data": {"rating": 2, "flag": True, "dash": "-", "blank": None,
                          "text": "PRIVATE-FIXTURE", "a/b~": 5}})
        self.put("rules/b.yml", {"id": "rule.test.a", "record_type": "rule",
                 "name": "Other vehicle", "effective": {"source": "source.other", "page": 10}})
        self.put("sources/manifests/Test.yml", {"id": "source.alias",
                 "record_type": "source", "catalog_number": "TEST",
                 "status": "complete", "entry": {"path": "rules/a.yml",
                 "commit": "a"*40, "blob": "b"*40,
                 "journal": "PRIVATE-FIXTURE"}})
        self.raw("entities/invalid.yml", "id: entity.invalid\nrecord_type: entity\ndata:\n  a: 1\n  a: 2\n")
        self.commit()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()

    def raw(self, path, text):
        p = self.root/path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def put(self, path, data):
        self.raw(path, json.dumps(data))

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def test_exact_committed_inputs(self):
        expected = self.git("rev-parse", "HEAD")
        self.raw("rules/a.yml", "not committed")
        index = ri.build(self.root, expected)
        self.assertEqual(index["head"], expected)
        self.assertEqual(len(index["records"]), 2)
        self.assertEqual(index["duplicate_record_ids"], ["rule.test.a"])
        self.assertIn("entities/invalid.yml", {x["path"] for x in index["issues"]})
        self.assertNotIn("PRIVATE-FIXTURE", json.dumps(index))
        self.assertFalse(index["page_credit"])

    def test_typed_values_and_paths(self):
        index = ri.build(self.root, "HEAD")
        blob = next(x["blob"] for x in index["records"] if x["path"] == "rules/a.yml")
        def check(pointer, value, expected, sha=blob):
            self.assertEqual(ri.compare(index, "rules/a.yml", sha, pointer, value)["result"], expected)
        check("/data/rating", 2, "exact_typed_value")
        check("/data/rating", "2", "different_typed_value")
        check("/data/rating", 2.0, "different_typed_value")
        check("/data/flag", 1, "different_typed_value")
        check("/data/blank", "-", "different_typed_value")
        check("/data/a~1b~0", 5, "exact_typed_value")
        check("/data/nope", None, "unindexed")
        check("/data/rating", 2, "unavailable", "0"*40)

    def test_page_and_registration_candidates(self):
        index = ri.build(self.root, "HEAD")
        packet = ri.packet(index, "source.test", "vehicle", printed="11", pdf="13")
        self.assertEqual(len(packet["manifest_candidates"]), 1)
        self.assertEqual(packet["source_record_count"], 1)
        self.assertEqual([x["path"] for x in packet["page_candidates"]], ["rules/a.yml"])
        self.assertEqual(len(packet["query_candidates"]), 2)
        self.assertEqual(packet["registration_candidates"][0]["manifest_pointer"], "/entry")
        self.assertEqual(packet["registration_candidates"][0]["semantic_blob"], "b"*40)
        self.assertFalse(packet["page_credit"])
        self.assertEqual(packet["review_status"], "unreviewed_candidates_only")
        self.assertEqual(ri.packet(index, "source.test", printed="99")["page_candidates"], [])
        with self.assertRaises(ValueError):
            ri.packet(index, "source.test", printed="unknown")

    def test_stale_index_and_unknown_sources(self):
        index = ri.build(self.root, "HEAD")
        self.put("rules/c.yml", {"id": "rule.new", "record_type": "rule"})
        self.commit()
        self.assertNotEqual(ri.build(self.root, "HEAD")["head"], index["head"])
        self.assertEqual(ri.packet(index, "source.unknown")["source_record_count"], 0)

    def test_no_inferred_printed_to_pdf_offset(self):
        index = ri.build(self.root, "HEAD")
        self.assertEqual(ri.packet(index, "source.test", pdf="11")["page_candidates"], [])
        self.assertIsNone(ri.page_range("10,12"))
        self.assertIsNone(ri.page_range(True))

    def test_duplicate_yaml_rejected(self):
        with self.assertRaises(ValueError):
            ri.load(b"a: 1\na: 2\n")


if __name__ == "__main__":
    unittest.main()
