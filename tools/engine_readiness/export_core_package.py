#!/usr/bin/env python3
"""Export the accepted FASA7001 core data without changing canonical records.

Requires PyYAML. This is a deterministic, offline data exporter, not a rules
engine, source reviewer, ingestion gate, or page-advancement operation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import yaml

ENTRYPOINT = "docs/engine-readiness/CANONICAL_RULES_DIGEST_ENTRYPOINT_2026-11-10.json"
EVIDENCE_PATHS = (
    "sources/manifests/SR3.yml",
    "docs/engine-readiness/FASA7001_CORE_RULES_CLOSURE_QUEUE_2026-11-11.yml",
)
EXPORTER_PATH = "tools/engine_readiness/export_core_package.py"


class StrictLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def encoded_json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n").encode("utf-8")


def read_relative(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path outside repository: {relative}")
    return path.read_bytes()


def export(root, output):
    root = root.resolve()
    entry_bytes = read_relative(root, ENTRYPOINT)
    entry = json.loads(entry_bytes)
    if entry.get("schema_version") != "sr3-canonical-rules-digest/1.0":
        raise ValueError("Use the consolidated version 1.0 core entrypoint.")
    if entry["publication"]["source_id"] != "source.sr3-core":
        raise ValueError("Entrypoint is not FASA7001 core.")

    members = {ENTRYPOINT: entry_bytes, "INDEX.json": entry_bytes}
    records = []
    seen_ids, seen_paths = set(), set()
    for item in entry["canonical_source_records"]:
        path, record_id = item["path"], item["id"]
        if path in seen_paths or record_id in seen_ids:
            raise ValueError(f"Duplicate registered path or ID: {path}")
        raw = read_relative(root, path)
        if git_blob(raw) != item["blob"]:
            raise ValueError(f"Canonical bytes differ from pinned Git blob: {path}")
        if hashlib.sha256(raw).hexdigest() != item["raw_sha256"]:
            raise ValueError(f"Canonical SHA-256 mismatch: {path}")
        if item["gate"] != "verified":
            raise ValueError(f"Registration is not marked verified: {path}")
        record = yaml.load(raw.decode("utf-8"), Loader=StrictLoader)
        if not isinstance(record, dict) or record.get("id") != record_id:
            raise ValueError(f"Canonical ID mismatch: {path}")
        seen_ids.add(record_id)
        seen_paths.add(path)
        members[path] = raw
        records.append({
            "id": record_id,
            "path": path,
            "content_class": item["content_class"],
            "record": record,
        })

    expected = entry["counts"]["registered_core_records"]
    if len(records) != expected:
        raise ValueError(f"Expected {expected} records, found {len(records)}.")

    for path in EVIDENCE_PATHS:
        members[path] = read_relative(root, path)
    manifest_path = entry["publication"]["source_manifest"]
    if git_blob(members[manifest_path]) != entry["publication"]["source_manifest_blob"]:
        raise ValueError("Source manifest differs from consolidated snapshot.")
    closeout_path = entry["accepted_closeout"]["path"]
    if git_blob(members[closeout_path]) != entry["accepted_closeout"]["blob"]:
        raise ValueError("Closeout evidence differs from consolidated snapshot.")

    members["CORE.md"] = read_relative(root, "CORE.md")
    members["README.md"] = members["CORE.md"]
    members[EXPORTER_PATH] = Path(__file__).read_bytes()
    members["core.json"] = encoded_json({
        "schema_version": "sr3-core-data-package/1.0",
        "publication": entry["publication"],
        "source_snapshot_commit": entry["source_snapshot_commit"],
        "counts": entry["counts"],
        "chapters": entry["chapters"],
        "known_limitations": entry["known_limitations"],
        "records": records,
    })
    members["PACKAGE_RECEIPT.json"] = encoded_json({
        "type": "existing_accepted_core_data_export",
        "source_snapshot_commit": entry["source_snapshot_commit"],
        "accepted_core_closeout_commit": entry["accepted_closeout"]["commit"],
        "entrypoint_git_blob": git_blob(entry_bytes),
        "exporter_git_blob": git_blob(members[EXPORTER_PATH]),
        "records_exported": len(records),
        "protected_mechanical_records": entry["counts"]["protected_mechanical_records"],
        "source_section_groups": len(entry["chapters"]),
        "all_record_bytes_and_ids_match_index": True,
        "duplicate_ids_or_paths": 0,
        "record_yaml_duplicate_keys": 0,
        "new_semantic_records": 0,
        "new_authorized_printed_pages": 0,
        "new_original_source_review_claimed": False,
        "game_engine_implementation_claimed": False,
    })
    members["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(raw).hexdigest()}  {name}\n"
        for name, raw in sorted(members.items())
    ).encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo("Shadowrun3E_Core/" + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw, compresslevel=9)
    return {
        "archive": str(output),
        "archive_bytes": output.stat().st_size,
        "archive_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "records": len(records),
        "files": len(members),
        "canonical_json_bytes": len(members["core.json"]),
        "entrypoint_git_blob": git_blob(entry_bytes),
        "exporter_git_blob": git_blob(members[EXPORTER_PATH]),
        "core_document_git_blob": git_blob(members["CORE.md"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=Path("dist/Shadowrun3E_Core.zip"))
    args = parser.parse_args()
    print(json.dumps(export(args.repo_root, args.output.resolve()), indent=2))


if __name__ == "__main__":
    main()
