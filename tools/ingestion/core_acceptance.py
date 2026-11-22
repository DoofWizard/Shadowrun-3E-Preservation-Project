#!/usr/bin/env python3
"""Offline acceptance of the available-source FASA7001 mechanical core.

This checks an independently source-reviewed obligation inventory against accepted
records and pinned review evidence. It does not perform source review, infer an
inventory from registered records, authorize pages, change a checkpoint, or mark
the complete narrative publication transcribed. Existing semantic gates remain
unchanged. Publication of the prepared receipt requires ordinary Contents writes
and a fresh exact readback before confirm can succeed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

from transaction_recovery import parse_yaml
from ingestion_gate import parsed_printed_or_pdf_page_set

SOURCE = "source.sr3-core"
PDF_SHA = "7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914"
MANIFEST = "sources/manifests/SR3.yml"
QUEUE = "docs/engine-readiness/FASA7001_CORE_RULES_CLOSURE_QUEUE_2026-11-11.yml"
INVENTORY_KEY = "core_acceptance_inventory"
PROTOCOL = "sr3-core-acceptance/v1"
CLASSES = {"rule_exact", "rule_procedure", "equipment_stat", "character_option", "campaign_guidance"}
SECTIONS = {
    "game_concepts": (36, 51), "character_creation": (52, 80),
    "skills": (81, 99), "combat": (100, 129), "vehicles_drones": (130, 157),
    "magic": (158, 198), "matrix": (199, 230), "running_shadows": (231, 241),
    "beyond_shadows": (242, 252), "contacts": (253, 259),
    "spirits_dragons": (260, 269), "street_gear": (270, 312),
    "seattle": (313, 322), "sourcebook_updates": (323, 325),
    "sample_record_sheets": (326, 329),
}


class AcceptanceError(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise AcceptanceError(reason)


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(encoded(value)).hexdigest()


def read_relative(root, relative):
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute(), "relative_path_required")
    require(".." not in Path(relative).parts, "unsafe_path")
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), "path_outside_repository")
    return path.read_bytes()


def pointer(value, path):
    require(isinstance(path, str) and path.startswith("/"), "explicit_json_pointer_required")
    for part in path[1:].split("/"):
        require(not re.search(r"~(?![01])", part), "invalid_json_pointer_escape")
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            require(bool(re.fullmatch(r"0|[1-9][0-9]*", part)), "invalid_list_pointer")
            require(int(part) < len(value), "field_pointer_missing")
            value = value[int(part)]
        else:
            require(isinstance(value, dict) and part in value, "field_pointer_missing")
            value = value[part]
    return value


def review_ref(root, ref, evidence):
    require(isinstance(ref, dict), "review_reference_required")
    path, ptr = ref.get("path"), ref.get("pointer")
    require(isinstance(path, str) and path.startswith(("docs/engine-readiness/", "references/audits/", "docs/ingestion/")), "source_review_path_required")
    require(not (path == QUEUE and str(ptr).startswith("/" + INVENTORY_KEY)), "self_attested_inventory_reference")
    # Parse each exact source review at most once per assess call. Hundreds of
    # distinct field pointers may share one lengthy independently reviewed file.
    # The cache is scoped to one assessment; prepare/confirm re-read current files.
    if path not in evidence:
        raw = read_relative(root, path)
        require(PDF_SHA.encode("ascii") in raw, "review_original_source_hash_missing_or_mismatch")
        evidence[path] = (blob(raw), parse_yaml(raw))
    value = pointer(evidence[path][1], ptr)
    require(value not in (None, False, "", [], {}), "empty_or_negative_review_evidence")
    require(ref.get("value_sha256") == digest(value), "source_review_fragment_changed")


def pages(value, maximum):
    require(isinstance(value, list) and value and all(type(p) is int and 1 <= p <= maximum for p in value), "explicit_page_list_required")
    require(value == sorted(set(value)), "duplicate_or_unsorted_pages")
    return set(value)


def indexed_record_pages(entry, record, key):
    """Check printed/PDF record provenance without erasing archival annotations.

    Two original unnumbered color-archetype sheets retain an exact explanatory
    suffix in printed_pages.  Only these two explicitly indexed exceptions may
    use the verified source-index range; arbitrary malformed ranges still fail.
    """
    value = record[key]
    try:
        return parsed_printed_or_pdf_page_set(value)
    except ValueError:
        annotated = {
            "65 (first unnumbered full-color archetype sheet after printed p64)": 65,
            "66 (second unnumbered color archetype sheet after p64)": 66,
        }
        require(key == "printed_pages" and value in annotated,
                "unparseable_indexed_record_pages:" + str(entry.get("path")))
        printed = annotated[value]
        expected_pdf = printed + 1
        require(entry.get("range_printed") == [printed, printed]
                and entry.get("range_pdf") == [expected_pdf, expected_pdf]
                and parsed_printed_or_pdf_page_set(record["pdf_pages"]) == {expected_pdf},
                "annotated_archetype_index_page_mismatch:" + str(entry.get("path")))
        return {printed}

def assess(root):
    root = Path(root).resolve()
    mraw, qraw = read_relative(root, MANIFEST), read_relative(root, QUEUE)
    manifest, queue = parse_yaml(mraw), parse_yaml(qraw)
    require(manifest.get("id") == SOURCE and manifest.get("source_pdf_sha256") == PDF_SHA, "wrong_core_source")
    recovery = manifest.get("postscan_verified_mechanics_recovery", {})
    require(recovery.get("source_pdf_sha256") == PDF_SHA, "index_source_hash_mismatch")
    entries = recovery.get("verified_semantic_records")
    require(isinstance(entries, list) and entries, "accepted_index_required")
    records, paths = {}, set()
    for entry in entries:
        rid, path = entry.get("id"), entry.get("path")
        require(isinstance(rid, str) and rid and rid not in records and path not in paths, "duplicate_or_missing_record_identity")
        require(entry.get("gate") == "verified" and bool(re.fullmatch(r"[0-9a-f]{40}", str(entry.get("commit", "")))), "unverified_record:" + rid)
        raw = read_relative(root, path)
        require(blob(raw) == entry.get("blob"), "record_blob_mismatch:" + path)
        record = parse_yaml(raw)
        require(record.get("id") == rid and record.get("source") == SOURCE, "record_provenance_mismatch:" + path)
        require(record.get("content_class") == [entry.get("content_class")], "record_class_mismatch:" + path)
        records[rid] = (entry, record)
        paths.add(path)

    policy = manifest.get("owner_scan_omission_policy_2026_11_20", {})
    require(policy.get("authority") == "project_owner" and policy.get("absent_pages_block_eligible_work") is False
            and policy.get("omitted_pages_count_as_scanned_or_authorized") is False, "owner_omission_disposition_required")
    omissions = set()
    for item in policy.get("source_specific_omissions", []):
        require(item.get("original_source_sha256") == PDF_SHA
                and item.get("current_disposition") == "owner_accepted_nonblocking_deferred_later_audit"
                and item.get("core_mechanics_blocker") is False
                and item.get("source_completion_or_page_credit_implied") is False, "invalid_omission_disposition")
        require(type(item.get("omitted_printed_page")) is int
                and 1 <= item["omitted_printed_page"] <= 345
                and item["omitted_printed_page"] not in omissions, "invalid_or_duplicate_omission_page")
        omissions.add(item["omitted_printed_page"])

    inventory = queue.get(INVENTORY_KEY)
    require(isinstance(inventory, dict), "missing_source_reviewed_heading_field_inventory:" + QUEUE + "#" + INVENTORY_KEY)
    require(inventory.get("schema_version") == "sr3-core-obligation-inventory/v1", "inventory_schema_mismatch")
    require(inventory.get("source") == SOURCE and inventory.get("source_pdf_sha256") == PDF_SHA, "inventory_source_mismatch")
    require(inventory.get("scope") == "available_original_mechanics", "inventory_scope_mismatch")
    require(inventory.get("independently_reviewed_original_headings_fields_and_classes") is True,
            "independent_source_inventory_review_required")
    require(inventory.get("unresolved_mechanical_fields") == [], "unresolved_mechanical_fields")
    evidence = {}
    review_ref(root, inventory.get("source_inventory_review"), evidence)
    sections = inventory.get("sections")
    require(isinstance(sections, list) and len(sections) == len(SECTIONS), "all_fifteen_sections_required")
    section_ids, required = set(), {}
    for section in sections:
        sid = section.get("id")
        require(sid in SECTIONS and sid not in section_ids, "duplicate_or_unknown_section")
        section_ids.add(sid)
        require(section.get("printed_range") == list(SECTIONS[sid]), "section_range_changed:" + sid)
        require(section.get("heading_field_content_class_inventory_complete") is True, "section_inventory_incomplete:" + sid)
        review_ref(root, section.get("source_review"), evidence)
        fields = section.get("required_fields")
        require(isinstance(fields, list), "section_fields_required:" + sid)
        if not fields:
            require(sid == "seattle" and section.get("no_independent_game_mechanics") is True,
                    "empty_mechanical_section:" + sid)
        for field in fields:
            fid = field.get("id")
            require(isinstance(fid, str) and fid and fid not in required, "duplicate_or_missing_obligation")
            require(isinstance(field.get("source_heading"), str) and bool(field["source_heading"].strip()), "source_heading_required:" + fid)
            require(field.get("content_class") in CLASSES, "mechanical_content_class_required:" + fid)
            pp, pdf = pages(field.get("printed_pages"), 345), pages(field.get("pdf_pages"), 345)
            require(pp.issubset(range(SECTIONS[sid][0], SECTIONS[sid][1] + 1)), "obligation_outside_section:" + fid)
            require(not pp.intersection(omissions), "unseen_page_mechanic_invented:" + fid)
            require(pdf, "pdf_provenance_required")
            required[fid] = field
    require(section_ids == set(SECTIONS), "section_inventory_gap")
    bindings = inventory.get("bindings")
    require(isinstance(bindings, dict) and set(bindings) == set(required), "missing_or_extra_field_bindings")
    for fid, binding in bindings.items():
        require(isinstance(binding, dict) and binding.get("record_id") in records, "unindexed_field_record:" + fid)
        entry, record = records[binding["record_id"]]
        require(entry["content_class"] == required[fid]["content_class"], "bound_content_class_mismatch:" + fid)
        ptr = binding.get("record_pointer")
        require(isinstance(ptr, str) and ptr.startswith("/data/"), "substantive_field_pointer_required:" + fid)
        pointer(record, ptr)
        require(set(required[fid]["printed_pages"]).issubset(indexed_record_pages(entry, record, "printed_pages"))
                and set(required[fid]["pdf_pages"]).issubset(indexed_record_pages(entry, record, "pdf_pages")), "bound_page_provenance_mismatch:" + fid)
        review_ref(root, binding.get("source_review"), evidence)
    return {
        "protocol": PROTOCOL, "status": "acceptance_evidence_validated",
        "source": SOURCE, "source_pdf_sha256": PDF_SHA,
        "validator_blob": blob(Path(__file__).read_bytes()),
        "manifest_blob": blob(mraw), "closure_queue_blob": blob(qraw),
        "inventory_sha256": digest(inventory), "source_review_document_blobs": {path: recorded[0] for path, recorded in evidence.items()},
        "indexed_records_verified": len(records), "source_sections": len(section_ids),
        "required_fields_bound": len(required), "owner_nonblocking_omitted_pages": sorted(omissions),
        "new_semantic_records": 0, "authorized_printed_pages": 0,
        "whole_publication_transcription_complete": False, "engine_execution_certified": False,
        "source_fidelity_limit": "Relies on the identified independently authored original-source reviews; this structural check does not perform or replace them.",
    }


def prepare(root, fresh_pdf):
    root = Path(root).resolve()
    result = assess(root)
    command = [sys.executable, str(root / "tools/ingestion/preservation_method.py"),
               "verify-source", str(Path(fresh_pdf).resolve()), str(root / MANIFEST)]
    executed = subprocess.run(command, capture_output=True, text=True, check=False)
    require(executed.returncode == 0, "actual_verify_source_failed:" + executed.stdout.strip())
    verification = json.loads(executed.stdout)
    require(verification.get("status") == "source_pdf_hash_verified" and verification.get("source") == SOURCE
            and verification.get("sha256") == PDF_SHA,
            "actual_verify_source_receipt_required")
    require(hashlib.sha256(Path(fresh_pdf).read_bytes()).hexdigest() == PDF_SHA, "fresh_pdf_hash_mismatch")
    require(assess(root) == result, "core_inputs_changed_during_prepare")
    return {"protocol": PROTOCOL, "status": "prepared_core_acceptance", "assessment": result,
            "actual_source_verification": verification, "next": "ordinary_contents_write_then_exact_fresh_readback_and_confirm"}


def confirm(root, plan_raw, readback_raw, commit, readback_blob):
    require(plan_raw == readback_raw, "acceptance_receipt_bytes_changed")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", str(commit))), "ordinary_commit_receipt_required")
    require(blob(readback_raw) == readback_blob, "acceptance_readback_blob_mismatch")
    plan = json.loads(plan_raw)
    require(plan.get("protocol") == PROTOCOL and plan.get("status") == "prepared_core_acceptance", "acceptance_prepare_required")
    verification = plan.get("actual_source_verification", {})
    require(verification.get("status") == "source_pdf_hash_verified" and verification.get("source") == SOURCE
            and verification.get("sha256") == PDF_SHA,
            "source_verification_receipt_missing")
    require(plan.get("assessment") == assess(root), "core_inputs_changed_after_prepare")
    return {"protocol": PROTOCOL, "status": "verified_core_acceptance", "source": SOURCE,
            "receipt_commit": commit, "receipt_blob": readback_blob, "receipt_sha256": hashlib.sha256(readback_raw).hexdigest(),
            "assessment": plan["assessment"], "whole_source_status_change_authorized": False,
            "checkpoint_change_authorized": False, "authorized_printed_pages": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["assess", "prepare", "confirm"])
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--fresh-pdf", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--readback", type=Path)
    parser.add_argument("--commit")
    parser.add_argument("--readback-blob")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.mode == "assess":
            result = assess(args.repo_root)
        elif args.mode == "prepare":
            require(args.fresh_pdf is not None and args.output is not None, "fresh_pdf_and_output_required")
            result = prepare(args.repo_root, args.fresh_pdf)
        else:
            require(args.plan is not None and args.readback is not None, "plan_and_readback_required")
            result = confirm(args.repo_root, args.plan.read_bytes(), args.readback.read_bytes(), args.commit, args.readback_blob)
        if args.output:
            with args.output.open("xb") as destination:
                destination.write(encoded(result))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (ValueError, TypeError, KeyError, IndexError, OSError, yaml.YAMLError) as exc:
        print(json.dumps({"protocol": PROTOCOL, "status": "blocked", "reason": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
