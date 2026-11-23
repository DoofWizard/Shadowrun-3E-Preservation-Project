#!/usr/bin/env python3
"""Source-authenticated continuous DRAFT queue. NEVER writes canonical repository.

Canonical acceptance still requires fresh original Drive review, independent
BASELINE/CANDIDATE, stage/prepare, ordinary GitHub Contents, exact readback,
confirm, and source-specific index readback by the authorized specialist.
"""
from __future__ import annotations

import argparse
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
SOURCE_OWNER = {
    "coordinator": {"FanPro10662"},
    "magic": {"FASA7907"},
    "augmentation": {"FASA7126"},
    "combat": {"FASA7908"},
    "character": {"FASA7905a"},
    "matrix": {"FASA7909", "FASA7219"},
    "sota": {"FanPro10664", "FanPro25004"},
    "legacy": {"FASA7109"},
    "critters": {"FASA7002", "FanPro10667", "FanPro10650",
                 "FanPro10666", "FanPro10653"},
    "sourcebooks": {"FASA7118", "FASA7115", "FASA7215", "FASA7124",
                    "FanPro10657", "FanPro25002", "FanPro25007",
                    "FanPro25006", "FanPro25003", "FanPro25014"},
}
ID = re.compile(r"[a-z][a-z0-9_-]{2,80}\Z")
MANIFEST = re.compile(r"sources/manifests/[A-Za-z0-9&._-]+\.yml\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")


def load_queue(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("jobs"), list):
        raise ValueError("invalid_queue")
    jobs, ids = data["jobs"], set()
    for j in jobs:
        if not isinstance(j, dict) or not isinstance(j.get("id"), str):
            raise ValueError("invalid_job")
        if not ID.fullmatch(j["id"]) or j["id"] in ids:
            raise ValueError("duplicate_or_invalid_job_id")
        ids.add(j["id"])
        if j.get("shard") not in SOURCE_OWNER or j.get("catalog_number") not in SOURCE_OWNER[j["shard"]]:
            raise ValueError("cross_shard_ownership:" + j["id"])
        if not isinstance(j.get("manifest"), str) or not MANIFEST.fullmatch(j["manifest"]):
            raise ValueError("invalid_manifest_path")
        if not isinstance(j.get("original_printed_pages"), str) or not j["original_printed_pages"].strip():
            raise ValueError("missing_printed_pages")
        pages = j.get("original_pdf_pages")
        if not isinstance(pages, list) or len(pages) > 12 or any(type(n) is not int or n < 1 for n in pages):
            raise ValueError("invalid_original_pdf_pages")
        if pages != sorted(set(pages)):
            raise ValueError("duplicate_or_unsorted_pdf_pages")
        if not isinstance(j.get("section"), str) or not j["section"].strip():
            raise ValueError("missing_mechanical_section")
    return jobs


def original_hash(manifest):
    raw = Path(manifest).read_text(encoding="utf-8")
    matches = re.findall(r"^source_pdf_sha256:\s*['\"]?([0-9a-f]{64})['\"]?\s*$", raw, flags=re.M)
    if len(matches) != 1 or not DIGEST.fullmatch(matches[0]):
        raise ValueError("invalid_live_source_manifest_sha256")
    return matches[0]


def original_pdf(folder, catalog, expected):
    if not folder.is_dir():
        raise FileNotFoundError("source_pdf_folder_missing")
    candidates = [p for p in folder.rglob("*") if p.is_file()
                  and p.suffix.casefold() == ".pdf"
                  and catalog.casefold() in p.name.casefold()]
    if not candidates:
        raise FileNotFoundError("cataloged_original_pdf_not_staged")
    matches = []
    for p in candidates:
        with p.open("rb") as f:
            if hashlib.file_digest(f, "sha256").hexdigest() == expected:
                matches.append(p)
    if len(matches) != 1:
        raise ValueError("original_pdf_hash_missing_or_ambiguous")
    return matches[0]


def verify_source(repo, pdf, manifest):
    cmd = [sys.executable, str(repo / "tools/ingestion/preservation_method.py"),
           "verify-source", str(pdf), str(manifest)]
    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if completed.returncode:
        raise ValueError("actual_verify_source_failed:" + (completed.stdout + completed.stderr)[-300:])
    result = json.loads(completed.stdout)
    if result.get("status") != "source_pdf_hash_verified":
        raise ValueError("original_source_not_verified")
    return result


def render_pages(pdf, numbers, target):
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("pymupdf_not_installed") from exc
    rendered = []
    with fitz.open(pdf) as original:
        for n in numbers:
            if n > len(original):
                raise ValueError("original_pdf_page_out_of_range")
            png = target / ("original-pdf-%03d.png" % n)
            original[n - 1].get_pixmap(
                matrix=fitz.Matrix(1.5, 1.5), alpha=False
            ).save(str(png))
            rendered.append(png)
    return rendered


def prompt(job, sha):
    return f"""Shadowrun original-source mechanics preservation: PROPOSAL ONLY.
Assigned source owner shard: {job['shard']}. Exact catalog: {job['catalog_number']}.
Original manifest: {job['manifest']}. Original PDF SHA256: {sha}.
Mechanical section: {job['section']}.
Cited printed pages: {job['original_printed_pages']}.
Original physically rendered PDF page numbers: {job['original_pdf_pages']}.

Visually inspect ALL ATTACHED original source page images. Review natural section
mechanics, every numeric table, modifier, exception, stat and dependency, and
compare existing accepted same-source canonical records BEFORE proposing anything.
Preserve the original edition: a 2E mechanic is not implicitly SR3-compatible.
Use the established editorial playbook: source-attributed fictional prose, no
loss of exact mechanical meaning, independent original-source BASELINE and
same-substance CANDIDATE with exactly one valid content_class.

Work in this temporary copy only. Write field-level analysis to
_proposals/{job['id']}/report.md, and draft YAML if genuinely missing.
If images are unreadable or data is unverified, report blocked; never fill gaps
with plausible conjecture. If already complete, document no-op.

CRITICAL: DO NOT COMMIT, PUBLISH, GIT PUSH, UPDATE MANIFESTS, OR TOUCH OTHER SHARDS.
This runner cannot perform the required independent fresh Drive acquisition,
source-owner transaction_recovery stage/prepare, normal GitHub Contents write,
readback, ingestion_gate.confirm, source index, or corpus acceptance. No
completed work here is accepted canon. FASA7001 core 451 records and
Denver printed p45 / PDF46 checkpoint stay immutable.
"""


def save_status(target, record):
    target.parent.mkdir(parents=True, exist_ok=True)
    enriched = dict(record, recorded_at=datetime.now(timezone.utc).isoformat(),
                    canonical_records_accepted=0, globally_authorized_pages=0)
    temp = target.with_suffix(".tmp")
    temp.write_text(json.dumps(enriched, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    temp.replace(target)
    return enriched


def process(job, repo, pdf_dir, output_dir, codex, dry_run=False):
    dest = output_dir / job["id"]
    state_file = dest / "status.json"
    if state_file.exists() and not dry_run:
        previous = json.loads(state_file.read_text(encoding="utf-8"))
        if previous.get("status") in {"proposal_prepared", "review_only", "blocked"}:
            return {"id": job["id"], "status": "already_processed_or_blocked"}
    try:
        if not job["original_pdf_pages"]:
            raise ValueError("original_pdf_page_mapping_not_source_authenticated")
        manifest = repo / job["manifest"]
        if not manifest.exists():
            raise FileNotFoundError("live_source_manifest_missing")
        digest = original_hash(manifest)
        pdf = original_pdf(pdf_dir, job["catalog_number"], digest)
        if dry_run:
            return {"id": job["id"], "status": "ready", "sha256": digest,
                    "original_pdf": str(pdf)}
        if not shutil.which(codex):
            raise RuntimeError("codex_cli_missing_or_not_authenticated")
        actual = verify_source(repo, pdf, manifest)
        with tempfile.TemporaryDirectory(prefix="sr3_draft_") as tmp:
            workspace = Path(tmp) / "source"
            shutil.copytree(repo, workspace,
                            ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                          ".venv", ".sr3-continuous"))
            images_dir = workspace / "_original_page_images"
            images_dir.mkdir()
            images = render_pages(pdf, job["original_pdf_pages"], images_dir)
            drafts = workspace / "_proposals" / job["id"]
            drafts.mkdir(parents=True)
            final = drafts / "last_message.txt"
            cmd = [codex, "exec", "--ephemeral", "--sandbox", "workspace-write",
                   "--skip-git-repo-check", "-C", str(workspace),
                   "--output-last-message", str(final)]
            for image in images:
                cmd.extend(["--image", str(image)])
            cmd.append(prompt(job, digest))
            env = os.environ.copy()
            for key in ("GITHUB_TOKEN", "GH_TOKEN", "GIT_ASKPASS",
                        "GOOGLE_APPLICATION_CREDENTIALS"):
                env.pop(key, None)
            proc = subprocess.run(cmd, cwd=workspace, env=env,
                                  text=True, capture_output=True, timeout=3600)
            if proc.returncode:
                raise RuntimeError("codex_failed:" + (proc.stderr or proc.stdout)[-400:])
            report = drafts / "report.md"
            if not report.exists() or not report.read_text(encoding="utf-8").strip():
                raise RuntimeError("missing_source_review_report")
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(drafts, dest)
            kind = "proposal_prepared" if list(drafts.glob("*.yml")) else "review_only"
            return save_status(state_file, {
                "id": job["id"], "status": kind, "sha256": digest,
                "actual_verify_source": actual,
                "manifest_records_indexed": 0,
            })
    except Exception as exc:
        return save_status(state_file, {
            "id": job["id"], "status": "blocked", "reason": str(exc)[:500],
        })


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path.cwd())
    ap.add_argument("--source-dir", type=Path, required=True)
    ap.add_argument("--results-dir", type=Path, required=True)
    ap.add_argument("--queue", type=Path, default=HERE / "queue.json")
    ap.add_argument("--shard", choices=("all", *SOURCE_OWNER), default="all")
    ap.add_argument("--codex", default="codex")
    ap.add_argument("--max-parallel", type=int, default=2)
    ap.add_argument("--poll-seconds", type=int, default=60)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not 1 <= args.max_parallel <= 10:
        ap.error("max-parallel must be between 1 and 10")
    if args.poll_seconds < 15:
        ap.error("poll-seconds must be at least 15")
    repo, pdf_dir, output_dir = (args.repo.resolve(),
                                 args.source_dir.resolve(),
                                 args.results_dir.resolve())
    if not (repo / "tools/ingestion/preservation_method.py").is_file():
        ap.error("repo must be a full checked-out preservation project")
    if repo == output_dir or repo in output_dir.parents:
        ap.error("results-dir must be outside the canonical repo")
    if not args.dry_run and not shutil.which(args.codex):
        ap.error("Codex CLI not installed; connect/authenticate execution machine")
    while True:
        jobs = [j for j in load_queue(args.queue)
                if args.shard in ("all", j["shard"])]
        to_process = []
        for job in jobs:
            status = output_dir / job["id"] / "status.json"
            if not args.dry_run and status.exists():
                state = json.loads(status.read_text(encoding="utf-8"))
                if state.get("status") in {"proposal_prepared", "review_only", "blocked"}:
                    continue
            to_process.append(job)
        if to_process:
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=args.max_parallel) as pool:
                for result in pool.map(
                    lambda j: process(j, repo, pdf_dir, output_dir,
                                      args.codex, args.dry_run), to_process):
                    print(json.dumps(result, sort_keys=True), flush=True)
        else:
            print(json.dumps({"status": "queue_exhausted_or_blocked",
                              "jobs": len(jobs)}), flush=True)
        if args.once:
            break
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
