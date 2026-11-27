# Expanded-source candidate acceptance (v1 prototype, 2026-11-26)

This is a read-only engineering tool for the coordinator. It does not replace
the original transcription, editorial review, staging, Contents write,
confirmation, indexing or final acceptance gates. It never updates manifests,
rules, CORE, checkpoints or page credit. A PASS means the separately trusted
inputs agree for the supported scope; it is not a source or corpus certificate.

## Inputs and trust boundary

Use a full local Git object database at the freshly observed authorized
branch commit. The CLI reads immutable Git objects; it does not fetch or write
the repository. The coordinator must independently pin the HEAD and three
input SHA-256 digests, after checking the originals and their provenance.
Do not take the hashes from an untrusted bundle's own assertions. Acquire the
cataloged original PDF from Drive under the existing source protocol.

The three UTF-8 JSON files are views of the existing source dossier and
original evidence, not another persistent queue. Synthetic test fixtures are
never source evidence. Keep all individual original journals and confirmations.

* Review: protocol sr3-expanded-acceptance/v1, reviewer, source (id, sha256,
  edition SR2/SR3, catalog, publisher, physical_pages, manifest path),
  unresolved_fields, expected_printed_folios, unrepresented_printed,
  contradictions, and pages.
* Each page: physical pdf number, printed folio (null for unnumbered),
  heading, image_review (actual independently reviewed original evidence
  locator), disposition, fields. The physical page sequence must cover the
  actual PDF. Mechanical pages have at least one original-derived field;
  zero_rules pages require an explicit reason. Owner omissions require
  authority, reason and no_page_credit=true. Missing printed folios outside
  the actual PDF require an independent unrepresented_printed disposition
  (accepted_scan_omission or original_folio_not_present), printed, reason,
  authority and no_page_credit=true. Never infer an unseen page is blank.
* Each field: unique id, actual heading, class (one permitted mechanical
  class), kind (rule, row, condition, exception, example, procedure), lineage,
  and exact typed value independently derived from the original. Enumerate
  every heading, rule, row, qualifier and exception; do not derive obligations
  from existing canon. A substantive structured value may represent a complete
  independently reviewed group. Values must preserve exact numeric/string
  types, units, lists, original terminology and edition.
* Lineage: sr3_effective, sr3_optional, sr2_unsuperseded, sr2_superseded or
  preserved_variant. SR2 fields require precedence_review; superseded ones
  require a named_successor. Those references are independently adjudicated,
  not inferred by this program. Contradictions list the distinct field IDs,
  disposition preserve_distinct_variants and reason. No collapse or silent
  rule selection is permitted.
* Bindings: mapping from every obligation ID to path and substantive JSON
  pointer under /data/. The set must exactly match the review inventory.
  No root headline/summary may satisfy a rule.
* Evidence: protocol, custodian (distinct from original inventory reviewer),
  transactions keyed by accepted path. Each transaction holds plan (original
  prepare result), confirm (original actual confirm result), baseline_sha256,
  prewrite_journal_artifact (baseline, candidate, plan), historical_confirm_artifact,
  editorial_review_artifact, index_commit, and index_pointer into the source's
  live registered entry. Each artifact is original_locator, sha256 and
  bytes_base64 (exact original bytes). A bare manifest gate label is not evidence.
* Editorial artifact JSON must bind source, source_sha256, edition, publisher,
  catalog, path, candidate_sha256, baseline_sha256, printed_pages, pdf_pages,
  reviewed_edition_scope, baseline_reviewed_independently=true,
  candidate_reviewed_independently=true and nested_text_reviewed=true. Only
  use genuine retained editorial evidence; no newly fabricated historical
  document or chronology. The referenced original journal must genuinely
  predate its write and the original confirm must follow the actual readback.
  The coordinator verifies custody and chronology; hashes and Boolean fields
  alone cannot establish them.

The CLI checks actual physical PDF length and runs the pinned original
preservation_method.py verify-source, verifies the manifest and exact original
source identity, checks each typed field and page/class binding, compares
journal bytes and immutable baseline/candidate substance, checks historical
confirmation, exact-path Git commits and ancestry, and compares the actual
historic and current registered index entries. It then executes the pinned
ingestion_gate.py prepare on the retained bytes as a present-day consistency
recheck, not a newly recovered historical receipt. A changed path or missing
artifact blocks; no semantic transaction is issued. All output is diagnostic
JSON. Exit 0 is PASS, exit 1 is BLOCKED.

```sh
python tools/expanded_acceptance/validator.py \
  --repo /local/repo --head ACTUAL_FULL_COMMIT \
  --pdf /fresh/cataloged-original.pdf \
  --review /local/review.json --review-sha TRUSTED_REVIEW_SHA256 \
  --bindings /local/bindings.json --bindings-sha TRUSTED_BINDINGS_SHA256 \
  --evidence /local/evidence.json --evidence-sha TRUSTED_EVIDENCE_SHA256
```

Requirements: Python 3, Git, PyYAML, PyMuPDF. The existing source verification
and preflight scripts are materialized from the pinned commit into temporary
directories only. Nothing writes to the authoritative repository.

## Limits and next implementation scope

This version supports source-local registered records with numeric printed/PDF
range notation and a stable index pointer. Shared cross-source equivalence,
unnumbered mechanical page bindings, renamed/moved index entries, heterogeneous
historic index schemas and legacy receipt layouts require explicit adapters
and independent evidence; unsupported inputs must remain blocked, not treated
as missing original mechanics. Source precedence references and source
completeness are not machine-derived. A human must verify the original
inventory completeness, image review, editorial truth, named supersession
and artifact chronology before certification. A PASS does not assert that
every other book or engine adapter is ready. The prototype is deliberately not
a final acceptance gate.

## Companion handoff (read-only)

At inspected main d6377ec4aab2e8b5a4ec9b63ef9867d59885f4ca, SRComp manifest blob
4c014f59d657cb872eef541f8a2693b26d8d2a6e, the existing book checklist records
138 physical pages, 18 scopes and no demonstrated remaining mechanics gap.
Printed p130/PDF131 Actions: 187 mapped rows, 37 owned exact rows, 150 remaining
original receipt links, zero remaining unmapped shared rows; formal section
acceptance false. Preserve the existing row/legacy-label mappings and distinct
variants (including focus deactivation classifications and CCSS system versus
opposed-combat disengagement). Do not equate Animal Gateway and Astral Gateway
without evidence. The recorded original PDF SHA-256 is
8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5; this is a
manifest read, not a fresh source verification in the engineering run.
No Companion or shared canon mutation is authorized by this handoff.
For source-wide certification, original receipt links/shared equivalence and
independent coordinator adjudication remain outstanding.

## Reproducible engineering checks and exact readbacks

```sh
cd tools/expanded_acceptance
python -m unittest test_validator test_integration.IntegrationTests -v
```

18 tests passed locally on 2026-11-26: 17 structural/adversarial fixtures and
one integration fixture using a synthetic two-page PDF, actual local Git
commits, actual existing prepare/confirm and verify-source, a PASS followed
by BLOCKED after altering an indexed record. These tests are not source evidence.
The existing cache matched all eight live pinned dependency blobs and passed
29 preflight, 40 ingestion/preservation, and 16 recovery tests.

Exact ordinary Contents commit and fresh commit/live byte readback:
* validator.py: a6eb1f59ef829387e2ea9d0f342e0df2556e6b70,
  blob b7a65588cc7e3dc4222dbf6cffd7cefdeba10cf0.
* test_validator.py: 432773bff6e87cffe651e8666144db18e5b2efc8,
  blob 846930c662e602fe13973f62056bb7762e6901d7.
* test_integration.py: 5925c4bb26cc0904313a6c129e5c5e788ed2cb12,
  blob e90478358fcac94429692b753b0043fd57d17e13.

Read-only precedents at inspected main: core_acceptance.py blob
c138b427cd38382b1e77555dae743a86e3d192ec; core-acceptance.md blob
04654facf92cd7389c3cf93180d617dabe304c6a; ingestion_gate.py blob
a123f7f374822c5f899d3e9df3c7f8709d80abf2; transaction_recovery.py blob
ef6a9361e93996eba2b9102b5447e71fef230d4e; preservation_method.py blob
258a6d16510673cbeba66f4431f80f3fb97ce5cd; connector_preflight.py blob
331626d7c285b00e541359e315ae2bdd0fa33f2d. No protected gate or existing test
was changed. No real book assessment, semantic record acceptance, historical
receipt recovery, or global page advancement is claimed.
