"""Fail-closed queue regression tests; no network, Codex, or real PDFs required."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import runner


class ContinuousQueueTests(unittest.TestCase):
    def test_all_ten_existing_source_owners_have_jobs(self):
        jobs = runner.load_queue(runner.HERE / "queue.json")
        self.assertEqual(len(jobs), 10)
        self.assertEqual({j["shard"] for j in jobs}, set(runner.SOURCE_OWNER))

    def test_rejects_cross_shard(self):
        job = {"id": "cross-shard", "shard": "legacy",
               "catalog_number": "FASA7118",
               "manifest": "sources/manifests/CorporateSecurityHandbook.yml",
               "section": "forbidden", "original_printed_pages": "94",
               "original_pdf_pages": [95]}
        with tempfile.TemporaryDirectory() as temp:
            q = Path(temp) / "q.json"
            q.write_text(json.dumps({"version": 1, "jobs": [job]}))
            with self.assertRaisesRegex(ValueError, "cross_shard_ownership"):
                runner.load_queue(q)

    def test_manifest_traversal_rejected(self):
        job = {"id": "bad-manifest", "shard": "matrix",
               "catalog_number": "FASA7909",
               "manifest": "sources/manifests/../../SR3.yml",
               "section": "forbidden", "original_printed_pages": "26",
               "original_pdf_pages": [27]}
        with tempfile.TemporaryDirectory() as temp:
            q = Path(temp) / "q.json"
            q.write_text(json.dumps({"version": 1, "jobs": [job]}))
            with self.assertRaisesRegex(ValueError, "invalid_manifest_path"):
                runner.load_queue(q)

    def test_exact_original_pdf_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            p = d / "FASA7909-original.pdf"
            p.write_bytes(b"original scan bytes")
            actual = hashlib.sha256(p.read_bytes()).hexdigest()
            self.assertEqual(runner.original_pdf(d, "FASA7909", actual), p)
            with self.assertRaisesRegex(ValueError, "hash_missing"):
                runner.original_pdf(d, "FASA7909", "a" * 64)

    def test_unknown_page_map_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            job = next(j for j in runner.load_queue(runner.HERE / "queue.json")
                       if not j["original_pdf_pages"])
            result = runner.process(job, root / "repo", root / "sources",
                                    root / "results", "codex", dry_run=True)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(result["canonical_records_accepted"], 0)
            self.assertEqual(result["globally_authorized_pages"], 0)

    def test_real_verify_source_failure_cannot_claim_success(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            gate = d / "tools" / "ingestion"
            gate.mkdir(parents=True)
            (gate / "preservation_method.py").write_text("raise SystemExit(2)\n")
            (d / "scan.pdf").write_bytes(b"source")
            (d / "manifest.yml").write_text("source_pdf_sha256: " + "a" * 64)
            with self.assertRaisesRegex(ValueError, "actual_verify_source_failed"):
                runner.verify_source(d, d / "scan.pdf", d / "manifest.yml")


if __name__ == "__main__":
    unittest.main()
