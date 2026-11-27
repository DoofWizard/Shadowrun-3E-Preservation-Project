# Forward-only Pass B ingestion v2 — owner-directed, 2026-11-27

## Authority and scope

Adopt faster extraction for remaining active mechanical work. This is not a
new queue, source acceptance gate, edition conversion, or historical re-audit.
Closed/accepted sources and independently reconciled scopes stay closed. No
routine re-reading, new historical evidence demands or reopening merely because
this tooling exists. A genuinely demonstrated original mechanical discrepancy
follows the existing authorized correction process. Denver pp46–47 are
owner-authorized archived losses: nonblocking and no page credit. All original
ownership, source verification, editorial, staging, ordinary Contents writes,
exact readbacks, individual confirmation/indexing and acceptance rules remain
binding. No change to worker count, schedules, branch, eight-slice limit, or
exclusive write ownership.

## Production work order

1. **Resume, do not rediscover.** Read the worker's live owned manifest and
   existing finite original-derived checklist. Finish pending lawful
   confirmations/indexing. Select nearest-completable *open* mechanical
   section/table. Prioritize mechanics useful to gameplay rather than lore.
   Reuse unchanged existing closures and exact accepted records; do not create
   another authoritative inventory.
2. **Acquire once and authenticate.** Obtain the cataloged original under the
   existing source acquisition policy. Run actual preservation_method.py
   verify-source against the exact live manifest and retain its result. Pin the
   independently cataloged SHA-256 and independently established physical page
   count. Do not learn these pins from the cache. A source lacking valid pins
   stays in the existing read-only intake workflow. A damaged/truncated source
   uses the existing recovery protocol, not this cache.
3. **Prepare a reusable layout cache.** Run source_cache.py for the open
   source once; it extracts embedded text, bounding boxes, line/span blocks
   and word coordinates for all physical pages (or just a selected range).
   It labels every page unreviewed. Use a trusted persistent scratch directory
   outside the Git working tree. Original PDFs and extracted full-book text
   must not be committed or shared publicly. Reuse the cache within and across
   runs only with exact original SHA, page count, extraction profile and
   independently authenticated source as required by the original policy.
   If persistent scratch is unavailable, rebuild once locally; don't stall.
   Cache checksums detect accidental corruption, not malicious modification
   or historical review. The original page image is authoritative.
4. **Escalate selectively.** Reliable text/coordinates speed prose and table
   extraction; numeric-dense and multi-column hints identify where to zoom.
   Sparse text, wrong glyphs, ambiguous reading order, complex tables and
   scans require original pixel review and, if useful, local OCR or layout
   specialist extraction (e.g. Docling/Marker/PaddleOCR). Those backends are
   optional evaluation candidates, not deployed dependencies or accuracy
   authorities. Don't upload private source material to public services.
   Use cached page renders on demand; visually inspect every game-affecting
   original rule, table cell, footnote, sign, modifier and exception. No
   automated hint proves a page contains zero rules, a table is correct or
   a source is complete. Physical page labels are not printed folios; verify
   mapping from original evidence.
5. **Extract natural groups, not individual fragments.** Enumerate all original
   mechanics in a section: named action/test, actor and target, dice/pools,
   TN, timing, conditions, units, damage/staging, costs, requirements,
   exceptions, examples, optional status and edition lineage. For tables,
   check row/column counts, merged headers, blanks/dashes and footnotes against
   source pixels. Compare typed source-derived fields against current
   canonical records before writing. Batch independent reads/comparisons and
   preparation of 2–4 genuine related records, up to existing per-run limits.
   Preserve one content class per record. Never inflate record/commit counts.
6. **Verify and publish exactly as before.** Independently source-review
   baseline and same-substance candidate; never create baseline from candidate.
   Use existing editorial playbook, actual transaction_recovery.stage and
   ingestion_gate.prepare, normal Contents write of exact prepared UTF-8,
   actual commit/blob/byte readback, individual ingestion_gate.confirm,
   individual source registration/readback and durable original journal.
   Serialize writes, use fresh blob leases, no alternate API or replay of
   denied unchanged bytes. Advance a contiguous boundary only under the
   existing authorization gate; no new page credit from preparation.
7. **Keep work moving.** Record precise unresolved mechanical fields vs
   historical archival receipt debt in the existing owned dossier. Don't
   repeatedly hunt unchanged missing artifacts. When a specific item is
   blocked, proceed to an unrelated eligible owned open scope in the same
   run. Acceptance specialist keeps using the existing read-only verifier
   and authenticated evidence; does not reopen formally accepted books or
   issue automatic source decisions. Existing coordinator-only routing and
   ownership adjudication remain in force.

## Bounded 404 recovery (2026-11-27)

Apply at the first observed 404, not on every successful transaction. Preserve
the exact diagnostic, operation, repository, branch/ref, case-sensitive path,
stable record ID and expected/observed blob or commit when available. Do not
infer a provider status from a wrapper error. The offline diagnostic is:

    python tools/ingestion/transaction_recovery.py classify-failure read "HTTP 404"

Pass --http-status 404 only for a separately observed GitHub response.
"404: Action not found" before action invocation is a tool-route failure, not a
missing GitHub file. A connector-level safety rejection remains a separate
restriction; do not bypass or replay denied content.

For repository path resolution, use the live owned source manifest and its
registered ID/path and blob as the first locator, then the canonical lineage
index or a bounded directory/tree listing at the intended ref. Never infer
a path from the record's topic (e.g. True Names belongs at
rules/spirits/true-names.yml). Inspect exact spelling/case and verify the live
ID, source and blob against the expected evidence. Use a known accessible
repository/ref and parent listing to distinguish a genuinely missing file from
a bad ref, stale path or insufficient access. A bare read 404 is not evidence
that a prior write failed or that the file is absent. Do not create duplicates
or silently rewrite historical paths/receipts.

For an attempted write with uncertain result, retain the exact prepared journal.
Use ordinary read-only checks of the intended ref/path and actual commit.
If the exact candidate blob and actual commit are established, follow normal
ingestion_gate.confirm and source-specific indexing. If they differ or cannot
be located, preserve the pending item and report the precise blocker; do not
overwrite a divergent blob or infer page credit. No retry of denied unchanged
bytes, alternate write APIs, fabricated confirmation or disabled workers.
Only a demonstrably resolved condition and existing authorization permit a
normal Contents operation. For semantic writes, use preservation_method.py
log-failure and decide; do not supply --remote-absent from a bare 404.

Limit each blocked path to one targeted manifest/index/parent lookup and one
corrected exact-path read when warranted. If unresolved, continue another
eligible owned open scope in the same run; do not repeatedly guess paths or
create another queue. Route-level failures in automation monitoring are handled
by the coordinator using supported task status lookup; do not change workers'
schedules or duplicate tasks to compensate. These diagnostics do not replace
any verification, acceptance or source-ownership gate.

## Running the cache

Python 3 with PyMuPDF. Initial benchmark used PyMuPDF 1.26.7. Fetch the live
tool and verify its exact Git blob before reuse. Run existing source verification
first.

```sh
python tools/ingestion/source_cache.py \
  --pdf /trusted/original.pdf --sha256 LIVE_PINNED_SHA256 \
  --expected-pages KNOWN_PHYSICAL_COUNT --cache /trusted/scratch/sr3-cache \
  --select all
```

For an open 2–4-record natural section, use physical page selection such as
`--select 207-210 --render-dpi 180`; zoom higher for tiny cells/footnotes.
The tool reports its cache path; pNNNN/layout.json stores text and coordinates,
and optional image-DPI.png stores render pixels. It hashes the actual source
bytes on each invocation. Renders are lazy to avoid needless storage and
processing. Tool profile includes schema and PyMuPDF version; bump schema on
incompatible extraction changes. Run the local regression suite:

```sh
cd tools/ingestion
python -m unittest -v test_source_cache
```

## Initial real-source performance evidence

Open source FanPro25007, Shadows of Asia, original 232 physical PDF pages,
16,290,405 bytes, independently matched live manifest SHA-256
ff7106b5cb9e484ce668b3e54f8aa7ce3734579aa9b3cadeb7f64f37d3666c3f.
Local full-book embedded-text/layout extraction: 232 misses, 2.232 seconds.
Repeat retrieval: 232 hits, 0.938 seconds. Hints: 214 possible-column pages,
28 numeric-dense pages, 10 sparse-text pages (overlapping categories).
Eight synthetic regression tests passed. Code/test Git blobs:
2f3e6d96793ac64ddef52fa91a61cb2dd19df9b4 and
347d8eb09988a4bda0d9c8751db726927899e118. These are preprocessing results,
not an executed production source acceptance, OCR accuracy benchmark or
end-to-end speedup. No rules or page credit awarded. The benchmark cache is
local, not a durable shared cache across workers.

## Throughput metrics for each existing worker report

Report actual time spent on preparation, source review, publication and
receipt recovery when available; new/corrected verified mechanical fields and
confirmed/indexed records; open scopes conclusively reconciled; unresolved
critical source discrepancies; separate historical receipt debt. Record cache
hits/misses and when the fallback path was necessary. Unknown timings remain
unknown. Avoid fixed minimum commits or artificial progress. Aim to double
verified new/corrected fields per active worker-hour on comparable open
sections while retaining zero unresolved critical numeric/semantic
discrepancies at acceptance; this is an engineering target, not a guarantee.
Evaluate over comparable new open scopes; do not reopen closed books to
benchmark them. If a tool slows or misreads a page, use the proven manual
review path immediately and continue.

## Design references (methods only, no imported canon)

- Foundry PF2e data-entry and review style guide:
  https://github.com/foundryvtt/pf2e/wiki/Style-Guide
- Docling layout/table pipeline: https://github.com/docling-project/docling
- olmOCR batch extraction: https://github.com/allenai/olmocr
- DevdrawDIY SR3E: https://github.com/devdrawdiy/sr3e (implementation comparison,
  never rule authority or code import).
