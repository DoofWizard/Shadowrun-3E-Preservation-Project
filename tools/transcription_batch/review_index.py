#!/usr/bin/env python3
"""Read-only, Git-pinned canonical discovery. Results are candidates, not evidence."""
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import yaml


SCHEMA = "sr3-review-index/v1"
ROOTS = {"rules", "options", "entities", "modifiers", "catalogs", "guidance",
         "procedures", "tables", "mechanics", "conditions", "skills", "gear",
         "archetypes", "data", "canon", "references", "templates", "systems"}
# Include all tracked YAML documents, excluding known administrative roots
# from candidate classification. Top-level id and content shape are checked.
ADMIN = {"tools", ".github", "docs", "indexes", "sources", "pending", "audits", "tests"}
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,180}$")
WORD = re.compile(r"[a-z0-9]+")
FIELD_ROOTS = ("data", "resolution", "stats", "statistics", "modifiers", "effects",
               "scope", "effective", "requirements", "conditions", "options",
               "attributes", "rules", "cost", "availability", "values", "table")
LIMIT = 8_000_000


class StrictLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node):
    loader.flatten_mapping(node)
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=True)
        if not isinstance(key, (str, int, float, bool, type(None))):
            raise ValueError("unsupported mapping key")
        if key in result:
            raise ValueError("duplicate mapping key")
        result[key] = loader.construct_object(v, deep=True)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load(raw):
    return yaml.load(raw.decode("utf-8"), Loader=StrictLoader)


def git(repo, *args, data=None):
    return subprocess.run(["git", "-C", str(repo), *args], input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout


def blobs(repo, ref):
    head = git(repo, "rev-parse", "--verify", ref + "^{commit}").decode().strip()
    entries = []
    for item in git(repo, "ls-tree", "-r", "-z", head).split(b"\0"):
        if not item:
            continue
        meta, rawpath = item.split(b"\t", 1)
        mode, kind, sha = meta.decode().split()
        path = rawpath.decode("utf-8")
        if kind != "blob" or mode not in {"100644", "100755"}:
            continue
        if path.endswith((".yml", ".yaml")):
            entries.append((path, sha))
    # Batch-read exact Git objects, not mutable worktree bytes.
    payload = b"".join((sha + "\n").encode() for _, sha in entries)
    raw = git(repo, "cat-file", "--batch", data=payload)
    result = []
    pos = 0
    for path, sha in entries:
        end = raw.index(b"\n", pos)
        actual, kind, size = raw[pos:end].decode().split()
        count = int(size)
        pos = end + 1
        if actual != sha or kind != "blob" or raw[pos+count:pos+count+1] != b"\n":
            raise ValueError("Git blob framing/identity mismatch")
        result.append((path, sha, raw[pos:pos+count]))
        pos += count + 1
    if pos != len(raw):
        raise ValueError("unexpected trailing Git object bytes")
    return head, result


def scalar(value):
    # Distinguish null, bool, int, float, string. Never coerce numeric strings.
    if type(value) not in (type(None), bool, int, float, str):
        raise ValueError("unsupported scalar type")
    canonical = json.dumps(value, ensure_ascii=False, allow_nan=False,
                           separators=(",", ":")).encode("utf-8")
    return {"type": type(value).__name__, "sha256": hashlib.sha256(canonical).hexdigest()}


def ptr(key):
    return str(key).replace("~", "~0").replace("/", "~1")


def fields(value, path, out, ancestors=(), depth=0):
    if depth > 64 or len(out) >= 100000:
        raise ValueError("field traversal limit exceeded")
    if isinstance(value, (dict, list)):
        if id(value) in ancestors:
            raise ValueError("cyclic YAML alias")
        ancestry = ancestors + (id(value),)
        items = value.items() if isinstance(value, dict) else enumerate(value)
        for k, v in items:
            if isinstance(value, dict) and not isinstance(k, str):
                raise ValueError("non-string field key cannot be bound unambiguously")
            fields(v, path + "/" + ptr(k), out, ancestry, depth+1)
    else:
        out[path] = scalar(value)


def source_ids(record):
    found = set()
    def add(v):
        if isinstance(v, str) and v.startswith("source.") and ID.fullmatch(v):
            found.add(v)
        elif isinstance(v, dict):
            for k in ("id", "source", "source_id", "catalog_source_id"):
                add(v.get(k))
        elif isinstance(v, list):
            for x in v:
                add(x)
    for key in ("source", "sources", "source_id", "provenance", "effective"):
        add(record.get(key))
    data = record.get("data")
    if isinstance(data, dict):
        add(data.get("publication"))
    return sorted(found)



def page_range(value):
    if type(value) is int and 1 <= value <= 10000:
        return [value, value]
    if isinstance(value, str):
        m = re.fullmatch(r"\s*(\d+)(?:\s*[-–]\s*(\d+))?\s*", value)
        if m:
            lo, hi = int(m[1]), int(m[2] or m[1])
            if 1 <= lo <= hi <= 10000:
                return [lo, hi]
    return None


def locators(record):
    results = []
    def add(source, printed, pdf):
        if not isinstance(source, str) or not source.startswith("source.") or not ID.fullmatch(source):
            return
        p, f = page_range(printed), page_range(pdf)
        if p or f:
            results.append({"source": source, "printed": p, "pdf": f})
    add(record.get("source"), record.get("printed_pages"), record.get("pdf_pages"))
    for item in record.get("sources", []) if isinstance(record.get("sources"), list) else []:
        if isinstance(item, dict):
            add(item.get("source"), item.get("printed_pages", item.get("pages")), item.get("pdf_pages"))
    eff = record.get("effective")
    if isinstance(eff, dict):
        add(eff.get("source"), eff.get("page"), None)
    return results


def registrations(manifest, path, blob):
    found = []
    def walk(value, pointer="", depth=0, ancestors=()):
        if depth > 64 or len(found) >= 100000:
            raise ValueError("registration traversal limit exceeded")
        if isinstance(value, (dict, list)):
            if id(value) in ancestors:
                raise ValueError("cyclic manifest")
            ancestry = ancestors + (id(value),)
            if isinstance(value, dict):
                p, c, b = value.get("path"), value.get("commit"), value.get("blob")
                if isinstance(p, str) and p.endswith((".yml", ".yaml")) and not p.startswith("/") and ".." not in p.split("/") and all(isinstance(x, str) and re.fullmatch(r"[0-9a-f]{40}", x) for x in (c,b)):
                    found.append({"record_path": p, "semantic_commit": c, "semantic_blob": b,
                                  "manifest_path": path, "manifest_blob": blob,
                                  "manifest_pointer": pointer})
                items = value.items()
            else:
                items = enumerate(value)
            for k, v in items:
                if isinstance(k, str) or type(k) is int:
                    walk(v, pointer + "/" + ptr(k), depth+1, ancestry)
    walk(manifest)
    return found


def words(value):
    return set(WORD.findall(str(value).lower()))


def build(repo, ref):
    head, entries = blobs(repo, ref)
    records, manifests, catalog, issues, refs = [], [], [], [], []
    for path, sha, raw in entries:
        is_catalog = path == "sources/catalog.yml"
        is_manifest = path.startswith("sources/manifests/")
        if not (is_catalog or is_manifest) and path.split("/", 1)[0] in ADMIN:
            continue
        try:
            if len(raw) > LIMIT:
                raise ValueError("document exceeds read-only limit")
            d = load(raw)
            if is_catalog:
                if not isinstance(d, dict) or not isinstance(d.get("sources"), list):
                    raise ValueError("invalid catalog shape")
                for row in d["sources"]:
                    if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                        raise ValueError("invalid catalog entry")
                    # Never emit Drive IDs, source text or private journal locators.
                    catalog.append({k: row.get(k) for k in ("id", "catalog_number", "corpus_role")})
                continue
            if not isinstance(d, dict):
                raise ValueError("not a single record mapping")
            rid = d.get("id")
            if not isinstance(rid, str) or not ID.fullmatch(rid):
                raise ValueError("missing/invalid record id")
            if is_manifest:
                manifests.append({"id": rid, "path": path, "blob": sha,
                                  "catalog_number": d.get("catalog_number"),
                                  "catalog_source_id": d.get("catalog_source_id"),
                                  "source_pdf_sha256": d.get("source_pdf_sha256"),
                                  "physical_pages": d.get("source_physical_pdf_pages"),
                                  "reported_status": d.get("status")})
                refs.extend(registrations(d, path, sha))
                continue
            if not isinstance(d.get("record_type"), str):
                raise ValueError("missing record type")
            flat = {}
            errors = []
            for k in FIELD_ROOTS:
                if k in d:
                    try:
                        fields(d[k], "/" + ptr(k), flat)
                    except ValueError as exc:
                        errors.append(str(exc))
            if errors:
                issues.append({"path": path, "blob": sha, "reason": "; ".join(sorted(set(errors)))})
            label = d.get("name") if isinstance(d.get("name"), str) else d.get("title")
            if not isinstance(label, str):
                label = rid
            tokens = words(rid + " " + path + " " + label + " " + str(d.get("domain", "")))
            records.append({"id": rid, "path": path, "blob": sha,
                            "record_type": d["record_type"], "sources": source_ids(d),
                            "tokens": sorted(tokens), "fields": flat, "locators": locators(d),
                            "field_index_incomplete": bool(errors)})
        except (UnicodeError, ValueError, TypeError, RecursionError, yaml.YAMLError) as exc:
            # Do not expose source document content through exceptions.
            issues.append({"path": path, "blob": sha, "reason": type(exc).__name__})
    dup = Counter(r["id"] for r in records)
    return {"schema": SCHEMA, "head": head, "catalog": catalog, "manifests": manifests,
            "records": records, "issues": issues, "registration_candidates": refs,
            "duplicate_record_ids": sorted(k for k,v in dup.items() if v > 1),
            "review_status": "unreviewed_candidates_only", "page_credit": False}


def packet(index, source, query="", limit=40, printed=None, pdf=None):
    if not ID.fullmatch(source) or not 1 <= limit <= 500:
        raise ValueError("invalid source or candidate limit")
    cat = [c for c in index["catalog"] if c["id"] == source]
    codes = {str(c["catalog_number"]).lower() for c in cat if c["catalog_number"]}
    manifests = [m for m in index["manifests"] if source in
                 (m["id"], m.get("catalog_source_id")) or
                 str(m.get("catalog_number", "")).lower() in codes]
    # Catalog-number matches are candidates, not proof that two PDFs are identical.
    aliases = {source} | {m["id"] for m in manifests}
    q = words(query)
    same, ranked, page_candidates = [], [], []
    wanted_printed, wanted_pdf = page_range(printed), page_range(pdf)
    if (printed is not None and wanted_printed is None) or (pdf is not None and wanted_pdf is None):
        raise ValueError("invalid page interval")
    def overlaps(a, b):
        return bool(a and b and a[0] <= b[1] and b[0] <= a[1])
    for r in index["records"]:
        own = bool(aliases.intersection(r["sources"]))
        score = len(q.intersection(r["tokens"]))
        brief = {k: r[k] for k in ("id", "path", "blob", "record_type", "sources",
                                   "field_index_incomplete", "locators")}
        if own:
            same.append(brief)
        if any(l["source"] in aliases and (overlaps(l["printed"], wanted_printed) or overlaps(l["pdf"], wanted_pdf)) for l in r["locators"]):
            page_candidates.append(brief)
        if q and score:
            ranked.append((score, own, brief))
    ranked.sort(key=lambda x: (-x[0], -int(x[1]), x[2]["path"]))
    return {"schema": "sr3-review-packet/v1", "head": index["head"], "source": source,
            "printed_range": printed, "pdf_range": pdf, "catalog_candidates": cat,
            "manifest_candidates": manifests, "source_record_count": len(same),
            "source_records": same, "page_candidates": page_candidates,
            "registration_candidates": [ref for ref in index["registration_candidates"] if ref["manifest_path"] in {m["path"] for m in manifests}],
            "query_candidates": [x[2] for x in ranked[:limit]],
            "query_candidate_count": len(ranked), "index_issue_count": len(index["issues"]),
            "duplicate_record_ids": index["duplicate_record_ids"],
            "review_status": "unreviewed_candidates_only", "page_credit": False,
            "instructions": "Verify live blobs, authenticate original PDF, visually review every applicable field; candidate matching never proves equivalence or completeness."}


def compare(index, path, blob, pointer, value):
    matches = [r for r in index["records"] if r["path"] == path and r["blob"] == blob]
    if len(matches) != 1 or matches[0]["field_index_incomplete"]:
        result = "unavailable"
    else:
        existing = matches[0]["fields"].get(pointer)
        result = "unindexed" if existing is None else (
            "exact_typed_value" if existing == scalar(value) else "different_typed_value")
    return {"result": result, "path": path, "blob": blob, "pointer": pointer,
            "review_status": "comparison_only", "page_credit": False}


def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False) + "\n", encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build")
    b.add_argument("--repo", default=".")
    b.add_argument("--ref", default="HEAD")
    b.add_argument("--out", required=True)
    b.add_argument("--packets")
    q = sub.add_parser("packet")
    q.add_argument("--index", required=True)
    q.add_argument("--source", required=True)
    q.add_argument("--query", default="")
    q.add_argument("--printed")
    q.add_argument("--pdf")
    q.add_argument("--out", required=True)
    c = sub.add_parser("compare")
    for k in ("index", "path", "blob", "pointer", "value-json", "out"):
        c.add_argument("--"+k, required=True)
    a = p.parse_args()
    if a.command == "build":
        index = build(a.repo, a.ref)
        write(a.out, index)
        if a.packets:
            for source in sorted({x["id"] for x in index["catalog"] if ID.fullmatch(x["id"])}):
                name = hashlib.sha256(source.encode()).hexdigest()[:16] + ".json"
                write(Path(a.packets)/name, packet(index, source))
            write(Path(a.packets)/"directory.json", {x["id"]: hashlib.sha256(x["id"].encode()).hexdigest()[:16]+".json"
                  for x in index["catalog"] if ID.fullmatch(x["id"])})
        print(json.dumps({"head": index["head"], "records": len(index["records"]),
                          "catalog": len(index["catalog"]), "manifests": len(index["manifests"]),
                          "issues": len(index["issues"]), "duplicate_ids": len(index["duplicate_record_ids"]),
                          "review_status": index["review_status"]}, sort_keys=True))
    else:
        index = json.loads(Path(a.index).read_text(encoding="utf-8"))
        if index.get("schema") != SCHEMA:
            raise ValueError("unsupported index schema")
        value = packet(index, a.source, a.query, printed=a.printed, pdf=a.pdf) if a.command == "packet" else compare(
            index, a.path, a.blob, a.pointer, json.loads(a.value_json))
        write(a.out, value)


if __name__ == "__main__":
    main()
