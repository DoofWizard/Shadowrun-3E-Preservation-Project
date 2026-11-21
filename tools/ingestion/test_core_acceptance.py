"""Synthetic-only acceptance fixtures; none are original-source or GitHub receipts."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import yaml

import core_acceptance as gate


class CoreAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.review_path = "docs/engine-readiness/SYNTHETIC_TEST_REVIEW.yml"
        self.review = {"source_pdf_sha256": gate.PDF_SHA, "review": {"fixture_only": True, "statement": "Synthetic unit-test evidence, not a source review."}}
        self.put(self.review_path, self.review)
        self.ref = {"path": self.review_path, "pointer": "/review", "value_sha256": gate.digest(self.review["review"])}
        self.inventory = {
            "schema_version": "sr3-core-obligation-inventory/v1", "source": gate.SOURCE,
            "source_pdf_sha256": gate.PDF_SHA, "scope": "available_original_mechanics",
            "independently_reviewed_original_headings_fields_and_classes": True,
            "unresolved_mechanical_fields": [], "source_inventory_review": copy.deepcopy(self.ref),
            "sections": [], "bindings": {},
        }
        self.entries = []
        for sid, span in gate.SECTIONS.items():
            section = {"id": sid, "printed_range": list(span),
                       "heading_field_content_class_inventory_complete": True,
                       "source_review": copy.deepcopy(self.ref), "required_fields": []}
            if sid == "seattle":
                section["no_independent_game_mechanics"] = True
            else:
                rid, fid, path = "synthetic." + sid, "field." + sid, "rules/test-" + sid + ".yml"
                record = {"id": rid, "source": gate.SOURCE, "content_class": ["rule_exact"],
                          "printed_pages": str(span[0]), "pdf_pages": str(span[0] + 1),
                          "data": {"synthetic_value": 1}}
                self.put(path, record)
                self.entries.append({"id": rid, "path": path, "content_class": "rule_exact",
                                     "commit": "a" * 40, "blob": gate.blob((self.root / path).read_bytes()), "gate": "verified"})
                section["required_fields"].append({"id": fid, "source_heading": "Synthetic test heading",
                                                   "content_class": "rule_exact", "printed_pages": [span[0]], "pdf_pages": [span[0] + 1]})
                self.inventory["bindings"][fid] = {"record_id": rid, "record_pointer": "/data/synthetic_value",
                                                    "source_review": copy.deepcopy(self.ref)}
            self.inventory["sections"].append(section)
        self.manifest = {
            "id": gate.SOURCE, "source_pdf_sha256": gate.PDF_SHA,
            "postscan_verified_mechanics_recovery": {"source_pdf_sha256": gate.PDF_SHA, "verified_semantic_records": self.entries},
            "owner_scan_omission_policy_2026_11_20": {
                "authority": "project_owner", "absent_pages_block_eligible_work": False,
                "omitted_pages_count_as_scanned_or_authorized": False,
                "source_specific_omissions": [{"original_source_sha256": gate.PDF_SHA, "omitted_printed_page": 308,
                    "current_disposition": "owner_accepted_nonblocking_deferred_later_audit",
                    "core_mechanics_blocker": False, "source_completion_or_page_credit_implied": False}],
            },
        }
        self.queue = {gate.INVENTORY_KEY: self.inventory}
        self.sync()

    def put(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def sync(self):
        self.put(gate.MANIFEST, self.manifest)
        self.put(gate.QUEUE, self.queue)

    def blocked(self, pattern):
        self.sync()
        with self.assertRaisesRegex(ValueError, pattern):
            gate.assess(self.root)

    def synthetic_plan(self):
        return gate.encoded({"protocol": gate.PROTOCOL, "status": "prepared_core_acceptance",
            "assessment": gate.assess(self.root),
            "actual_source_verification": {"status": "source_pdf_hash_verified", "source": gate.SOURCE, "sha256": gate.PDF_SHA}})

    def test_available_source_acceptance_never_advances_or_needs_denver(self):
        result = gate.assess(self.root)
        self.assertEqual(result["source_sections"], 15)
        self.assertEqual(result["required_fields_bound"], 14)
        self.assertEqual(result["owner_nonblocking_omitted_pages"], [308])
        self.assertEqual(result["authorized_printed_pages"], 0)
        self.assertFalse(result["whole_publication_transcription_complete"])
        self.assertFalse((self.root / "WORKER_CHECKPOINT.yml").exists())

    def test_packaged_records_without_independent_inventory_do_not_pass(self):
        del self.queue[gate.INVENTORY_KEY]
        self.blocked("missing_source_reviewed_heading_field_inventory")

    def test_incomplete_source_scope_is_rejected(self):
        self.inventory["independently_reviewed_original_headings_fields_and_classes"] = False
        self.blocked("independent_source_inventory_review_required")

    def test_each_original_section_is_required_once(self):
        self.inventory["sections"][-1] = copy.deepcopy(self.inventory["sections"][0])
        self.blocked("duplicate_or_unknown_section")

    def test_missing_rule_field_binding_is_rejected(self):
        del self.inventory["bindings"]["field.magic"]
        self.blocked("missing_or_extra_field_bindings")

    def test_unresolved_field_is_not_cleared_by_hash_consistency(self):
        self.inventory["unresolved_mechanical_fields"] = ["synthetic unresolved exception"]
        self.blocked("unresolved_mechanical_fields")

    def test_wrong_source_and_unverified_registration_are_rejected(self):
        self.manifest["source_pdf_sha256"] = "f" * 64
        self.blocked("wrong_core_source")
        self.manifest["source_pdf_sha256"] = gate.PDF_SHA
        self.entries[0]["gate"] = "preflighted"
        self.blocked("unverified_record")

    def test_record_byte_change_is_rejected(self):
        (self.root / self.entries[0]["path"]).write_text("changed", encoding="utf-8")
        self.blocked("record_blob_mismatch")

    def test_source_review_fragment_change_is_rejected(self):
        self.review["review"]["statement"] = "Different fixture review"
        self.put(self.review_path, self.review)
        self.blocked("source_review_fragment_changed")

    def test_inventory_cannot_cite_itself_as_independent_review(self):
        self.inventory["source_inventory_review"] = {"path": gate.QUEUE, "pointer": "/core_acceptance_inventory", "value_sha256": "0" * 64}
        self.blocked("self_attested_inventory_reference")

    def test_another_source_review_cannot_certify_core(self):
        self.review["source_pdf_sha256"] = "f" * 64
        self.put(self.review_path, self.review)
        self.blocked("review_original_source_hash_missing_or_mismatch")

    def test_duplicate_registration_cannot_inflate_coverage(self):
        self.entries.append(copy.deepcopy(self.entries[0]))
        self.blocked("duplicate_or_missing_record_identity")

    def test_nonexistent_and_presentation_field_bindings_are_rejected(self):
        binding = self.inventory["bindings"]["field.magic"]
        binding["record_pointer"] = "/data/absent"
        self.blocked("field_pointer_missing")
        binding["record_pointer"] = "/headline"
        self.blocked("substantive_field_pointer_required")

    def test_wrong_page_and_class_bindings_are_rejected(self):
        field = self.inventory["sections"][0]["required_fields"][0]
        field["pdf_pages"] = [50]
        self.blocked("bound_page_provenance_mismatch")
        field["pdf_pages"] = [37]
        field["content_class"] = "equipment_stat"
        self.blocked("bound_content_class_mismatch")

    def test_nonblocking_omission_does_not_authenticate_an_unseen_rule(self):
        field = next(s for s in self.inventory["sections"] if s["id"] == "street_gear")["required_fields"][0]
        field["printed_pages"] = [308]
        self.blocked("unseen_page_mechanic_invented")

    def test_nonblocking_omission_cannot_create_page_credit(self):
        self.manifest["owner_scan_omission_policy_2026_11_20"]["omitted_pages_count_as_scanned_or_authorized"] = True
        self.blocked("owner_omission_disposition_required")

    def test_confirm_requires_exact_committed_readback(self):
        plan = self.synthetic_plan()
        result = gate.confirm(self.root, plan, plan, "b" * 40, gate.blob(plan))
        self.assertEqual(result["status"], "verified_core_acceptance")
        self.assertFalse(result["checkpoint_change_authorized"])
        for changed_readback, commit, sha in [(plan + b"\n", "b" * 40, gate.blob(plan)),
                                               (plan, "", gate.blob(plan)), (plan, "b" * 40, "0" * 40)]:
            with self.subTest(commit=commit, sha=sha):
                with self.assertRaises(ValueError):
                    gate.confirm(self.root, plan, changed_readback, commit, sha)

    def test_confirm_rejects_changed_inputs_after_prepare(self):
        plan = self.synthetic_plan()
        self.queue["unrelated_history"] = "new concurrent source state"
        self.sync()
        with self.assertRaisesRegex(ValueError, "core_inputs_changed_after_prepare"):
            gate.confirm(self.root, plan, plan, "b" * 40, gate.blob(plan))

    def test_prepare_actually_requires_successful_verify_source_command(self):
        fake_pdf = self.root / "synthetic.pdf"
        fake_pdf.write_bytes(b"not an original PDF")
        with patch.object(gate.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "rejected", "")) as run:
            with self.assertRaisesRegex(ValueError, "actual_verify_source_failed"):
                gate.prepare(self.root, fake_pdf)
            self.assertIn("verify-source", run.call_args.args[0])
        response = {"status": "source_pdf_hash_verified", "source": gate.SOURCE, "sha256": gate.PDF_SHA}
        with patch.object(gate.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps(response), "")):
            with self.assertRaisesRegex(ValueError, "fresh_pdf_hash_mismatch"):
                gate.prepare(self.root, fake_pdf)

    def test_symlink_and_parent_escape_are_rejected(self):
        with self.assertRaises(ValueError):
            gate.read_relative(self.root, "../other.yml")
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / "other.yml"
            external.write_text("outside", encoding="utf-8")
            (self.root / "escape.yml").symlink_to(external)
            with self.assertRaises(ValueError):
                gate.read_relative(self.root, "escape.yml")


if __name__ == "__main__":
    unittest.main()
