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

## Split historical journal adapter (v1 diagnostic, 2026-11-26)

`tools/expanded_acceptance/archive_adapter.py` supports the actual retained
split prewrite/confirmed ZIP layout and root correction registration schema
observed in the Companion worked character examples. It is a separate
read-only diagnostic, not yet wired into validator.py. It requires separately
pinned archive SHA-256 values and Git blobs observed at the original semantic
commit, current record, and original index commit. It compares all four
prewrite members byte-for-byte, checks the exact original confirmation and
index registration, and actually re-executes the unchanged prepare and confirm
scripts as present-day consistency checks. It rejects unexpected/duplicate
members, changed archives, missing evidence and divergent record/index bytes.
It does not extract archives to arbitrary paths or mutate Git.

Even consistent archives return BLOCKED: the original text review is not
invented into a historical structured editorial receipt. Independently verify
its custody, exact source/page/class/edition binding, chronology and source
images; check exact-path ancestry and current index entry before any candidate
acceptance. The caller must independently authenticate the supplied gate
scripts and the external pins. The CLI always exits 1; inspect
journal_consistency for the narrower successful diagnostic. No new gate
receipt is issued. Other index shapes and shared-source equivalence remain
unsupported.

Engineering evidence, 2026-11-26: the already-known point-buy example journal
pair (Library IDs libfile_34491f51843c819189ccabda7a0636b5 and
libfile_4670cc0116b48191a7266069864b5ed9) was actually materialized and checked.
Archive SHA-256 values respectively:
130ffd89defd12a801b83ad8c309bf8d38ac77be91c97cb3f6b6b09345d5cb41 and
ee455f29b9c866b9a433b20e5ff037e7815160f7a20d99bf6da05db9ed42cea6.
Original plan SHA-256 470515d9027982ddca86bd94a89101450ecc0efd825c1e3d59f2a1caa667912b;
original confirm SHA-256 e25801b022328353f05ffe17b7fbe0a704282098095c4895e2ef96b2276d7234;
original review SHA-256 75ac429ec1607815f82a8bc37871a902c38ca978471238bddee7f7e6e89a4844.
The semantic commit 335e8d007c52897a8a763b9a79974d88ef4511ba and live record
both matched blob 6b534bd0503c815f0a428b7399fda6f06d6559c3. The index commit
37d775931f6c59c6ad6296c45acf2c7f547729e0 matched stored manifest blob
e0560485f789a2b3d99beebafcf06c842911aed7. The exact root registration line
srcomp_point_buy_worked_character_examples_original_p14_15_2026_11_25
was identical in that commit and the current SRComp manifest blob
4c014f59d657cb872eef541f8a2693b26d8d2a6e. Actual prepare and confirm replay
matched the retained receipts. Diagnostic: consistent_stored_evidence,
source acceptance BLOCKED. This is an existing known journal, not a newly
recovered missing receipt, fresh original PDF verification or formal closure.

Eight new archive tests passed (`python -m unittest test_archive_adapter -v`).
The eight runtime dependency blobs matched live main and local integrity;
29 preflight, 40 ingestion/preservation and 16 recovery tests passed.
Exact ordinary Contents commits and fresh commit/live byte readbacks:
* archive_adapter.py: 9f12a2ffa2d05d41037aeece298d5a908040593f,
  blob 11ea9839a0cbaa66d78df94d74017166fc6d3508.
* test_archive_adapter.py: a4405c904d63161849da82c693edb1e98fb331ea,
  blob 7c891542829ca5c880535ea228926e4b3ebc9c7c.

Next: integrate independently authenticated editorial bindings for original
text-review artifacts without rewriting them, verify ancestry and current
registration in the main validator, and then implement explicit cross-source
field equivalence with separately pinned source inventories and transaction
evidence. No canon, source manifests, historical journals or protected gates
changed. Global pages advanced: zero.

## Split archive backend integrated (2026-11-26)

The separate diagnostic above remains unchanged. The main validator now
also supports a transaction with layout `split_archive/v1` (no layout key
continues to select the original structured receipt format). For that
transaction supply pre_base64, post_base64, pre_sha256, post_sha256,
attestation_base64 and attestation_sha256 in the externally pinned evidence
JSON. These are original ZIP bytes, not reconstructed or normalized journals.
The attestation is a NEW independently reviewed binding of the original
text-review artifact, not a replacement historical artifact or gate receipt.
The coordinator must independently authenticate the archives and attestation
and pin the complete evidence JSON before invoking the CLI.

The attestation JSON protocol is sr3-expanded-editorial-binding/v1. It must
contain source, source_sha256, edition, publisher, catalog, path, record_id,
printed_pages, pdf_pages, reviewed_edition_scope, content_class (the original
one-element array), baseline_sha256, candidate_sha256, historical_review_sha256
(the SHA-256 of the unchanged source-review.txt member), pre_sha256,
post_sha256, semantic_commit, index_commit, baseline_reviewed_independently,
candidate_reviewed_independently, nested_text_reviewed and
historical_custody_and_chronology_reviewed (each exactly true); plus reviewer
(distinct from inventory reviewer and custodian) and original_review_locator.
The binding must actually be authenticated by an independent reviewer; a
locally generated claim, self-issued digest or Boolean alone is insufficient.
Missing attestation remains BLOCKED. No actual Companion attestation has been
issued by this engineering run.

The integrated backend checks exact-path semantic/index commits, ancestry to
the pinned head, byte equality of original archives with historical and live
Git record bytes, exact historical manifest bytes, current registration,
original source identity, and the independent attestation against the
immutable original text and record/page/class/edition digests. It runs actual
pinned prepare AND confirm as current consistency rechecks. The outer validator
still checks the complete original-derived inventory and typed bindings and
runs actual verify-source. Unknown archive layouts fail closed. The main
CLI skips a redundant prepare for this backend and reports archive_diagnostics
separately, including historical review/attestation hashes and semantic/index
commit and blob pins. Candidate PASS is not formal acceptance.

Engineering regression: 11 new tests passed with actual local Git commits
and live-blob-matched original prepare/confirm code (synthetic fixtures,
including changed live record/registration, wrong edition or historical
review hash, same reviewer, absent confirm, mismatched pin, typed mismatch,
unindexed head, and unknown layout). These exercise assess, not a fresh
production original PDF. Original protected suites passed 29 preflight and
56 combined ingestion/preservation/recovery tests. All eight dependency
blobs matched the runtime kit and live main. The original validator and
archive adapter local inputs matched b7a65588cc7e3dc4222dbf6cffd7cefdeba10cf0
and 11ea9839a0cbaa66d78df94d74017166fc6d3508 respectively.

Exact ordinary Contents commits, fresh commit and branch byte readbacks,
matching the locally tested Git blobs:
* receipt_binding.py: 6fd61b7e436f3a9fe113fbd33db2dfb073e0c058,
  blob e385e906dad8d77b6c843d8c2609c0b15d1d457e.
* validator.py: 90fe4645a907f4357125bd9639e900920a0ff7c9,
  blob b097bd3f2c2232bb1aee96b473e0cf0d17610f3c.
* test_receipt_binding.py: 5e8c3eb434bbb8056d2d374cac4dd84f81a3c504,
  blob 20cee24ab8f606bc3e30dfca05b232dca1e82115.

Next: explicit cross-source equivalence with separately verified original
inventories and indexed target evidence, retaining edition/optional scope,
conditions, units and conflicts. Companion p130's outstanding receipt links
are not closed. No production original PDF verification, newly recovered
historical receipt, accepted semantic record or formal source decision this
run. No protected files, source manifests, canon or global pages changed.

## All-at-once prerequisite triage (read-only)

Use `tools/expanded_acceptance/blocker_triage.py` **before** the more expensive acceptance validator to enumerate all structurally evident prerequisite problems in one run. This reduces the historical receipt one-error-at-a-time loop. It does not inspect original page pixels, verify source truth, parse Git commits, prove a transaction, resolve cross-source equivalence, approve omissions, or certify any rulebook.

Inputs are **separately and externally pinned** UTF-8 review, bindings and evidence JSON files from the same independently prepared sourcebook dossier already specified above. It never generates a supposedly complete review from existing canonical records or treats an absent rule as a zero-rule page.

```sh
python tools/expanded_acceptance/blocker_triage.py \
  --review /local/book-review.json --review-sha EXACT_SHA256 \
  --bindings /local/book-bindings.json --bindings-sha EXACT_SHA256 \
  --evidence /local/book-evidence.json --evidence-sha EXACT_SHA256
```

The output is deterministic JSON with `status: TRIAGE_ONLY`, a complete list of detected prerequisite blocker codes, counts by category and individual field/path locations. The CLI fails for invalid external input pins; even **zero detected structural blockers is not PASS**. It must be followed by actual original-source editorial review, the independent `validator.py` with the fresh cataloged original PDF, recorded gate checks, and explicit source-level coordinator certification. Any foreign-source field is classified as requiring independently reviewed edition/lineage and accepted target proof; it cannot be silently treated as a source-local binding.

Twelve synthetic tests were actually executed locally with all twelve passing; the source and test GitHub blobs matched the exact locally executed files after ordinary Contents commits and readback:
* Diagnostic source: `tools/expanded_acceptance/blocker_triage.py`; latest validation-hardening commit `facc338e6bad5b42aef2e215277add3b0cb08192`, blob `c305ffb80d6413e8db4745cd49f17cb038854bb2`.
* Regression tests: `tools/expanded_acceptance/test_blocker_triage.py`; latest twelve-case commit `e41cc42239e9c2849060b760127288a939ef7275`, blob `c71c42653bc8e69dcba9abbe039906b7e2c637fa`.

```sh
PYTHONPATH=tools/expanded_acceptance python -m unittest discover -s tools/expanded_acceptance -p test_blocker_triage.py -v
```

**Highest-priority production handoff:** Complete ONE independently sourced full-book review/bindings/evidence pack for the nearest-complete owned supplement (initial candidate: FASA7905a Shadowrun Companion). Use this triage to enumerate exact missing original review/page/equivalence/receipt inputs, and resolve or bound those without fabricating history. Next run `validator.py` against the fresh authentic original PDF and live full Git history. Present the coordinator either a verified source-specific PASS candidate with the independent acceptance prerequisites, or exact BLOCKED reasons, never a synthetic certification or unchanged-status essay. Formal expanded-source/corpus acceptance requires the separate authorized final procedure; no such certification is conferred by this diagnostic.


## Accepted SR3 core equivalence (v1)

`tools/expanded_acceptance/core_equivalence.py` now supports the explicitly opted-in binding mode `sr3-accepted-core-equivalence/v1` inside `validator.py`. This is for a *precise SR3 supplement field whose rule and all conditions are independently reviewed as exactly identical to a genuinely accepted FASA7001 core field*. It does **not** support automatically importing SR2, collapsing conflicting action costs or treating similar wording/numbers as proof.

An original-derived field remains in `review.json` with its exact original published page, heading, source edition, typed value and `lineage`. Instead of a duplicated source-local historical transaction, `bindings.json` selects:

```json
{
  "specific-original-field-id": {
    "mode": "sr3-accepted-core-equivalence/v1",
    "core_obligation": "EXACT_ACCEPTED_FASA7001_OBLIGATION_ID",
    "path": "rules/ACTUAL_ACCEPTED_CORE_RECORD.yml",
    "pointer": "/data/ACTUAL_SUBSTANTIVE_FIELD"
  }
}
```

The externally pinned `evidence.json` includes `accepted_core_equivalence` with protocol `sr3-accepted-core-equivalence/v1`, `core_source_id: source.sr3-core`, original core PDF SHA256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`, independently verified `receipt_commit`, exact `receipt_blob`, and a `comparisons` map keyed by each original source field ID. Each comparison supplies independent reviewer, original source/target image review locators, source ID/hash, original printed/PDF page, original heading, lineage, exact core obligation, relationship `exact_restatement`, and independently reviewed `identical` findings for scope, conditions, exceptions, units and optional-rule status.

The backend checks the historical confirmed FASA7001 source acceptance receipt, historical **accepted** manifest/obligation queue blobs, unique indexed core rule ID/path/blob/field, present-day **unchanged** core record bytes, source-to-core exact *typed* value, and mandatory independent comparison fields. It returns `CORE_FIELD_MATCH_CANDIDATE` and `formal_acceptance: false`. A string reviewer/locator is not, by itself, authenticated evidence; the coordinator separately verifies the actual original-page comparison and custody before accepting any source.

`blocker_triage.py` recognizes this mode and lists missing core receipt, accepted obligation or independently reviewed comparison prerequisites together, without requiring a fabricated *duplicate Companion* historical receipt for a previously accepted original core field. The full validator still requires the genuine sourcebook PDF, all original pages/fields, all remaining source-local actual receipts and global consistency. Unknown and partial equivalences remain BLOCKED.

Real evidence and ownership for the initial FASA7905a Actions p130 source-review handoff are in `docs/ingestion/audits/FASA7905A_EXPANDED_ACCEPTANCE_BRIDGE_2026-11-26.md`. The 38 previously mapped core reference candidates are not 38 automatically accepted rules; original source work recorded 27 exact label matches and 11 qualified/nonliteral cases. Do not silently treat other Critters, MiTS, Matrix, rigging or VR2.0 source material as accepted core.

Local synthetic regression evidence: 17/17 accepted-core equivalence tests passed; 14/14 prerequisite-triage tests passed. Source and test GitHub blobs match the local executed bytes. The integrated validator's complete test suite and the new GitHub Actions run were **not independently observed as passing** in this handoff. New CI workflow: `.github/workflows/sr3-expanded-acceptance-contract-tests.yml`, committed to run the complete test suite on affected changes. This is test automation, not original-source acceptance.


## 2026-11-26 production attempt: Companion Actions and SOTA64 archive handoff

Pinned read-only main: `74c616b8e4afcc03e3f84ab9f03d8ab811c80251`. Fresh cataloged Drive originals FASA7905a (138 PDF pages, SHA256 `8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5`) and FASA7001 (345 physical pages, SHA256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`) independently returned actual preservation_method.py verify-source status source_pdf_hash_verified against live manifest blobs `4c014f59d657cb872eef541f8a2693b26d8d2a6e` and `b0ebffa4985ab544e64857b99e98b17d69ee3184`. Runtime kit eight exact blob checks, 29 preflight and 56 ingestion/preservation/recovery tests passed.

Original Companion p130/PDF131 visually read at enlarged column scale before matching owner inventory. All 187 labels and group placements reconcile (186 literal, one apostrophe typography difference in simple.rigging row 6); class totals 36 Free, 48 Simple, 103 Complex. Printed introduction names SR3, Rigger 2, Virtual Realities 2.0, Magic in the Shadows, and Critters. This is an index of action labels/classes, not a reprint of all underlying rules and conditions. Keep the existing owner checklist as the only inventory.

Historical accepted core receipt `6baeb5dffd92dbdcbe50aa451d637e8ae9702316`, blob `d11888c9f20b5603f874f4e976dff3e23c8cde98`, historical manifest `a79b28a3970668982ef44a5318642ed55848839a`, queue `366ee748f51dbf2b699a26edbc1215352743191d`. Exact historical and current core target `rules/actions/sr3-core-combat-phase-action-timing-p104-108.yml` blob `87371b67cf6ac9e57ffd276d44713eaa3cdafcfd`, semantic commit `5a5cdb69809565fd76f4029933f02be0af75a4c7`. Accepted obligation `obligation.rule.actions.sr3-core-combat-phase-action-timing-p104-108.selected_free_actions`; original core review pointer /review/original_action_economy_checked. Original Core p105/PDF106 visually compared. All eleven exact typed label descendants (/data/selected_free_actions/N/action, zero-based N) and Free classification reconcile: free.general rows 1–7 -> N=8,4,10,3,11,7,12; free.combat rows 1–3 -> N=0,1,5; free.magic row 5 -> N=2. **Bounded label match, not full condition equivalence or certification.** Coordinator must adjudicate whether the appendix reference can use this accepted group without treating unprinted conditions as newly reviewed Companion text. Three specific core condition review leads: free.general 1 Activate Cyberware (original wording on devices not continually switched on versus canonical continuous active control); 6 Observe (original vision enhancement allowance and no actual Perception Test); 7 Speak a Word (original practical phrase allowance subject to GM discretion). Do not reopen closed core or modify these fields on this authority.

Other 27 direct core candidates have no named historical accepted parent covering the referenced groups/fields in the two mapped records: simple.general 1–5; simple.combat 1–6,8–9; simple.magic 2,3,10; complex.general 1–2; complex.combat 2,4,5; complex.magic 2,3,5,9,12; complex.rigging 8. Seek other already accepted exact obligations or independent owner-authorized addenda; never use generic action_economy as a proxy. Remaining 112 shared links retain existing owner mapping, not verified full scope or receipt proof. 37 owned rows retain owner evidence; no reclassification or new mechanical omissions inferred.

Actual blocker_triage.py (blob `e5757595a0c910dc56b14efff770cb84ab4317e0`) ran on locally SHA-pinned partial real inputs: 187 independently read p130 labels, all 187 owner binding leads, historical core receipt references, and explicitly unassembled independent comparisons/custody. TRIAGE_ONLY, 374 diagnostics: 190 original_rule, 164 equivalence, 14 binding, 4 receipt, 1 independence, 1 inventory. These are overlapping diagnostic prerequisites, not missing mechanical rule counts. 176 lineage fields not adjudicated in this partial input, 38 independent comparisons absent, 27 accepted obligations absent, 98 external equivalence proofs absent, 14 legacy/non-/data pointers (complex.decking 5,6,7,17; complex.rigging 2,4,5,7,16–19; free.rigging 4; simple.decking 10). Four source-local record receipt bundles not assembled here, NOT newly established loss. Full independently authenticated pages PDF1–130,132–138, contradiction/edition adjudication, custody/chronology and independent pins still required. Local diagnostic input SHA256s review `accaaecf24b4174834516c4eb679148522502daa0b52078ecfe285975ab61aad`, bindings `b8911c4e64fd14fcdca6171866871c1ad79319c871f07aab6309e520eb9d0fd4`, evidence `f9714def26ac9063bfd35641fb1d25404cf352caf9cc3f7ea48e07773b8858da`; not coordinator-authenticated full acceptance inputs. Actual validator.py (blob `b4520838cf432d93710599a6b6dae419cfa24466`) invoked, BLOCKED at Git cat-file HEAD exit 128: full local Git object database unavailable, git ls-remote failed DNS resolution. No production PASS; actual source verification above executed separately. Do not reconstruct history from connector snapshots.

Distinct SOTA2064 manual archive handoff: freshly acquired recovery archive SHA256 `98da0c21e9b1d1c2ed89d0f7654f9ad314a789b9856beba6efeec673bcafb2ac`; all five nested original archives match their recorded SHA. Actual live-blob-matched ingestion_gate.py prepare and confirm rechecks matched all eight archived original plans/confirm receipts. Fresh exact-path GitHub historical blob reads and historical StateOfTheArt2064.yml index snapshot blob reads matched eight of eight each. Six original index receipts are present in archive; media van and police drone lack original local index receipt; historical GitHub index snapshots exist but are not original local index receipts. Five record blobs unchanged at pinned main; three newer current blobs require separate correction transaction evidence: adept competition `ad92d15ba658ebf52675b31da4ecf76bfd9e0d4e`, custody timing `aa182f9f2ba9c1d88157ac72136d27e4fbecabf5`, international competition `4e2a25fa35d6f897619b5e324679c51dabb34dd0`. Exact original historical semantic/index pins are in the recovered archive recovery-evidence.json, which remains the authoritative handoff; original editorial chronology and original local index snapshot custody not established here. Present-day rechecks are not new historical receipts, fresh SOTA original review or source certification.

New accepted mechanical fields, records, formal source decisions and global page advancement: zero. No source manifest, canon, common gate or schedule changes.


## Offline full-history recovery for the production validator

**Fixed infrastructure bottleneck (not sourcebook certification):** The first real FASA7905a assessment verified both original PDFs but could not run the full local Git proof chain because its ephemeral environment lacked complete Git history. `.github/workflows/sr3-acceptance-history-export.yml` now creates a **portable, complete Git bundle** in GitHub Actions on relevant pushes or manual dispatch, without credentials or external uploads. A full-depth Git checkout verifies that the original FASA7001 acceptance receipt commit is an ancestor of the source HEAD and that all three original immutable receipt/snapshot blobs exactly match. It then bundles a new `acceptance-snapshot` branch at that HEAD, verifies the bundle, restores a fresh local clone from the bundle, and rechecks its HEAD and receipt ancestry before uploading a short-retention (3-day) artifact with:
- `sr3-acceptance-history.bundle`: actual full Git object history and the named `acceptance-snapshot` ref.
- `sr3-acceptance-snapshot.json`: exact source HEAD, accepted core commit/blob, bundle SHA-256 and byte length, reachable commit count, *non*-certification flags.

The bundle is **history transport, not source evidence or a new authority**. The validator still requires the original authenticated PDF, source-reviewed entire-book field inventory, independently pinned review/bindings/evidence inputs, and original historical journals. Neither the JSON nor the workflow certifies mechanical correctness.

### Using the verified bundle without a GitHub clone or working network

1. Obtain the actual workflow run's artifact from the repository's GitHub **Actions → SR3 acceptance complete Git history export**, or through the connected GitHub Actions artifact retrieval tool. Use the repository's authenticated workflow-run/artifact identity, not an arbitrary ZIP or pasted blob.
2. Materialize and extract the artifact outside the authoritative Git working tree. Independently read the intended current/pinned main commit SHA from connected GitHub. Compare the artifact's head and SHA-256 against that pinned source and authenticate the artifact origin; the bundle and its accompanying JSON are not independent attestations of themselves.
3. Use the following local checks and clone (replace `PINNED_MAIN_SHA` with the complete independently observed 40-character SHA):

```sh
sha256sum sr3-acceptance-history.bundle
git bundle verify sr3-acceptance-history.bundle
git clone -b acceptance-snapshot sr3-acceptance-history.bundle /tmp/sr3-full-history
test "$(git -C /tmp/sr3-full-history rev-parse HEAD)" = "PINNED_MAIN_SHA"
git -C /tmp/sr3-full-history merge-base --is-ancestor \
  6baeb5dffd92dbdcbe50aa451d637e8ae9702316 PINNED_MAIN_SHA
test "$(git -C /tmp/sr3-full-history rev-parse \
  6baeb5dffd92dbdcbe50aa451d637e8ae9702316:references/audits/fasa7001-available-source-mechanical-core-acceptance-confirmed-2026-11-21.json)" \
  = "d11888c9f20b5603f874f4e976dff3e23c8cde98"
```

The normal full `validator.py --repo /tmp/sr3-full-history --head PINNED_MAIN_SHA` invocation from the preceding section then works with true immutable historical Git objects. This removes the environment's **unavailable Git history** blocker; it does not resolve missing historical receipt files, original source-only review, the 27 unaccepted Simple/Complex accepted-core group obligations or the remaining 112 shared Companion action references.

**Verification status at authoring:** The bundle/create/verify/clone/HEAD-ancestry procedure was executed successfully using a synthetic two-commit local Git repository; the exact workflow file was committed and independently read back from GitHub. **No actual GitHub Actions run/artifact or full production Companion PASS has yet been independently observed.** Do not advance any acceptance flag from this workflow alone.

## 2026-11-27 mechanics sprint: Companion Actions — additional accepted-parent candidates and one original-rule discrepancy

Read-only assessment at main `47b5be9e09c43380f56be85f979c0386df2a2578`. Exact live Companion manifest `4c014f59d657cb872eef541f8a2693b26d8d2a6e`; core manifest `b0ebffa4985ab544e64857b99e98b17d69ee3184`; catalog `31315a037d5798616e2de8fc9cbaeef0c2e4d8c5`. Fresh cataloged Drive originals independently returned actual `preservation_method.py verify-source` status `source_pdf_hash_verified`:

- FASA7905a: 138 physical pages, SHA-256 `8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5`.
- FASA7001: 345 physical pages, SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`.

Original Companion printed p130/PDF131 and relevant original core action, ranged-combat, reflex-trigger and magic passages directly viewed. Eight protected dependency/editorial blobs matched the runtime kit; actual existing tests passed 29 preflight, 40 ingestion/preservation, 16 recovery. No original receipt was reconstructed or new source transaction performed.

### A. Demonstrated mechanical field mismatch — coordinator/core-owner adjudication required

Companion `simple.combat[2]` is the Fire Weapon (SS, SA or BF) index reference. Core printed p106/PDF107, Fire Weapon, expressly permits firing one shot from each held weapon within a single Simple Action. The current and historically indexed phase record `rules/actions/sr3-core-combat-phase-action-timing-p104-108.yml`, blob `87371b67cf6ac9e57ffd276d44713eaa3cdafcfd`, semantic commit `5a5cdb69809565fd76f4029933f02be0af75a4c7`, field `/data/selected_simple_actions/0/rule` instead requires a separate Simple Action for each weapon. This is a source-versus-field action-economy mismatch, not evidence that all canon omits dual-weapon rules. Original p112/PDF113 and existing `rules/combat/sr3-core-attacker-situational-numeric-p112.yml`, blob `34dfbdc5900e78e3e8524f578640ff38988ea1e8`, `/data/using_second_firearm` preserve pistol/SMG eligibility, +2 TN per weapon, applicable targeting-aid restriction and cross-weapon uncompensated recoil. Generic p115/PDF116 single-weapon action costs do not cancel the special two-weapon provision. Refer this exact field to coordinator/core owner for source-reviewed correction and supplemental accepted-field evidence if authorized. Protected closed core remains unchanged; do not silently rewrite its historical receipt.

### B. Five new alternate historical accepted-parent candidates (index class, not full procedure identity)

Historical acceptance commit `6baeb5dffd92dbdcbe50aa451d637e8ae9702316`, receipt blob `d11888c9f20b5603f874f4e976dff3e23c8cde98`, original obligation queue blob `366ee748f51dbf2b699a26edbc1215352743191d`, original manifest blob `a79b28a3970668982ef44a5318642ed55848839a`. Checked exact historical queue parent pointers and independently fetched historical/current identical target blobs. Compared original p130 index rows with the actual core original printed/PDF pages below. Indices are the existing one-based Companion row identifiers.

| Companion row | Core source | Accepted obligation (prefix obligation.rule.) | Exact data pointer(s) | Required qualification |
| --- | --- | --- | --- | --- |
| simple.magic[2] | 186/195 | magic.sr3-core-conjuring-summon-nature-elemental-exact-p186.nature_spirit_summoning | /data/nature_spirit_summoning/summoned_standby_call | Simple, non-Exclusive; previously summoned standby spirit, shaman still in domain; not summoning |
| complex.magic[2] | 172/173 | magic.sr3-core-astral-projection-attributes-movement-p172-173.projection_actions | /data/projection_actions/enter; /data/projection_actions/exit; /data/projection_actions/during_projection | Exclusive Complex entry and return; ongoing projection restriction remains |
| complex.magic[3] | 189/198 | magic.sr3-core-spirit-control-banishing-exact-p189.banishing | /data/banishing/action | Exclusive Complex; preserve eligibility, contest and original astral restrictions |
| complex.magic[9] | 189/198 | magic.sr3-core-spirit-control-banishing-exact-p189.controlling_spirits | /data/controlling_spirits/action | Exclusive Complex; preserve spirit type eligibility, opposition and summoner bonus |
| complex.magic[12] | 172/173 | magic.sr3-core-assensing-astral-signatures-p171-172.astral_signatures | /data/astral_signatures/timing | Complex Actions equal Force; astral perception, skill test, Drain and intrinsic-signature exclusion remain |

Exact target files and historical/current blobs:
- `rules/magic/sr3-core-conjuring-summon-nature-elemental-exact-p186.yml` — `e470ad27b21804394cfcfa95ea3b5ae43a5e010e`.
- `rules/magic/sr3-core-astral-projection-attributes-movement-p172-173.yml` — `974e21185f2403741453da313896460641e0fb81`.
- `rules/magic/sr3-core-spirit-control-banishing-exact-p189.yml` — `cb1253425d56ef7f027d69bcde0d0b3808a91cc0`.
- `rules/magic/sr3-core-assensing-astral-signatures-p171-172.yml` — `b9bca9574a128959d2136fb95710c3b1fe7db0af`.

These five are source-audited index-class candidates using genuine alternate accepted parent obligations. They are NOT five newly certified rules. Some target values are full procedures rather than the index's label, and the current narrow indexed-action-reference adapter does not automatically approve them. Independent scope/exception attestation, actual validator support and coordinator adjudication remain required. Never infer accepted scope of neighboring fields solely from record membership.

### C. Exact remaining dispositions

All 38 mapped core labels were independently read from original p130 and matched the owner's inventory. Eleven Free rows have the previously established accepted parent `selected_free_actions`; eight bounded label/class matches plus the three separately resolved index abbreviations (Activate Cyberware, Observe, Speak a Word), with original controlling conditions retained. None is newly formally accepted. Of 27 Simple/Complex rows lacking acceptance coverage in the initial two target groups, five now have the alternate parent candidates above; 22 do not yet have independently verified alternate accepted-field proofs:

- simple.general 1–5; simple.combat 1–6, 8–9; simple.magic 3, 10.
- complex.general 1–2; complex.combat 2, 4–5; complex.magic 5; complex.rigging 8.

The Fire Weapon mismatch is within those 22. Core p301/PDF310 confirms the reflex trigger's Simple toggle and original conditions, but the historical acceptance queue does not cover /data/reflex_trigger. Generic core p115 firing-mode provisions and p280 reloading-table lead are not blanket substitutes for unaccepted action groups; p280 source review is still needed for exact candidate conditions.

The existing 112 other-source links (not independently re-reviewed against their foreign originals in this run) remain coverage-only; exact positions below preserve existing mappings rather than imply new missing rules:

- Free: critter 1–6; decking 2–5, 7–9; magic 2, 4, 6–7; rigging 2–4.
- Simple: combat 7; critter 1–4; decking 1–5, 7–8, 10–12; magic 4–7; rigging 2–3, 5–6.
- Complex: combat 1, 3; critter 1, 3, 6–17, 19–33, 35; decking 1, 3, 5–9, 11–15, 17–18; magic 4, 6, 11, 13–14, 20–22; rigging 1–2, 4–5, 7, 10–19.

Totals: critter 40, decking 31, magic 16, rigging 22, combat 3. Existing 37 owned row evidence unchanged. Historical receipt and edition/lineage adjudication debt is separate from mechanics. Existing 18-scope owner inventory is not a newly authenticated complete independent page/field review. Full local authentic Git history bundle and independently authenticated complete 138-page reviewer/binding/custody input pack were not materialized in this run; historical blob snapshots are not a replacement. Prior actual production validator BLOCKED remains; not rerun with invented inputs. The new discrepancy prevents a clean mechanical-fidelity verdict for the mapped action field. No new source semantic/index commit, formal book certification, recovered historical receipt or global page credit. Next: owner adjudicate the exact Fire Weapon field; obtain accepted-parent proof and source review for remaining 22, then group other-source review by actual target publication while preserving original edition and exceptions.


## 2026-11-27 production history recovery and bounded Actions Matrix/rigging reconciliation

**Actual production full-history transport verified.** GitHub Actions run [45953667935](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/actions/runs/45953667935) completed successfully at independently fetched main `ded2a66c23ca848dccc767789521be0b4133f422`. Authenticated artifact 15177752546, `sr3-acceptance-history-45953667935`, downloaded; ZIP SHA256 `8e71ac6fa3a3e67546e2c1febf8a1d7f2cf5c70df1b3a81bcc7fd88be65e1eda` matched GitHub artifact digest. Bundle SHA256 `0659484ebfe5b2a833e27485a0b36b0fc10ab98a84bea580d23634f106ba1913` matched snapshot; actual git bundle verify, clone, non-shallow HEAD, git fsck connectivity, original receipt ancestry and receipt blob `d11888c9f20b5603f874f4e976dff3e23c8cde98` and historical manifest blob `a79b28a3970668982ef44a5318642ed55848839a` checked. This resolves the local-history transport blocker for this pinned HEAD, not missing original evidence.

Fresh Drive PDF acquisition and actual verify-source: FASA7905a `8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5`, FASA7001 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`, both `source_pdf_hash_verified` against live exact manifest blobs `4c014f59d657cb872eef541f8a2693b26d8d2a6e` and `b0ebffa4985ab544e64857b99e98b17d69ee3184`. All eight protected runtime blobs matched; actual 29 editorial + 56 ingestion/preservation/recovery tests passed. Expanded full local discovery did not finish before command timeout; no claim of its pass. GitHub reported expanded contract checks run 45953667928 success at same HEAD.

Original Companion p130/PDF131 and core pp215–219/PDF224–228, p157/PDF158, p152/PDF153 visually inspected. Selected the existing 26-row additional_batch in the unchanged Companion closure checklist, rather than constructing a new queue. Actual typed comparisons matched 32 retained owner field values against canonical records; independently read index class and original controlling procedure classifications agree for these 26 rows. This is bounded action-class coverage, not a full independent review of every target procedure or a new historical receipt. All five target record blobs identical at original acceptance commit and pinned HEAD:

- analysis: rules/matrix/sr3-core-interrogation-analysis-operations-p214-215.yml, `8b2ef0b38fc5e9f2dd4a2f989af38fb45ce0dfff`.
- data: rules/matrix/sr3-core-data-decrypt-edit-locate-p216-217.yml, `7503036d8b8d6a70a456d752d3fb8cbd214d0c1e`.
- grid: rules/matrix/sr3-core-grid-comcall-monitoring-operations-p218-219.yml, `c6b84e61f1b69416c848440e370b81306788cd8f`.
- drone: rules/drones/sr3-core-remote-command-action-comprehension-p157.yml, `ced95d126b7f765220fac091eb48bf6efaa35457`.
- gunnery: rules/vehicles/sr3-core-gunnery-resolution-p151-152.yml, `b263f5a6a25260dc3f458fa8f4957decbf9f9870`.

Historical queue at `6baeb5dffd92dbdcbe50aa451d637e8ae9702316` (not current queue): **20 rows have all corresponding historical accepted parent pointers, 6 rows (8 field bindings) lack them.** Exact obligations are obligation.<record id>.<parent suffix>; pointers below are relative to the named target's /data. One-based Companion row positions are from the existing owner checklist.

| Companion row | Target pointer(s) | Historical accepted parent |
|---|---|---|
| free.decking[2] | analysis listed_operations/1/action; /2/action | missing |
| free.decking[4] | analysis monitored_operations/maintenance_action | missing |
| free.decking[8] | grid operations/5/if_insufficient_active_memory | operations |
| simple.decking[1] | analysis listed_operations/3/action; /4/action | missing |
| simple.decking[3] | data operation_definitions/0/action; /1/action; /2/action | operation_definitions |
| simple.decking[4] | data operation_definitions/3/action | operation_definitions |
| simple.decking[5] | data operation_definitions/4/action | operation_definitions |
| simple.decking[7] | grid operations/3/action | operations |
| simple.decking[11] | grid operations/5/action | operations |
| complex.decking[1] | analysis listed_operations/0/action | missing |
| complex.decking[3] | analysis listed_operations/5/action | missing |
| complex.decking[8] | data operation_definitions/5/action | operation_definitions |
| complex.decking[9] | data operation_definitions/6/action | operation_definitions |
| complex.decking[13] | data operation_definitions/12/action; grid operations/0/action; /1/action | operation_definitions; operations |
| complex.decking[14] | grid operations/2/action | operations |
| complex.decking[15] | grid operations/4/action | operations |
| complex.decking[18] | grid operations/6/action | operations |
| free.rigging[3] | drone declared_action_examples/free/1 | declared_action_examples |
| simple.rigging[2] | drone declared_action_examples/simple/0 | declared_action_examples |
| simple.rigging[3] | drone declared_action_examples/simple/3 | declared_action_examples |
| simple.rigging[5] | drone declared_action_examples/simple/2 | declared_action_examples |
| simple.rigging[6] | drone declared_action_examples/simple/3 | declared_action_examples |
| complex.rigging[10] | drone declared_action_examples/complex/1 | declared_action_examples |
| complex.rigging[11] | gunnery sensor_enhanced/lock_action | missing |
| complex.rigging[12] | drone declared_action_examples/complex/2 | declared_action_examples |
| complex.rigging[13] | drone declared_action_examples/complex/3 | declared_action_examples |

Do not expand index abbreviations into unconditional rules: monitored operations require maintenance each Initiative Pass and restart test on interruption; memory unloading Free applies to insufficient active memory before loading (Simple, no test); decrypt prerequisites, ongoing download interruption, monitored slave/comcall procedures and separate grid logons remain controlling. Drone status report is single-drone; identical simultaneous Free actions require captain's-chair mode, not distinct actions; direct primary-drone operation is separate from command issuance; secondary observation is Complex while controlling a primary; sensor lock requires successful Sensor Test before the separate sensor-enhanced attack. All conditions remain in original target records; no inferred CCSS, later Matrix or SR2 equivalence. No new discrepancy demonstrated in these bounded index class comparisons.

Real pinned-input triage on this partial 26-row/32-field diagnostic: TRIAGE_ONLY, 41 equivalence, 1 independence, 1 inventory and 4 original_rule diagnostics (overlapping prerequisites, not missing rules). Input SHA256 review `279274e8771d79899a6480cd8bc87f2361d873a8757faf028ccf92946f11b2e9`, bindings `89292fd54f089f9d78bd591b8e205b928c73484d51df36ad54527dd339d317eb`, evidence `aaeb4f0d6e8f9dc7f9d1ba372fa0e3d143d06fafdf04c54ee6c323b08baf34f9`. Actual validator with full restored production Git and fresh original Companion PDF executed and returned `{"status":"BLOCKED","reason":"independent_review_required","formal_acceptance":false,"global_pages_advanced":0}`. Not an environmental Git failure: authentic independently pinned custodian, full source-derived field/page review (PDF1–130,132–138 outside this bounded review), row-level comparison attestations, source-local original journals and contradiction/edition adjudication remain required. No fabricated custodian, historical journal, zero-rule disposition or equivalence.

Remaining original action references: 86 of previously listed 112 other shared mappings still outside this bounded source comparison; the six newly isolated missing-parent rows are documentary/acceptance obligations, not six missing mechanics. The previously recorded 22 unresolved Simple/Complex accepted-parent candidates and Fire Weapon field discrepancy remain with appropriate owner; 11 Free and five alternate parent candidates are not promoted to formal acceptance. New semantic records/corrections, recovered historical receipts, formally accepted sources and global pages advanced: zero. No protected path or worker control modified.


## 2026-11-27 bounded Companion/Critters action index reconciliation

Fresh observed main `692d1132d5e595956106ccf6dd31bb503f4dd8a2`. Restored and checked authentic non-shallow historical bundle at `ded2a66c23ca848dccc767789521be0b4133f422` (run 45953667935, artifact 15177752546, verified ZIP and bundle SHA256 and core receipt ancestry). The older local HEAD is explicitly not current main. Current main Contents readbacks matched both exact source manifests, all eight target record blobs, the power framework, catalog, both handoffs, editorial playbook, protected gate/test blobs and expanded validator/triage code used below. Actual tests: 29 preflight, 20 ingestion, 20 preservation, 16 recovery passed.

Fresh cataloged Drive originals independently hashed and actual preservation_method.py verify-source returned source_pdf_hash_verified for Companion FASA7905a (SHA256 `8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5`, manifest `4c014f59d657cb872eef541f8a2693b26d8d2a6e`) and Critters FASA7002 (SHA256 `40f9991ad10d7453e39bcd7fdc7dd4600cb29892facf641de13ee9c34880bef7`, manifest `6e27751e549e98f61c46dda5963bb36770c256cd`). Visually read original Companion p130/PDF131 and Critters printed/PDF pp7–14. The source-derived bounded comparison used 39 original index labels, 156 typed original detailed profile fields (type, action, range, duration), and 18 selected numerical or variant fields. All 213 comparisons matched current canon/owner label inventory; no demonstrated new mechanic gap in these fields. This does not certify the entire detailed power rules or the book.

Exact remaining reference mapping: one-based row position in Companion action category -> Critters canonical entry key under /data/entries/<key>/profile/action (each target is rules/critters/power-entries-pN.yml). All 39 selected rows have original class coverage; the abbreviated index does not remove detailed conditions.

| Critters printed/PDF | Companion row : target entry |
|---|---|
| 7 | complex.critter[1]: accident; [3]: animal_control |
| 8 | free.critter[1]: cold_aura; [2]: corrosive_saliva; simple.critter[1]: concealment; complex.critter[6]: binding; [7]: blindness; [8]: compulsion; [9]: confusion |
| 9 | complex.critter[10]: desire_reflection; [11]: dispelling; [12]: empathy; [13]: engulf |
| 10 | free.critter[3]: fading; [4]: flame_aura; complex.critter[14]: essence_drain; [15]: fear; [16]: glamour |
| 11 | complex.critter[17]: guard; [19]: hypnotic_song; [20]: influence; [21]: innate_spell |
| 12 | free.critter[5]: magical_guard; simple.critter[2]: magic_sense; [3]: materialization; [4]: mimicry; complex.critter[22]: mist_form; [23]: movement |
| 13 | complex.critter[24]: noxious_breath; [25]: paralyzing_touch_howl; [26]: petrifying_gaze; [27]: possession; [28]: psychokinesis |
| 14 | free.critter[6]: shadow_cloak; complex.critter[29]: search; [30]: silence; [31]: sonic_projection; [32]: spraying; [35]: weather_control |

33 plain matches, six qualified/label-distinct matches: materialize/dematerialize both Exclusive Simple in detailed p12 prose; index Dispell vs source Dispelling is a label distinction, not an automatic alias acceptance; Engulf, permanent Essence Drain, Mist Form and Search retain Exclusive Complex. Critters p10 Temporary Essence Drain is a distinct Complex/Special variant already in canonical data; no collapse into permanent drain. Framework p7 exclusivity, physical/astral eligibility, sustaining and domain limits remain controlling. The 18 extra typed checks include animal-control capacity, Cold Aura reach and hit modifiers, Compulsion action count, Temporary Essence Drain variant profile, materialization Initiative, six Magic Sense numerical modifiers, Shadow Cloak modifiers and Spraying arc.

All eight original semantic and index commits are ancestors of the restored authentic HEAD. Actual Git historical path/blob and original index snapshot matched unchanged current exact registered entry (including gate status), then current live blob readbacks matched. This is registered evidence, NOT recovery of original baseline/plan/candidate/confirm/index journal artifacts:

| p | semantic commit | semantic blob | index commit | index blob |
|---|---|---|---|---|
| 7 | 345bd61e64d3b0e969f2fde67221542c95070f5c | ebc3a6abdb5db80498fd7fe7d8606f1e0e6d58c5 | fdd0fb358c01e03c61ef6cb84262a625f83d603c | 13022a04a804c09a996323fa8ddbfe6b27c85c7a |
| 8 | e1e870966618bf3a1d809a90e3b92cfc8e618f73 | 6810e9c702e330d98dd8afbcf4e1435e681450e8 | 613b53c1b87e42853f9f53c36d86bd246bf53265 | 7825de5a5d012635d5bc0d90ecc2e93f68d5ae9f |
| 9 | c95ec23f0103deb3911f6dd65314e7fc15a82b18 | 313c1bdf3c415c20be39d55552d4ba3121bb0b5e | 58aef7217793cc227ee87d3fef82cb2832916c0a | 9b7c1faa032dd145a03dfde65a71d817db49848b |
| 10 | 2ac9a621188223d050acbd28ff9830f709e12e9b | b68e11787ce203776339f7c9667870ca868e75cd | e970f882139f8235fd05b5b7909aa00ec49dd780 | 5cd100adfe0f9e54e4bec30482527fdba77223df |
| 11 | 5e4162619079da3df691027c0979639ad7ca9269 | 4b75a78ecee5ce1e184384172bb7cd71d96ea733 | 544bfad2b53b486e34795f974952d88bbd23bd65 | 3c03bd418e8d50d4e6535174cb73e5047d6b6f2b |
| 12 | 07e7831718164c94fcdb999f748899fc3ffd1d8a | 288493056c1408132f33ab11aa4a568853e35ca0 | e804375db41e67695e0f7a8e063d3620095f150a | e2978fd9b5e80367310ac55c630a720e3be57313 |
| 13 | 82edbacb65388255f6e65f384b6977f8cda87e7b | a3aa4f9c49bb859905ee24c6a6d9a9fb263c8b7a | 086ed091a540f56788177c788bdb06e993be3790 | f2b8c95396cc25f7d0178901bccf8a3ccc05789f |
| 14 | 3238add3ff99f08eba9e5c3540c2a13590ce3cdc | e0f351a2fc548361a12e770a2a0581d877c4fd25 | b6cf0c1f2b12937e4c7ea34b2666b11d16de75d0 | a2ead1c70e3608c6d330f258bde71b1c9200eda8 |

Actual bounded pinned-input triage TRIAGE_ONLY (39 fields, 8 paths; 40 equivalence, 1 independence, 1 inventory, 4 original_rule prerequisite diagnostics; overlapping, not missing mechanics). Actual validator at authentic restored HEAD returned BLOCKED: independent_review_required, no formal acceptance. Non-core equivalence and original independent editorial/custody inputs remain absent. Original full-book inventory outside p130 and other rows not substituted by zero-rule dispositions. Diagnostic hashes: review 7eb3bc3c2a823873c83e050e6cda8a539803e1f665f4b7ed41cd42c2e85d96da; bindings be1af4bd666149629510ef5edf51ae46b0000d37b974425d34396c26762dcc5b; evidence 44915d05182f79dfbb3ccf28f20846f9a5313fecb5c64f74f3e8276542eb584a. Row diagnostics SHA256 1980b69f4c24ffb2f7e3002d1a99ff648ea962f034bfc8efde968bb4c87b0289, attached diagnostic ZIP SHA256 99d3f43336b31fae34f3071886a330a2f700040f36738def6adf70d92de52a57.

Remaining 47 of 112 original other-source references are outside the two recent bounded source comparisons (including complex.critter[33] Storm, requiring separate fresh MitS original and current manifest). Prior 22 Simple/Complex core accepted-parent gaps remain, as do independent review of Free and alternate accepted parent candidates. Previously referred Fire Weapon discrepancy still present in live revised blob 87371b67cf6ac9e57ffd276d44713eaa3cdafcfd at inspected main; no protected correction authorized here. Historical Critters original journal search negatives reused until evidence changes. No new semantic correction, recovered original receipt, fully certified scope, formal source acceptance or global advancement. Next: group remaining 47 by actual publication and original page conditions, without equating Rigger 2/3 or VR2/Matrix merely by labels.


### 2026-11-27 — Companion Actions: bounded MitS mechanical reconciliation

Fresh Drive originals authenticated by actual preservation_method.py verify-source: source.srcomp SHA256 8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5, manifest blob 4c014f59d657cb872eef541f8a2693b26d8d2a6e; source.mits SHA256 d96829f0393ed61052d7d7b8ab9e355c37156788dd5594ff4bd1e30df6eed427, manifest blob 7d7ca0ffcd68c8212770b47119e744a9353de106. Both returned source_pdf_hash_verified. Original Companion printed 130/PDF131 and MitS printed 47–48,70–74,76,98–100/PDF48–49,71–75,77,99–101 visually reviewed for the seven targeted natural scopes. Source/target record and manifest blobs match live main observed e92aed385fedd521dd7cee5cc1fce32dbb44efa8. Actual history checkout 4454f82eea80b020ca9c278ed795ce68e14512de from successful workflow 45966958253 artifact 15183376250, ZIP SHA256 30dc1714747a74b914a640fd501affa1156cc3e1c6dc0ddd0178f1aea19f3675; original core receipt ancestry verified. Existing protected regression suites: 85 passed (29 preflight, 20 ingestion, 20 preservation, 16 recovery).

Eight original index rows located, 136 typed selected source/record field comparisons matched; seven bounded class matches, one scope ambiguity. These are NOT independent formal equivalence attestations or full target section closure. Preserve all original conditions.

| Companion row | MitS printed scope | Exact target field (relative to record data) | Mechanical disposition |
|---|---|---|---|
| free.magic[2] | 72–74 | centering /use/action | Free; same phase, before augmented magic, one benefit, eligible skill/astral and adept exceptions |
| free.magic[4] | 76 | masking /deliberate_masking/drop_action | Free; maintaining restriction stays |
| simple.magic[4] | 76 | masking /deliberate_masking/action | Exclusive Simple; grade ×2 dice, own Magic TN, 2:1 countering |
| simple.magic[7] | 48 | formula /inspiration/observation/action | Exclusive Simple; astral perception, Force TN, instant +2, one success |
| complex.magic[6] | 74 | cleansing /resolution/duration_action_type | Complex; two actions per level, temporary only, cause removed, grade cap, Drain |
| complex.magic[13] | 98 | heal /healing/summoner_action | Exclusive Complex; one service, Physical only, last-service exception |
| complex.magic[14] | 70–72 | anchoring /linking/test_action | Complex linking test within one Exclusive activity; unused dice, retry and separate Drain preserved |
| complex.critter[33] | 99–100 | storm /storm/action and /storm/strike/action | BLOCKED blanket equivalence: printed power profile Exclusive, separate strike Complex once per Combat Turn; canonical record already distinguishes both. No missing rule demonstrated. |

Each target exact current semantic blob matched its original registered commit and earliest observed exact manifest registration in authentic Git history. Historical gate/index evidence is registration evidence only; separate original transaction/custody artifacts not recovered in this review.

| Target path | Semantic commit | Blob | First matching index commit | Index manifest blob |
|---|---|---|---|---|
| options/magic/metamagic-centering.yml | 5e0aa49d23433a2b57cbb16d56ceb42cd215aae7 | 423b3946234a9e206e234ec772afff5206ca924d | 26359983ae79d4f40ab69cf0f9356f160124dbc6 | 1a64ec1be24d6ddfdde11907179bdc9861f0bd03 |
| options/magic/metamagic-masking.yml | d931ae250a8bb33ff0ab888a76ebd60e99003baa | 10f994bf9086a1f36879ef72647df6712d2fbca8 | cc1b8af1fd66a3e8d300995ea7e7889e81dc58b2 | c7780a792910ac9c473afabf4c9e6959acd92b57 |
| options/magic/metamagic-cleansing.yml | e05696620799ccf800e3f9c9341c0a17cca68fe1 | 0096021864e0d0f8eaffa3469cd7d47419c604f6 | 6e881a5c0fc3c7f285b077e4890dfc8d729ef5d3 | 031168ccdc1b2c2cfd5ed47d68d8ca2fb7a87f81 |
| options/magic/metamagic-anchoring.yml | ae4a9c6ffe45213495726aa340be527b812d2023 | 78ce6a47e0baedaf51ee88409c0a380854542f15 | 51ebaa1f171cfe574ae72101edeffb8c8a29d879 | dc1957a1a81d5428f700bc72d54e8e13f7da7a4b |
| rules/magic/mits-spell-formulas-original-p47-48.yml | 52f433badeb6f9ddaaf017f15e40a8041f37ed86 | cc977415b5388f9f1202197e23118aa046a2076e | e9c9e854632e5308515db3248df5cf638ebccf83 | 6fabd65b1a801e759c748c8b8528919fd25d091e |
| rules/magic/mits-spirit-service-original-p98.yml | 4e8182302a7f9ca53b0e7cea9ec56331e6388baf | d6b76a39697938c2453472178a8946bd5b2a1c03 | 18172bd298cbac5f4f357f88d023343ce7ede8cf | 605c3761d4d30bdeab6b7536ef0a7b503cc6a323 |
| rules/magic/mits-spirit-powers-original-p99-100.yml | 7d8af1022e094a3b0b3f595356bd3b78e190b845 | 7fecee3dc067d1781139eb21a246727c3d210b22 | 12e9547b6373968a192c1ecaee9c31bab15e55ae | e68b5c2ba74f989540db0d40b348e5bcf9320fda |

Actual pinned-input blocker_triage: TRIAGE_ONLY, 8 fields/7 paths, 14 diagnostics (9 equivalence, 1 independence, 1 inventory, 3 original-rule/unresolved items). Actual validator using fresh original Companion and authentic non-shallow Git: BLOCKED independent_review_required. Full page/field custody and accepted non-core target proof remain needed. No implied zero-rule pages. Diagnostic archive Companion_MitS_Action_Review_2026-11-27.zip SHA256 8ad4824bf00fe5bae351bd3d1abf98afdb71e684c39def694fb9fa8809601f62, contains source-derived expectations, actual field values, full commit/registration pins and machine outputs. No semantic corrections, newly recovered original receipts, formal book acceptances or global pages. Remaining other-source references outside these three bounded comparison batches: 39 of 112; Storm separately requires scope adjudication. Continue with remaining references; do not repeat these comparisons absent changed evidence.


### 2026-11-27 — Companion Actions: remaining core-reference conditions and acceptance parents

Live observed main 9fb22e7f6b532c76864c10afd6d8bf2fc105bc13. Authentic complete Git bundle checkout 4454f82eea80b020ca9c278ed795ce68e14512de (artifact 15183376250, ZIP SHA256 30dc1714747a74b914a640fd501affa1156cc3e1c6dc0ddd0178f1aea19f3675, bundle SHA256 9c90961adc6d26aaf5f02087e16906ff57440c175da5905504fe4ddfc460ab6d). Bundle verification, non-shallow checkout and original acceptance commit ancestry verified. Catalog, both handoffs, editorial playbook, protected tools/tests, expanded validator/triage/equivalence dependencies, exact current source manifests and all nine target blobs matched current live Contents pins. Actual 29 preflight, 20 ingestion, 20 preservation and 16 recovery tests passed (recovery import environment corrected with PYTHONPATH; no code modification). Fresh cataloged Drive originals both returned actual preservation_method.py verify-source status source_pdf_hash_verified: FASA7905a 8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5, manifest 4c014f59d657cb872eef541f8a2693b26d8d2a6e; FASA7001 7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914, manifest b0ebffa4985ab544e64857b99e98b17d69ee3184. Original Companion p130/PDF131 and eight bounded original core headings directly visually examined (not full-page/book acceptance). Nine index rows and 89 selected typed source-value comparisons, all 89 matched. Text condition comparison separately exposed two genuine canonical qualification omissions and one broader index scope question.

| Companion row | Core printed/PDF | Mechanical result | Historical accepted parent |
|---|---|---|---|
| free.magic[6] | 173/174 | End manifestation Free; explicit any-time statement in source; check general timing before correction; not return from projection | Missing /data/manifestation |
| simple.magic[6] | 173/174 | Manifestation Simple; visible/audible/intangible, machines cannot perceive | Missing /data/manifestation |
| free.magic[7] | 170/171 | Missile Parry Free, cost 1, slow projectiles, Reaction plus Combat Pool vs 10 minus range TN; must beat attacker, ties attacker | /data/powers |
| simple.magic[5] | 196/205 | Control Thoughts Simple, original Willpower/half-Willpower threshold and per-command resistance preserved; index says control manipulations broadly, no generalized action timing inferred | /data/spells (scope still blocked) |
| complex.magic[11] | 184/193 | Dispelling Complex; visible target of sustained spell, same plane; Force TN, subtract successes, threshold, separate Drain retained; printed Petrify example matched | /data/eligibility |
| complex.magic[20] | 164/165 | Dog only, Willpower TN6 to change declared course, Complex | /data/totems |
| complex.magic[21] | 176/177 | BLOCKED mechanical condition: suppression actor qualification omitted | Missing /data/astral_objects |
| free.decking[5] | 209/218 | BLOCKED mechanical condition: two/three success disclosures only for IC | /data/noticing_icons (condition mismatch) |
| complex.rigging[1] | 141–142/142–143 | Accelerating/braking Complex in vehicle combat, Handling TN, signed table, max speed/crash thresholds and pursuit example retained; separate worked-test record matches original | /data/original_mechanics |

**Authorized coordinator/core-owner correction handoff (not permission to reopen accepted core automatically):**
1. rules/magic/sr3-core-astral-damage-objects-evasion-p176.yml, /data/astral_objects/suppression. Printed p176/PDF177 specifies the character who reduced the object's Force to zero without destroying it as the one who can maintain suppression. Current field allows an unspecified character to spend the Complex Action. Preserve repeated per-Combat-Turn action, full untouched turn recovery, and astral/dual passage conditions. Actor eligibility changes gameplay.
2. rules/matrix/sr3-core-system-tests-action-security-tally-p209-210.yml, /data/noticing_icons/successes_two and /data/noticing_icons/successes_three_or_more. Printed p209/PDF218 parenthetical explicitly limits type and rating disclosures at two and three successes to IC; current fields state unconditional icon type/rating. Preserve free Sensor Test/no utilities, decker versus program TN and one-success detection. Original identification may still require Analyze Icon. Do not infer unconditional disclosure.
3. Control Manipulations index label scope remains unresolved, not a proven absent procedure. Preserve individual spell-specific timing. Manifestation's explicit any-time qualification should be compared to existing general Free Action timing before adjudication.

Nine exact semantic path/blob registrations in current and original accepted manifest snapshots verified against actual Git semantic commits, with historical ancestry; not newly recovered original local journals:

| Record filename (unique within source) | Semantic commit | Blob |
|---|---|---|
| sr3-core-astral-projection-attributes-movement-p172-173.yml | 574b60401e774eb5cb99eb66daa10b4bb398ed18 | 974e21185f2403741453da313896460641e0fb81 |
| sr3-core-adept-powers-combat-survival-p170-171.yml | e799748918f0d8aa3e7afd60d7300c2609ea5629 | cca921ca755ee9020a13b1f1fac2a16138be8199 |
| sr3-core-control-manipulation-numeric-p196.yml | 8758e1123046e2e36079fb4db46bda3be99eae87 | 50b1465ac2b06fa7ab845b2661a3cbf0a65854d4 |
| sr3-core-dispelling-exact-p184.yml | 5fd11e47cf86ab06bf40fcb6316cc90f54dcf25f | b23cd0b936ca90b65592a3ecf98b97418e413c88 |
| sr3-core-shamanic-totem-options-p163-166.yml | cd96910dc727c5461c0049f1fe3a12849e8adfe9 | 2bfccea91ca56aea36a69e5e13dbc004fe50b1be |
| sr3-core-astral-damage-objects-evasion-p176.yml | 78f9fc4298849471ed3597717c89243aae5b30e6 | b392eceebb80631ba9f509e028e3f591a60a561b |
| sr3-core-system-tests-action-security-tally-p209-210.yml | 607fa4b5565e3fe99038ee2d15d43cda8fd213f4 | f64d01b115580a74bd77faafab06973d939223cd |
| sr3-core-acceleration-braking-tests-p141-142.yml | 9d498d3447ce6002c1cd1d4393724e5d07d34ba0 | 7c87ef394b8eccc6b443eb74f2001bf324f032b4 |
| sr3-core-vehicle-actions-worked-tests-p142-144.yml | 42985b7247fa85c90a367d8bfceb0ae7ca63e33a | 313ce84249484764664518a0f44ecd5e096e7d85 |

Historical accepted receipt commit 6baeb5dffd92dbdcbe50aa451d637e8ae9702316, receipt blob d11888c9f20b5603f874f4e976dff3e23c8cde98, historical index manifest blob a79b28a3970668982ef44a5318642ed55848839a, closure queue blob 366ee748f51dbf2b699a26edbc1215352743191d. Six row pointers have named historical accepted parents, three do not. Parent existence is not independent source equivalence proof. Four plain and two qualified action matches; two mechanical-condition blocks; one index-scope block. No new accepted source or formal row equivalence.

Actual pinned-input triage on nine rows/eight paths returned TRIAGE_ONLY (10 equivalence, 1 independence, 1 inventory, 3 original_rule diagnostics; overlapping). Actual validator against fresh Companion and full historical checkout returned BLOCKED independent_review_required. Current local review is not independently authenticated, and full-book page evidence remains absent. Diagnostic archive Companion_Residual_Core_Action_Review_2026-11-27.zip SHA256 977aef931d935a2d10451c2635d497887ca9db6e083e696e981bbb4830e2bbaf; diagnostics.json SHA256 7c86444c4a8a09d06cf8d5ac7bbd2b5f4e91fc36768c703449941fcf92fc3d4f, review 3e8a66194bccc52d8af6954d6fd02bb029f554f6cf77fbfbf29ae22d9dd695a1, bindings c6b18f2728c2e30ba5a624dbd7bcb342beb64a4ee353c4a4a2e93b725106020a, evidence 44915d05182f79dfbb3ccf28f20846f9a5313fecb5c64f74f3e8276542eb584a.

30 of the original 112 other-source/shared-reference rows remain outside the four bounded comparison batches, not 30 proven missing mechanics. Previously reported Fire Weapon mismatch is distinct. Next prioritize residual core vehicle and Matrix references, then genuine Rigger 2/VR2 or later-source lineage with original editions verified separately. Two newly demonstrated mechanical condition gaps referred, no semantic changes, newly recovered original receipts, source acceptance, or global page advancement. Protected core and worker configurations untouched.


## 2026-11-27 — bounded Companion residual vehicle, focus and Matrix review

Live main observed 48ee8fd0087fa0014f786635457646f90cfb6b88. Authentic complete historical bundle (artifact 15177752546, ZIP SHA256 8e71ac6fa3a3e67546e2c1febf8a1d7f2cf5c70df1b3a81bcc7fd88be65e1eda) checked out ded2a66c23ca848dccc767789521be0b4133f422, with original core receipt ancestry 6baeb5dffd92dbdcbe50aa451d637e8ae9702316. This is not a checkout of the newer live HEAD: selected record and source manifest blobs and gate/tool dependencies were compared to live and matched. Fresh cataloged original Companion and SR3 PDFs both actually passed preservation_method.py verify-source (source_pdf_hash_verified), SHA256 respectively 8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5 and 7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914. Live manifest blobs 4c014f59d657cb872eef541f8a2693b26d8d2a6e and b0ebffa4985ab544e64857b99e98b17d69ee3184. Protected tests: 85 passed.

Ten further p130/PDF131 shared rows reviewed in six bounded natural scopes, 99/99 selected typed comparisons (separate semantic discrepancies below), nine exact historical semantic registrations, seven accepted-parent candidates. Four bounded matches, three qualified index references, three blocked on mechanical conditions. These are not ten formally accepted rows. Twenty of the previously outstanding shared references remain outside comparison; no assertion about their mechanical completeness.

Coordinator/core owner correction handoff (no protected writes):
- Ramming p143/PDF144, rules/vehicles/sr3-core-ramming-test-modifiers-p143-144.yml /data/original_mechanics/collision, semantic 4d47b5e731ec526349ad503cfc3157dfaedb8df9 blob f2a685742bb910a98a898c5d8130959305978243: Crash Test applies if either vehicle takes damage, not only the rammer. General p147 trigger already preserves the broader mechanic; inconsistent local field. Legacy rules/vehicles/ramming.yml /resolution/summary blob b9c3d6182484243986f6f401ccc7ee2b1324de53 calls it opposed Driving; the original uses one Driving Test against Handling. No exact accepted registration asserted for that generic summary.
- Matrix p225/PDF234, rules/matrix/sr3-core-cybercombat-hit-damage-maneuvers-p224-227.yml /data/maneuvers/parry_attack: a successful Evasion by either icon cancels the Parry bonus; current record restricts it to the opposing icon.
- Same Matrix record, p224/PDF233 /data/actions/terminate_download_upload: original permits suspension as well as termination any time, absent explicit suspension in the inspected core Matrix records. Both Matrix fields share semantic 1667b9da218eaa93ab229279669d1dbb73ed9fe2 blob a3bf9e6e2e1c849983ede4177ad4c525db080101.
- Preserve source's p142/p143 pursuit equality-boundary discrepancy (at least twice vs strictly more than twice distance), not silently resolve. Cruiser #1 positioning worked example absent from inspected worked-example record 42985b7247fa85c90a367d8bfceb0ae7ca63e33a blob 313ce84249484764664518a0f44ecd5e096e7d85; distinct example coverage gap, not a demonstrated missing general mechanic.
- Preserve Exclusive Complex restriction of expendable spell focus p190/PDF199 and conditional Free/Complex Jack Out boundary with black IC, not blanket index-label equivalence.

Actual pinned-input blocker_triage: TRIAGE_ONLY, 10 equivalence, 1 independence, 1 inventory and 3 original-rule blockers. Actual validator on fresh Companion PDF against verified historical checkout: BLOCKED independent_review_required, exit 1. Local diagnostic pins are not independent reviewer/custodian authentication. Full-book original inventory, receipt and cross-source equivalence attestations remain outstanding. No formal row/book acceptance, no newly recovered original receipt, no semantic/index writes, no global page advancement.

Diagnostic archive Companion_Residual_Actions_Vehicle_Matrix_Review_2026-11-27.zip SHA256 aee3d4ff548a18add6f949de26969e63bdd128f89278366140a13a0483654763; diagnostics.json af43f522ba9d62685d4ad182500a8a8377b8b8d26eb3a7f7db974dc6d4346bf7, triage.json 996860b1dbff6ef1757188b532f31e75c9ce4cf46c9f1e59a9491dba62ce493d, verdict.json d1b3eee5f462d0a4627e37e619421c74b490f3f66bc0f0a1b72e78532ee311d3. Next cursor: remaining twenty shared action references, first original-pinned vehicle/Matrix/equipment qualifiers, then actual legacy-source edition lineage; separately adjudicate the named core condition mismatches.


## 2026-11-27 — bounded Companion Matrix and equipment action comparison

Live main observed dc1059c567b66d80e450376a119ded33603f6b64. Full authentic historical checkout ded2a66c23ca848dccc767789521be0b4133f422 (bundle SHA256 0659484ebfe5b2a833e27485a0b36b0fc10ab98a84bea580d23634f106ba1913; original acceptance receipt ancestry 6baeb5dffd92dbdcbe50aa451d637e8ae9702316). Relevant live manifest and record blobs, catalog, both handoffs, editorial playbook and acceptance/gate runtime files matched that snapshot; not a claim of full live HEAD checkout. Actual preservation_method.py verify-source returned source_pdf_hash_verified for all three freshly acquired catalog originals: FASA7905a 8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5 (manifest 4c014f59d657cb872eef541f8a2693b26d8d2a6e); FASA7001 7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914 (manifest b0ebffa4985ab544e64857b99e98b17d69ee3184); FASA7909 b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe (manifest b1cf2028c102d24b17bcf5a64c8b6f640507363e). 85 protected regression tests passed.

Eight of the prior twenty unreviewed shared rows examined on original Companion p130/PDF131, core pp156–157/PDF157–158, p217/PDF226, p220/PDF229, p280/PDF289 and p282/PDF291, Matrix p40/PDF41, pp98,100–101/PDF99,101–102 and p162/PDF163. All 76 selected typed field comparisons matched; ten exact current/historical source index entries and semantic blob/commit ancestry checked. Legacy Matrix operation catalog has matching header values but no verified individual registration located in the current manifest. These are bounded coverage comparisons, not formal row acceptance or original journal recovery.

- free.rigging[2]: Free drone weapon-system class, one armed system per drone and one Free switch; broader rigged-system scope remains qualified, not inferred identical.
- simple.combat[7]: both original equipment setup classes and distinct posture/recoil conditions match; bipod and tripod separate accepted parents /data/accessory_effects and /data/procedures.
- simple.decking[10], complex.decking[5,6,7,17]: later Matrix Scan Icon, Decoy, Disinfect, Dump Log and Redirect Datatrail header and bounded procedural comparisons. The original Scan Icon p101 explicitly qualifies frame/agent utility information as loaded in active memory; inspected /data/operations/scan_icon/per_success shortens that condition. Preserve explicit qualifier; no assumption that later Matrix automatically supersedes every VR2 procedure. Dump Log p98 explicitly lists three baseline log identifier fields plus conditional additional records; /data/operations/dump_log/log_scope references p40, which instead gives discretionary breadth and more extensive log fields. Preserve both original assertions and request source-owner adjudication; do not overwrite discretionary p40 rule or claim all log fields absent. Two source-condition documentation concerns, no new confirmed missing global procedure.
- complex.decking[12]: seven distinct Locate operations (five core, two later Matrix) are Complex. Preserve original thresholds, utilities, eligibility, and Analyze/Browse contradiction; Matrix p162 lists Browse for Locate Slave. Accepted core /data/operation_definitions covers five, not the two later supplement operations.

Actual blocker_triage: TRIAGE_ONLY (8 equivalence, 1 independence, 1 inventory, 3 original_rule); actual validator BLOCKED independent_review_required, exit 1. Missing independent full-book inventory/custody and reviewed source lineage/target proofs, not a new Git-history blocker. Historical registration matches do not recover original local receipts. Full exact paths, field values, semantic and index commits, blobs and source review limits in Companion_Matrix_Equipment_Action_Review_2026-11-27.zip SHA256 af9d470617255618c88b06e88908ed4706bb42eef8d37afe50845247e12f709c; diagnostics.json 9d95272fc1efeaeeac3ee8296e7229bb113c739df70f7c1ce42bcd5cbad7ee7d; triage.json 3ac96fd7ee33e612cd6028875225f378738613e1fd7e531d2cfe2b6e612ac461; verdict.json d1b3eee5f462d0a4627e37e619421c74b490f3f66bc0f0a1b72e78532ee311d3.

Twelve remaining of original 112 shared references outside bounded comparison: free.rigging[4], complex.combat[1,3], complex.magic[4], complex.rigging[2,4,5,7,16,17,18,19]. Rigger 3 original manifest has no root source SHA in inspected historical snapshot; Revised PDF was acquired but its live manifest changed (08a4416828d5d133eee2135cfaf52258b99f7aec vs historical 0776904a283106e8bb68becba9075c79bdf0dca8), so no source verification or original comparison of that edition claimed. Obtain current exact manifest bytes for Revised or authenticated original Rigger 2 lineage where available; then compare remaining CCSS/EW, missile lock and indirect fire qualifications. No semantic corrections, original receipt recoveries, formal book acceptance or global page advancement. No protected writes.

### Companion p130 final bounded shared-action comparison (2026-11-27)

Read-only coordinator handoff. Live main observed 476e3998e75795efdbef6cc4ed76773ebb95c578; authenticated full-history checkout ded2a66c23ca848dccc767789521be0b4133f422 (not a claim of live HEAD checkout). Exact target blobs compared to live. Five fresh cataloged PDFs passed actual preservation_method.py verify-source: FASA7905a 8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5; FASA7001 7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914; FASA7907 d96829f0393ed61052d7d7b8ab9e355c37156788dd5594ff4bd1e30df6eed427; FASA7908 7b979ed358aaa23bbe68eb95a0887b1315f302bedd6bcc04df00d8d68fbd84a4; FanPro10662 88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909. Current Revised manifest 7da4fbd19a572d7f64793a625675f96e3c79a713, MitS 3adb7f985743dc19c252c22e2a4952f8b4934b00 and CannonCompanion b44e8dd4af4dd76c66171a8d22153c1643d07ae8 restored byte-exactly.

Twelve remaining index rows received bounded original-page comparisons. This brings the 112 shared-reference comparison queue to zero unexamined rows, NOT zero unresolved rows. Eleven labels have matching action-class components, one (grapple/entanglement) partial. Eight later Revised rigging references still lack authenticated original Rigger 2 lineage. No blanket edition supersession or independent attestation inferred.

| Source printed/PDF | Bounded finding | Outstanding scope |
|---|---|---|
| Core 276/285 | Entanglement escape Complex | Generic grapple component not established |
| Core 186/195; MitS 109–110/110–111 | Elemental Exclusive Complex; ally recall Complex | Separate prerequisites, no blanket equivalence |
| CC 99–101/100–102 | Spotter acquisition Complex; action qualifiers present | Independent predecessor/target equivalence |
| R3 Revised 37/39, 40/42, 48/50, 50/52, 83/85, 84/86 | Eight rigging/CCSS references compared | Original R2 lineage, exact accepted target evidence |

Source-owner questions, not proven global omissions: R3 Revised p37 continuing mutual communications range and immediate target awareness are not explicit in rules/rigging/miji.yml /resolution/steps; linked infiltration procedure states range at entry. R3 Revised p48 room-control pool and rigger bonus qualification not explicit in rules/security/ccss-actions.yml /complex_actions/0. Verify other canonical fields before any correction. Do not modify legacy source.r3 records using Revised text without edition adjudication.

Eight exact typed comparisons matched, alongside separate bounded prose review. Four live registrations matched historical semantic blobs: bullwhip 2607a49cf3cb301d74ba7d5b7d8266b6bb4f055f / 62268acb26719043fca7c9a8733c22ea75bc9e05; elemental 17d2cfe033b11b0398b004cafb80ef96cc0b39f3 / f0c3544e64a4a481865ce5e32dbbc49ac152d28d; ally c2ad9416adf8266ba1fd1d2648bd4e9fcd0ebbe2 / 5b8de1646065beb1cee942ca5b51e8a3cdef4e94; spotting d9f946ef3da9206177d2c181cfe269ce2ff861b4 / 84e2b60dbc3b4c23010a3c72e83a49336e0f74eb. Original core acceptance receipt commit 6baeb5dffd92dbdcbe50aa451d637e8ae9702316 queue blob 366ee748f51dbf2b699a26edbc1215352743191d binds ordinary_bullwhip_p276 and call_and_command_sequence; descendants do not automatically discharge composite Companion labels. No new original historical transaction receipts recovered.

Actual preflight 29 + protected regression 56 passed. Pinned blocker_triage TRIAGE_ONLY: 9 binding, 3 equivalence, 1 independence, 1 inventory, 5 original-rule entries. Actual validator exit 1 BLOCKED independent_review_required. The 9 binding diagnostics include legacy pointer shapes; they do not establish absent mechanics. Full-book independently authenticated review/custodian and accepted target proof still missing. Machine-readable diagnostic archive Companion_Final_Bounded_Action_Review_2026-11-27.zip SHA256 c789d63a97d8f94bdfde922bcde3cba0ba3e027412a971664280265847da794c. No semantic/index write, no formal book acceptance, zero global page advancement. Next: independent original predecessor/equivalence adjudication and full-book acceptance evidence; avoid repeating unchanged p130 comparisons.

### 2026-11-27 — exact single-path commit verification hardening

A reproduced verifier defect: the former Git.changed path-filtered diff could not detect unrelated files in the same commit. It accepted a combined semantic/index commit, an unrelated extra record, and a rename. The independent validator now examines the entire single-parent tree delta with NUL-delimited path names and rename detection disabled. Only the requested path may differ; multi-path, rename and unchanged-path cases fail closed. This applies to source-local semantic/index commits, split archive bindings and the accepted core receipt reference. No protected gate or pre-existing test changed.

Exact ordinary Contents writes and fresh commit/live byte equality:
- validator.py commit 7c7efed4026c13449f5f7e4a44184b8a1e515a97, blob 2e46735e148ceeb81515497bf058b45102d7b033.
- New test_exact_commit.py commit 2c5a419d616b1d9530b45e77d240a72eef103f24, blob 478c50541a3b23b54620626a72d527c9f2c0b723.

Five new real-local-Git synthetic regression tests: four pre-fix failing assertions across three adversarial tests, all five tests passed after correction. Full expanded suite 106 passed using PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tools/expanded_acceptance python -m unittest discover -s tools/expanded_acceptance -v. Without that environment setting the existing integration fixture stages generated Python cache files via git add ., and correctly fails strict single-path verification; no weakening of the check or alteration of old tests. Protected preflight 29, gate/preservation 40, recovery 16 passed. The historical checkout was ded2a66c23ca848dccc767789521be0b4133f422, archive 15177752546 SHA256 8e71ac6fa3a3e67546e2c1febf8a1d7f2cf5c70df1b3a81bcc7fd88be65e1eda, with core receipt commit ancestry verified. Initial live main was 7ae79d05d9857aee1cf19722ea79dfd612b4f680; relevant validator, dependencies, catalog and handoff blobs matched local historical inputs before edits, not a claim of full live checkout.

Production historical topology diagnostic: actual original SOTA2064 recovery archive SHA256 98da0c21e9b1d1c2ed89d0f7654f9ad314a789b9856beba6efeec673bcafb2ac, five embedded archive hashes matched. All eight original semantic/index commit pairs passed new complete-tree single-path and ancestry checks, exact historical semantic bytes and index blob pins; all eight registered entries were newly inserted relative to the actual index parent (zero previous matching entries). All eight actual prepare and confirm replays matched original retained receipts. Core acceptance receipt also passed new exact-path check. This is a targeted historical recheck, not new recovery, current correction acceptance, or original PDF review. Six original index receipt files previously recovered; media van and police drone still lack original local index receipts. Historical local indexed-manifest artifacts and independent editorial chronology are not invented. Machine-readable exact commit/blob diagnostics: SOTA2064_Exact_Commit_Diagnostic_2026-11-27.json SHA256 b1066f0500435a35f69e99999a19b1b713f410530058469b78ad2ea7cf80cee2.

Next: generalize registration-transition checking in the validator (this run checked actual eight parent snapshots, not a generalized gate), retaining support only for explicit verified index schemas. Companion's remaining adjudication and independent evidence obligations remain outstanding. No new source selected for extraction, source SHA verification or book verdict claimed; no semantic/index writes, new receipts, formal book acceptance or global page advancement.


### 2026-11-27 — actual index-registration transition proof

The production CLI now invokes index_transition.py after structural assess() and before final PASS. This is required for both inline source-local and split_archive/v1 layouts; assess() alone is not a full production CLI verdict. The original index commit must be a single-path, single-parent manifest change, with the semantic commit in its parent ancestry and the exact semantic blob present in Git. The supported registration schemas are explicit id/path/commit/blob and record_id/record_path/current_commit/current_blob, including nested lists and correction keys. The target verified tuple must occur exactly once in the index snapshot and must not already have been verified anywhere in the parent snapshot. Moving a pointer, switching aliases, duplicating an entry or changing only unrelated manifest metadata cannot provide new indexing evidence. Conflicting aliases fail closed. These checks establish Git history, not original local receipt custody, original editorial chronology or formal acceptance.

Exact Contents writes with fresh commit/live byte equality:
- index_transition.py: commit 44210b241ca6b7b58c36a8a961d8dbd2c81181d2, blob ea37102db7c46b8659a5f74021dafe58df19c027.
- test_index_transition.py: commit 1e6c8e458dd8667f4f537f44092c353247ce87f9, blob 5230e145237e6e10951e32ca8a2a1a0bfebed33d.
- validator.py: commit 4e27528d6cd5bd136b480c6086bdf0d67545eebe, blob 69ce7f996619e5398cb78b748e573b2204becce2.

Eight new real-local-Git synthetic transition tests and one existing CLI integration test passed. Another 83 selected expanded regression cases passed; the combined discovery run timed out and is not reported as a complete suite pass. Protected preflight 29, gate/preservation 40, recovery 16 passed. Initial live main e9d5a1b1f42033a56a711582b2b12c4e0bd73eb2; selected dependencies and gate blobs matched authenticated full historical checkout ded2a66c23ca848dccc767789521be0b4133f422 and the previous validator change was restored byte-exactly before testing. This is not a claim of a full current HEAD checkout.

Actual new verifier executed against the eight historical SOTA2064 registrations in original Git history. All eight passed, with zero prior matching record registrations in each index parent. Exact path, semantic/index commit/blob and parent details in SOTA2064_Registration_Transition_Diagnostic_2026-11-27.json SHA256 faaad882571563f8e70af859d00916083721a0de15532e80c689979f4f84af2c. The earlier archived receipt diagnostic is input for commit identification only; historical bytes and transitions were read again from actual Git objects. No new original journals recovered, no source PDF selected or verified this run, no semantic/index mutations, no book certification and zero global page advancement. Next: original index receipt/snapshot binding for inline layout and source/edition-specific accepted evidence, while preserving the independent Companion adjudication requirements.


### 2026-11-27 — new Rigger Revised correction evidence for Companion p130 handoff

Read-only reconciliation, not a new source extraction. Observed main 5470d6f40f5def1943896f8fb972b6aefb734cf8. Companion manifest remains 4c014f59d657cb872eef541f8a2693b26d8d2a6e; Rigger3Revised manifest 22521966493082f0e47df730ed6299886f0f1857. Three previously executed source-owner corrections now supply retained prewrite and confirmed/index archives in the existing recovery folder. Actual GitHub exact-path historical/current semantic readbacks and historical index blobs match the retained archive bytes; each GitHub commit response lists only its intended record or manifest path. All three original prewrite baseline/candidate/plan/review members match their confirmed archive copies; actual current protected prepare and confirm rechecks match original retained receipts. Original indexed-manifest bytes match their historical blobs and all three registrations remain identical in the live manifest. This does not establish full ancestry or independent custody/chronology.

| Scope and source printed/PDF | Semantic commit / blob | Index commit / blob; live pointer |
|---|---|---|
| MIJI qualifications p37/PDF39 | 00597e8d4c3df7f3aeb64a7436fc793670b6c82f / 983372deb3eb18aca252b9c20ef2ac0ab4a8562a | c52c1ca4058afed8cea35fe2c1a4b7ea754ea268 / dc3b24e8a504ebd4e620274bd324b7ab2720a240; /verified_semantic_records/112 |
| CCSS action qualifications p48/PDF50 | cb2732c25a68e6c17a3e42d318eb264b7da78343 / a6fde73072274ac2a41e644f295b548d9d515a80 | c2f045b4bd4e4f934245014788675ce35298f65d / e8d5ab33161672f32c8111bfbdd4b28021f7d1bc; /verified_semantic_records/111 |
| CCSS perception area p48/PDF50 | 2d5bc36a9b9428c99ae74417404d7405659b6f63 / 50d882834520e6c5242cca0e9735e7a0e224970e | 98304ff4eab26ae5f4d6fff14a23782cb8f21778 / 22521966493082f0e47df730ed6299886f0f1857; /verified_semantic_records/113 |

MIJI previously raised mutual range and target awareness: revised source-local record now contains /data/test_qualifications/mutual_communications_range_required_at_miji and /data/result_qualifications/target_rigger_awareness. Preserve its test-time scope; do not infer loss-of-range timing. CCSS previously raised room-control pool scope: /data/complex_action_qualifications/fire_weapon_system/combat_pool_requires_direct_control_of_drone_or_room is now present, and the linked existing subsystem (live blob 856a6673b26f58fa175a02a9325ff4a87dd36607) separately preserves initiative bonuses and applicable pool restoration. The new perception record preserves strict room/corridor limits and tactile awareness; no legacy edition equivalence inferred. These are newly observed source-owner corrections, not semantic writes by the acceptance worker. The eight Rigger 2 lineage references, original generic grapple component and independent book acceptance remain outstanding. Cannon Companion p85–86 subduing record is present (live blob 6ce7a743fc2e659daf37121b6ee2cf1a303aefc0), but its explicit unresolved success/net-success precedence does not settle generic grapple equivalence.

Three original index receipts and original local manifest snapshots located in six retained prewrite/confirmed archives; full exact archive and member SHA256 pins in Companion_Rigger_Correction_Evidence_2026-11-27.json (SHA256 e10eef168565c56b0e34325672004ad2a974f7431146129a034c0d0fb174dbfa). FanPro10662 stored source SHA256 88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909; no fresh original PDF verification claimed for this archival recheck. Protected current preflight 29, gate/preservation 40, recovery 16 tests passed. No new semantic corrections, no formal book acceptance, zero global page advancement.

Concrete next validator issue: live Rigger3Revised manifest edition is exactly "Shadowrun Third Edition", while validator.py currently restricts review.source.edition to SR2/SR3 and compares it literally to manifest.edition. Add explicit approved source-edition identity mapping, not inferred substring matching or a waiver of record scope/lineage. The original index receipt/snapshot requirement for inline layout also remains open; support exact observed receipt schemas, including Rigger's commit_sha/blob_sha/manifest_path/readback_exact shape, with byte-exact archived snapshot and historical Git comparison. Never manufacture a missing original snapshot from Git and call it locally recovered.


### 2026-11-27 — source-specific Rigger 3 Revised edition identity

The concrete FanPro10662 false-negative is corrected without changing original source/canonical bytes. The independently reviewed inventory still uses canonical `SR3` (or `SR2` for actual SR2 books); only the exact source identity tuple (source.fanpro-10662, FanPro10662, FanPro, sources/manifests/Rigger3Revised.yml) permits the observed literal manifest label `Shadowrun Third Edition` as SR3. Other sources still require literal canonical edition equality. No substring match, case folding, legacy conversion, or source-precedence waiver. Both inline validator and split-archive current/historical manifest checks use this identity function; the exact Rigger Revised record scope is also required, and any present nested publication identity must not conflict. A matching scope does not establish authentic original field review, historical receipt custody, or Rigger 2 equivalence.

Exact committed and live byte readbacks matched locally tested Git blobs:
- source_edition.py: commit ce637b1256622872051459414072ee545eeb180f, blob 54f3738da50b9cf7a0c9a055058869f97106c379.
- test_source_edition.py: commit 239809a2691ecf28864a780b077f46e60aba0faf, blob 9df3d63027ac9d7b6f91f5a64454fa24c93dae61.
- validator.py: commit 3fa3c85bd5e2b1170b7f3de8ab257837d32f5547, blob 7ccbe5b5c5ab7a66e0174a74a56e46fdc2755e74.
- receipt_binding.py: commit d85bd651c0e45647b5bef9abcf4c51a0cd9a3, blob b844bdd4b7e3ce5004ff95d1ba159d1bed271e2e.

Nine new synthetic tests plus the existing validator/receipt binding suites passed (37 total). Protected preflight 29, gate/preservation 40, recovery 16 passed. Full expanded suite not run this turn. Local authenticated historical bundle SHA256 0659484ebfe5b2a833e27485a0b36b0fc10ab98a84bea580d23634f106ba1913, checkout ded2a66c23ca848dccc767789521be0b4133f422; core accepted receipt ancestry checked. Live protected scripts, handoffs, catalog, editorial playbook and predecessor tool blobs matched exact historical bytes or reconstructed exact current validator blob. Actual historical manifest blob 0776904a283106e8bb68becba9075c79bdf0dca8 and p49 vigilance record blob 1570c2bf6f48afe1af1eacdc5c462f2f530341ec passed the new identity predicates. Live manifest 22521966493082f0e47df730ed6299886f0f1857 has the same observed edition label; the three latest correction records' scope labels match the mapped source. This is a bounded identity diagnostic, not fresh PDF validation or book acceptance.

Next: original inline index receipt/snapshot binding (with exact observed schema and retained original bytes), independently attested field/edition lineage and unresolved grapple; general record-scope checking for other source identities remains an independent task. No semantic writes, fresh source selection, original journal recovery, formal source acceptance, or global page advancement.


### 2026-11-27 — original inline index artifact binding

The inline source-local production CLI now requires both `historical_index_receipt_artifact` and `historical_index_snapshot_artifact` in each transaction, in addition to the actual Git registration-transition proof. Each is an independently pinned original artifact object with `bytes_base64`, `sha256`, and nonempty `original_locator`. The snapshot must equal the historical Git manifest bytes, not a newly exported replacement presented as an original. The receipt must bind the exact manifest path, index commit, and snapshot blob, with a literal true original exact-readback marker. Explicit receipt parent blob pins are checked against the actual index parent; the supported split-style receipt's registration key is checked against the exact pointer. Unknown or mixed schemas, conflicting aliases, duplicate JSON keys and missing original bytes fail closed. The split_archive/v1 path retains its existing separate original artifact checks. Structural assess() alone remains insufficient. Coordinator custody/independence and full original review remain mandatory.

Exact committed and live bytes:
- inline_index_receipt.py: commit 4126f968a1f760437a93c1bf91934870492aa0d7, blob 79a21d6307d65001abefa48eed63ed78391a6f35.
- test_inline_index_receipt.py: commit 4931e34bf7f3eb50a53a87f88dc00884466532c7, blob 68eb8efc9fd1564696d6f0d501af78d414a7af6e.
- validator.py integration: commit 289249940d4e424b71141f364fb306e921d28724, blob 24cbf4218164c410a2cb2ee0b0b539d3f53977ba.

Eleven new local synthetic unit tests passed for the exact verifier bytes, including missing artifacts, altered snapshot, identity and readback mismatch, conflicting aliases, wrong parent, duplicate JSON, wrong pointer, bad digest and absent transition. Protected current preflight 29, gate/preservation 40, recovery 16 passed after all eight runtime-kit blob pins matched observed main 3c510ca60a4689f01fee9f3b95a57b7dd11c535c. The complete expanded suite and production CLI integration were not executed in this run; older inline CLI positive fixtures without the two new original artifacts now require fixture updates, not a production bypass. Existing tests were not modified.

Real bounded diagnostic: reacquired three original Rigger10662 confirmed archives for MIJI and CCSS action/perception. All three original index receipt and archived manifest byte pairs passed verify_bytes against independently fetched historical Git blob pins (index commits c52c1ca4058afed8cea35fe2c1a4b7ea754ea268, c2f045b4bd4e4f934245014788675ce35298f65d, 98304ff4eab26ae5f4d6fff14a23782cb8f21778). Each fetched commit listed the manifest alone. Actual full-history parent ancestry was not rechecked this run; two receipt parent pins remain unchecked against Git parent objects in this diagnostic. Diagnostic Rigger_Inline_Index_Receipt_Diagnostic_2026-11-27.json SHA256 e293a89e956686824b12ed235ba06bc56e67cfd12516587d75ed8590cfa6cff0. No new receipt recovery, no claim of independent editorial custody, no source PDF extraction or fresh source verification.

The SOTA2064 recovery archive SHA256 98da0c21e9b1d1c2ed89d0f7654f9ad314a789b9856beba6efeec673bcafb2ac was reacquired; embedded archives do not supply per-index original snapshot files for the eight historical transactions. The adjudication archive contains a manifest, not eight individually pinned original index snapshots. Do not substitute later Git exports or infer missing receipts for media van and police drones. Next: production CLI regression with original-artifact fixture, and precise triage of unsupported historical index schemas / missing original snapshots; independent Companion review and lineage remain unresolved. No semantic writes, new formal source acceptance, or global page credit.

## Matrix correction receipt schema (2026-11-27)

The two newly available Matrix source-owner correction archives retain original
prewrite baseline/candidate/plan, verified confirmation, index receipt and
indexed-manifest snapshot. Their receipt layout uses both commit/blob and
commit_sha/blob_sha, previous_blob, semantic_commit/semantic_blob, and
exact_commit_and_branch_readback. The old inline verifier rejected this
authentic shape. The narrow Matrix.yml adapter now requires the exact key set,
identical aliases, literal true, exact historical manifest snapshot and
independently pinned semantic commit/blob and parent manifest blob. Production
verify() obtains the parent from the existing actual index-transition proof;
it does not replace that proof. Conflicting aliases and missing pins block.

Observed archived source-owner review and exact current rule bytes:
* Scan Icon p101/PDF102 (record pp101–102/PDF102–103): active-memory OR
  frame/agent utility eligibility and running-Sleaze condition restored.
  Semantic e8271dba218179a5ee27ce408dcd931524123e09 / blob
  3408fff7a0aa662fac518d2fa21031697d63031c; index
  922860d036ae7985fce83ad943b39018f97f4385 / blob
  9791a5af8019349ac836f0afe84c355b2ccd06fc.
* Dump Log p98/PDF99 (record pp98–99/PDF99–100): baseline identifiers
  and security-dependent additional records restored, p40 discretion retained.
  Semantic 70f142cab2414c8e540f6d7f249b6d93f9b2db08 / blob
  752b38d951fba2a7c217d39d570d26a709bf20cd; index
  9452df9f8215dc06f5ef03e77c9db33b35d8f33a / blob
  714aeff0d47a15570b93f7be2d66cd42a742c48d.

Both pre/post archive pairs passed CRC and exact prewrite member comparison.
Actual pinned original prepare and confirm rechecks matched both retained
receipts. Eight selected typed bindings matched the archived source-owner
review; semantic historical/live blobs, archived historical index blobs
and exact current registration text matched. Connector commit file lists
each showed only the expected path. The lower-level receipt diagnostic
passed using independently fetched manifest blobs at each semantic commit
as prior-blob comparison pins. Actual index-parent ancestry, independent
original review, historical custody and full-book acceptance were NOT
established by this run. No fresh PDF verify-source execution is claimed
(the archived source SHA is
b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe).
Use the original archived journals, not reconstructed receipts.

Archive SHA-256 pre/post:
* Scan: c218c52c942178c005f39b11b9135a99abd59323babc89f4bbacdde302917053 /
  810496120aa0013cd7bae6fb195456c3104747855f0912dbc28b71a3fa12ad39.
* Dump: b6159521360310ec6fc2c4f21f4101f1f519dc43fd578336602435927dde42fe /
  f3ee29186f6386203a8074e1e38078aadf8992a9711e083dc88f2705b011c82d.

20 inline receipt tests passed (11 existing + 9 Matrix), 85 protected tests
passed using all eight live-blob-matched runtime dependencies. Full expanded
CLI integration remains outstanding; older synthetic positive fixture needs
the mandatory original index artifacts. Ordinary Contents writes and exact
commit/live byte readbacks matched locally tested blobs:
* inline_index_receipt.py: 62027a07d58af410b9bcc0e0a9896df14e61dd8d,
  blob c17c1b65541aee2d8c79dea20181f351621251bd.
* test_matrix_inline_receipt.py: 19bc73c27784617dfa2eff64eabafc12bfb85c1e,
  blob 41d62569a5cd7ebed690526d4f22f7af76c64a6a.

The two Companion cross-source Matrix concerns now have matching
source-owner corrected fields, not a formal cross-source acceptance.
No semantic or manifest writes by this worker; global page credit zero.


## Target: Wastelands — bounded production evidence reconciliation, 2026-11-27

Pinned main 5f229593a3f3e976cabd7d06d459899b02192d16; live source manifest
916247d5094422dadc0aed0a63f48d5244c3fd74. Fresh cataloged FanPro10653 original
(138 physical pages) returned actual source_pdf_hash_verified, SHA-256
31db497dcbe649eda35b596ed2dff9475241518027137c65f35ea720b03d0c6b.
Printed pp112–117/PDF113–118 visually inspected for the bounded scopes below.
30/30 exact typed biohazard equipment table properties match, including the
two printed dashes. Actual protected suites: 29 + 40 + 16 = 85 passed.
Four retained prewrite/confirmed archive pairs match their original bytes,
prepare/confirm re-executions, semantic blob at original commit and pinned
main, archived index snapshot and current unique registration. These are
present-day rechecks, not invented historical reviews or new transactions.

| Scope | Semantic commit / blob | Index commit / blob |
|---|---|---|
| Mutation | 85ef7b61046b2d26203b9e540f6ab2c6490cdec7 / 9047141e6ce053a8f075ed8e435e003fc8c4f173 | 30ee0558712c1e76f110a56be48eb85ea9286d03 / 6f0824a14454ea9bfb0d067a511f73112dd5c32f |
| Toxic domains | 0391d85c27fe20fe83ba302664870979a23f7d83 / f67ff781054cc510035562b5c424ade34b473579 | d3358a87b50bb62def203febaab1ec9900822373 / a6ccd17db97132cf17488760c5fcb5f2eb835dec |
| Biohazard equipment | 5b14c86f5a9cbf2f689cda132754549227a458f4 / 296036c8f6960d5a17695480ee5ce5148fa5f1e0 | 02577686eaab006454d26da06b7dc1fc394f8d73 / f7a756528477bfe5b96f882e4e6d261d1b69984e |
| Sand and Gear | 41594badee9470ff36b6109f9051ffc86acd7d2e / dd44da81a65dda6d11932ea691fbb98aa89a1ccf | 848ea4b63e312b1fe5d11650639222efab6ce2ba / 5d0b49c82169511276fe655d9cdec9a41feac7d6 |

Authenticated GitHub comparisons show all four index commits ancestral to
pinned main, three directly one commit ahead of the semantic write. Mutation
has six intervening-interval commits (ahead_by=6), and its exact index parent
was not independently recovered; prior manifest blob at semantic commit and
the index addition patch agree with the original receipt. Do not treat this
as full-history proof. Existing mutation/toxic qualification records retain
the source's option limits, dice, examples, potency guideline and Aura
Masking condition. No new missing gameplay procedure established. Rad-Suit
p113 explicitly refers to damage to the wearer: preserve that qualification
in any authorized owner clarification; do not infer a radiation boundary.

All eight formal scope dispositions remain BLOCKED, not newly certified:
survival/navigation (legacy skill evidence); pollution/disease/radiation
(bounded gear verification above, radiation boundary and legacy receipts);
mutation/toxic (two pairs verified, sterile shaman original journal and
mutation parent proof missing); desert (one pair verified, Black Wasp journal
and legacy receipts); polar (original Temperature Tolerance wording and
Silap Innua pool, legacy receipts); orbital (prior corrections retained,
legacy evidence); underwater (literal 6MN and legacy receipts); vehicle
adaptation (Stress and landing-distance variants, legacy receipts). All still
require complete independent original-derived field bindings and editorial
custody. Do not reopen unchanged scopes merely to repeat this assessment.

The current invocation could not acquire the authenticated full Git bundle
at pinned HEAD or independently pinned complete 138-page review, bindings
and evidence JSON files. The connector's PR-only workflow listing returned no
runs for pinned main; the Library search yielded no exact bundle artifact.
The actual full-book triage and validator CLI were therefore NOT executed;
BLOCKED here is a bounded prerequisite disposition, not a validator exit.
Machine-readable local diagnostic Wastelands_Acceptance_Bounded_Evidence_2026-11-27.json
SHA-256 de010d2e24ff95f80a3682678d910609ad31013b5fc23dd33f8233b986e31473.
No common gate, source canon or manifest changed; no page credit.


## Man & Machine — two newly indexed source-owner addenda, 2026-11-27

Forward-only workflow read at blob 2afd00d765314d425430618e2bb5b31f4440fdc6.
Read-only archival reconciliation at main dd4b4957f732f90ed259f19d7be46af67dc178e7,
M&M manifest blob 859c237e0e26dbd29543453861ddce52077bb578. Do not reopen the
already corrected original scopes or duplicate their mechanics. Four retained
source-owner ZIPs were reacquired by Library ID, CRC checked, hashed; both
prewrite/confirmed pairs retain byte-identical baseline, candidate, plan and
source-review files. Both actual protected prepare and confirm rechecks
match the original retained JSON, and candidate Git blobs match historical
and pinned-head exact-path readbacks. Eight live dependency blob pins matched
the kit; 29 preflight and 56 gate/preservation/recovery tests passed.

| Source scope | Semantic commit / blob | Index commit / blob |
|---|---|---|
| Signature p47/PDF47 | 3b5b0dc4e6a86ffc8effa96b3ad5446f2a085332 / df2f74015e4a0946cc38fcf1df3127057aa653b9 | e780530b2f706c235572f7e7f4bba78f743767d2 / 80316bfa511a6bc6b581df09e15740a1edc98467 |
| Shock Hand pp42–43,156/PDF42–43,157 | 41280ee3cb6e7d2050a0aa4bcf1a12a29c84b1aa / 5b9e3cfab95261679d8467db40303f7d6e901ba3 | c42232389a9261a911dd4db7d36beb80c5ca89f4 / 5cdad565952006b01c9db59198dd32e02a56ef8d |

Both index commits change the M&M manifest alone and their nested registration
entries match pinned-head entries. Connector comparison establishes both index
commits ancestral to the pinned head, with Signature directly one commit
after the semantic write and Shock Hand two commits after its write. The exact
Shock Hand index parent has not been independently fetched. Nine selected
typed source-owner review-to-candidate field comparisons matched; two further
archived image/modifier digest checks matched. The existing Signature modifier
blob fb722046f7f4a428a1e501b240e75ea0b078fb79 remains unchanged. Shock Hand
entity blobs b65d52987d8254cd9fce8c0bb344d6308a64b2d9 and
9963851a6dc29a0cff7f071199276520f78e48a1 still share the same ID; the latter
still points to p155. No consumer inventory or safe migration established;
the connector code-search queries returned no results, which is not evidence
of absence. Preserve both files pending source-owner/coordinator adjudication.

Archive SHA256 prewrite / confirmed:
- Signature: c7ad5bf395d951d4df059b078ff97e4dc8c1b12a0fe8bd297eeb0aba66f03f5c /
  710d09bb4787d259d2ed87ebe9b367f28462d8c24c223d366ac73d426d07d7fb.
- Shock Hand: 997b46641b09859131052254f09c300a96c44462115639ee89dd07aad0da020e /
  618f7fcc2900279e50908582fc95356a050ad323483ecbcaad6285de656282c2.

Exact archival-only blocker: neither confirmed ZIP contains an original local
indexed-manifest snapshot; their actual receipts explicitly disclose that
limitation. Do not manufacture it from later Git export. Both use new index
receipt layouts unsupported by inline_index_receipt.py (live blob
c17c1b65541aee2d8c79dea20181f351621251bd); that verifier's path regex also
excludes the literal ampersand in sources/manifests/M&M.yml. These are specific
future adapter requirements, not justification to bypass the mandatory
original artifact or to spend this run rewriting the verifier. Independent
review and complete source-wide bindings remain unestablished. The original
source SHA recorded by the owner is
6d4e25208e8ee3b8b8b05a7f9308ccdbf5a73f090f4d0b32a0916457a9dc5ec8;
no fresh original PDF selection, extraction, cache or verify-source was
performed in this archival reconciliation. Full production CLI not executed.
Diagnostic MM_Original_Receipt_Reconciliation_2026-11-27.json SHA256
252b661d30d59be866b4e7f3e814310a7acf61859eb225478c5294a2f077d5b9.
No new semantic writes, no formal book acceptance, no global page credit.


## Man & Machine — four newly indexed equipment-table corrections, 2026-11-27

Read-only reconciliation of newly available owner transactions, pinned main
eaa55ef4f3c2332bdf3490f34e34e11585c412fa, manifest blob
e1e02eeac39f3dfa9b48d6040f52589204043985. Forward-only workflow blob
2afd00d765314d425430618e2bb5b31f4440fdc6 read. No prior reconciled section
reopened. Printed pp41,155/PDF41,156 as recorded by the source owner.

| Record suffix | Semantic commit / blob | Index commit / blob |
|---|---|---|
| external-clip-port | 365eae9cda129090fa13d3c9b6cd551388317737 / ebe2b16c12d8bcf4e3848be715c8f07695dc260f | 677b423943b636a49e7f66a10f9033ec088263f5 / 9987ba006a064a32929b7d20bbf778be213a94df |
| laser-sight | 6c6040d47a7e9e2db6719bc5104a0d78d6b37d62 / 3452248a3768ac833a90a79e07a7340ab462355a | 04119f7f346a1146dc7f96f80d293183e3659c80 / 3be24137c1eb10e2549cb92687b07daca475d60b |
| silencer | 1f0e5a2fe363ee0e526362a38d4ea8d13e4a148c / 0a50c984f2f745f0327f62c59f4dc40466c8b79a | aede58d19a20624835c819babd5b2b3624733e14 / fd5bd7452d55cb4221ef72ea53ab5184d1c2091c |
| sound-suppressor | 9c8be54dcefcc4cfff2180a5960694ac7f269767 / 5223b9f32e465f012f7efd3f3afea14ff72a0214 | a3546c29174598e2fff7880d5f3f5c25c9df0d73 / 5436104048acc372079ed6bbc63ce6e16101b8fa |

All four original confirmed archives retain the original indexed-manifest
snapshot, unlike the previous Signature/Shock Hand archives. All six distinct
prewrite/confirmed ZIPs pass CRC. Original baseline/candidate/plan bytes match
across archive pairs; actual protected prepare and confirm re-executions match
retained JSON (4/4 each). Historical and pinned-head candidate Git blobs and
historical index manifest blobs match local exact hashes. Exact registration
excerpts match historical and pinned-head manifests. Each semantic commit
changes only its entity path and each index commit changes only M&M.yml.
Authenticated comparisons establish all four index commits ancestral to pinned
head; three index commits are one commit ahead of their semantic write, while
silencer is two ahead, so its exact index parent remains unestablished.
Twenty newly restored intrinsic fields match the actual source-owner commit
patches and archived baseline/candidate with exact types, including literal
dash strings. This is a commit-delta and archival comparison, not independent
original-image field review. All eight runtime dependency pins match;
29 editorial + 40 ingestion/preservation + 16 recovery tests passed.

New specific acceptance blockers: each original index receipt contains only
commit_sha and blob_sha, not a literal original exact-readback marker. The
archived snapshots and current readbacks do not supply missing historical
attestations. The live validator blob 24cbf4218164c410a2cb2ee0b0b539d3f53977ba
requires /data/ bindings, excluding these legitimate /intrinsic/ equipment
properties, and its safe-path rule excludes the literal ampersand in M&M.yml.
The inline verifier blob c17c1b65541aee2d8c79dea20181f351621251bd likewise
excludes that manifest path. Preserve these concrete adapter requirements
without waiving historical evidence. Independent source review and complete
book bindings remain outstanding. No full production validator executed.

Latest p41 tabletop boundaries source-owner commit
e98a3c74a3aae645c10900e1c31e47241acfd9b0 / 9cb0796d3bc700af679fdf3dca389d84e0f71b26
and index eaa55ef4f3c2332bdf3490f34e34e11585c412fa observed. Its prewrite ZIP
was located but confirmed archive was not present in the returned latest
folder listing; defer that distinct scope until original artifacts arrive.
No duplicate semantic transaction. The original source SHA is
6d4e25208e8ee3b8b8b05a7f9308ccdbf5a73f090f4d0b32a0916457a9dc5ec8
as retained by the owner. No fresh PDF verification or cache use claimed
during this archival reconciliation. Machine-readable diagnostic
MM_Accessory_Receipt_Reconciliation_2026-11-27.json SHA256
ac7f093ae6e6465ed5d21c3ed9d26a7c10a20095c71f60a06e4387342fb085ff.
No semantic writes, formal book acceptance, or global page credit.


## Newly recovered p41 M&M and p154 Rigger Revised journals — 2026-11-27

Read-only reconciliation at pinned main d4addd8922713e7c430a13dcb6a707c3b72459c6;
forward-only workflow blob 2afd00d765314d425430618e2bb5b31f4440fdc6 read.
Four newly selected prewrite/confirmed ZIPs pass CRC; the original baseline,
candidate, plan and review bytes agree across each pair. Actual gate prepare
and confirm re-executions match both retained receipts. All eight kit dependency
pins match live; 29 editorial, 40 ingestion/preservation and 16 recovery tests
passed. Both original indexed snapshots match historical and pinned-head manifest
blob pins; both candidate blobs match exact-path semantic and pinned-head reads.
Both index commits are directly one commit ahead of their semantic write,
change only the corresponding manifest, add the absent registration, and are
ancestors of pinned HEAD.

| Source scope | Semantic commit / blob | Index commit / blob |
|---|---|---|
| M&M p41/PDF41 game boundaries | e98a3c74a3aae645c10900e1c31e47241acfd9b0 / 9cb0796d3bc700af679fdf3dca389d84e0f71b26 | eaa55ef4f3c2332bdf3490f34e34e11585c412fa / e1e02eeac39f3dfa9b48d6040f52589204043985 |
| Rigger Revised p154/PDF156 medium sidecar | 3ba7600925be49a7317884c295c46a0de347ab3f / e0de56b1fe4bf5cba3460f2a2ac2505f3e0d46ab | bc547a1f4c4412ed70bedd4ad7b7f051f95f1c5b / 79af758172c9cebdfb15b69aaa8146022c83deb5 |

M&M original confirmed archive now available, registration pointer
/source_field_review/confirmed_cybergun_game_boundaries_p41_2026_11_27/records/0.
This is the previously deferred p41 scope only. Source-owner verification
receipt retains SHA256 6d4e25208e8ee3b8b8b05a7f9308ccdbf5a73f090f4d0b32a0916457a9dc5ec8.
Original index receipt has only commit_sha/blob_sha; explicit historical
readback attestation remains absent, and M&M manifest path is unsupported.

Rigger Revised registration /verified_semantic_records/115 and original
index receipt include explicit readbacks_exact=true and exact registration.
Owner review's medium sidecar price 2000 matches the typed canonical integer.
IMPORTANT demonstrated reference discrepancy: the same new rule claims that
the historical normalized medium price is 2500 at
rules/vehicles/customization-accessories.yml blob
2279fc22ec373a343dca1c27de6cd7d3fcc31225. Exact path fetched at the semantic
commit and pinned HEAD has that very blob, but its sidecar retrofit sequence
is 1,000/2,000/3,500 nuyen. Thus the claimed difference from that historical
canonical blob is not supported; the two recorded medium prices already
agree. Source owner must adjudicate/correct the historical-reference metadata
with original edition review. Do not duplicate the price or infer the printed
FASA7910 edition from normalization. Original revised source SHA retained:
88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909.
The original Rigger receipt uses index_commit/manifest_blob/registration/
readbacks_exact and is not yet supported by the inline verifier's strict
schemas. This does not make it a formal acceptance receipt.

No fresh original PDF review, cache use, full production CLI, independent
book-wide review, semantic writes or formal acceptance claimed. No global
page credit. Machine-readable diagnostic
Expanded_Acceptance_New_Journals_2026-11-27.json SHA256
9445a9338e9cef90affcdbb81c4cf10229b543f8d88177ed64bd745e2371c6c2.


## Newly indexed M&M device effects and ShadowBeat mixer — 2026-11-27

Read-only archival reconciliation at pinned main
2ac1a4f79d096b75bb67c1f8354c075380c76fe2; live forward-only workflow
f289054db49b55dec6f9e5a6401abaa6588c2e69 read. Both newly retained prewrite/
confirmed ZIP pairs pass CRC and all original prewrite member bytes agree.
Actual present-day prepare and confirm re-executions exactly match both
original receipts. The two archived indexed-manifest snapshots match the
historical and pinned-head Git blob pins. Both index commits are directly
one commit ahead of the semantic write, introduce a previously absent path
registration, change only their own manifest, and are ancestors of pinned
HEAD. Both semantic commits change only the corresponding record. No source
review or archival chronology is inferred from these checks.

| Scope | Semantic commit / blob | Index commit / blob |
|---|---|---|
| M&M printed/PDF41–42 implant device game effects | d4addd8922713e7c430a13dcb6a707c3b72459c6 / 19e909acdede83c507aafac613abb01e01b75623 | e9988c47623214872ecbf680478519fea85a4d8a / 4d0e3cbebec3f66d41402403fca8403505ae1191 |
| ShadowBeat unnumbered color insert PDF39 mixer | 97120f0ee1022b50dd0ac86b098a6388c245e5dc / b407be40908fc8b1ea8bea383b1e0afb3e7ccb84 | dc1bcc2750cad90f5d6c46265e560d2d47899f18 / be0dd90012dc31e7a6d01a4d5f177c07aaf8b8ec |

M&M registration pointer /source_field_review/confirmed_implant_device_effects_p41_42_2026_11_27/records/0.
Unlike the previous accessory receipts, this original index receipt explicitly
retains branch_and_commit_readback_equal=true and
exact_index_proposal_readback_equal=true. The original proposal and indexed
snapshot are byte-identical; manifest SHA256
44ca04ab0a471c18062b604f35aa81e1773b9bc6ee824e2f598c9186c33f8b9f.
The preserved review covers four device-specific tabletop game-effect groups
and integral magazine reload eligibility, without duplicating equipment
purchase stats. Original p41 external-port arrangement and compound-example
references remain for the source owner to compare. This is not pp41–49 closure.

ShadowBeat registration /verified_semantic_records/85. Retained original
index receipt has exact_index_bytes_match=true and matches the actual index
commit, semantic commit and record ID. Original mixer profile supplement
retains two integrated equipment labels; other uncertain original profile
fields remain unresolved. The source is original FASA7109 (1992), with SR3
adaptation explicitly unverified. Do not treat a legacy profile as a complete
SR3 playable stat block or infer unsuperseded mechanics from this archive.

Specific acceptance-only blockers: M&M's literal ampersand manifest path
and authentic new receipt schema remain unsupported by the expanded
validator. ShadowBeat's index_commit_sha/manifest_blob_sha/
exact_index_bytes_match receipt schema and readback_blob_sha/transaction_status
registration aliases are unsupported by current inline_index_receipt.py
(c17c1b65541aee2d8c79dea20181f351621251bd) and index_transition.py
(80a0f8ba358f6c71dcd10eb634b2e4ee92d87dbe). The numeric printed-page binding
also cannot certify the unnumbered original color insert. These defects do
not establish missing mechanics. Complete independent original review,
edition adjudication and book-wide bindings still required.

Original source hashes as retained by owners: M&M
6d4e25208e8ee3b8b8b05a7f9308ccdbf5a73f090f4d0b32a0916457a9dc5ec8;
ShadowBeat d111ebcfcab4e40645e61f2924e58b5d8ace6ab4c18610e3085e324c52bd4278.
No fresh original PDF acquisition, verify-source or cache use in this
archival-only run. Actual 29 editorial and 20 ingestion-gate tests passed,
with matching live code blobs. Four preservation/recovery dependency/test
blobs changed since the kit; those stale cached suites were not executed.
No full production validator run or formal acceptance. Original archives
remain in the Recovery library. Local diagnostic
MM_ShadowBeat_Bounded_Receipt_Reconciliation_2026-11-27.json SHA256
f589fc68fb17cfc56f282d1ada1b97d87f391b53c8c034a83795fbcf3d896b69.
No semantic or manifest writes by this worker, no global page credit.


## Newly indexed M&M reservoir exception and Cannon Companion p118 variants — 2026-11-27

Read-only archival reconciliation at pinned main
418336b9f534d00813f97f286cedb3c4c20fd7ef; forward-only workflow
f289054db49b55dec6f9e5a6401abaa6588c2e69 read. Four newly retained source-owner
ZIPs pass CRC; original prewrite members agree byte for byte with the
confirmed archives. Both present-day gate prepare and confirm re-executions
match original retained receipts (2/2 each), and local exact candidate and
index-snapshot Git blob hashes match historical and pinned-head GitHub
reads. Connector historical and pinned-head content compares equal.
Both semantic commits change only their own path, and both index commits
change only their own source manifest. Both index commits are ancestral to
the pinned head. Actual current editorial and ingestion-gate tests: 49
passed, exact cached script/test blobs match live. Four changed preservation/
recovery dependencies are not locally refreshed; stale suites not run.
No fresh PDF verification, extraction or cache use in this archival-only
scope; original source-owner verify-source receipts retained.

| Scope | Semantic commit / blob | Index commit / blob |
|---|---|---|
| M&M printed/PDF41–42 reservoir exception and references | fcb40a5cae126f46e8cb6592f1a26f9797540d9e / d2ffc488833f637f2930e00ec573ccaa20957862 | fb32ff23585256d00ff968e934b36f9e1a81a0b1 / 2b7e9c8c9651b7134d73c75a34c659dd28215961 |
| Cannon Companion printed118/PDF119 appendix variants | 3d5dfa7dc9c3543bc7b60145ab29fd549601ce49 / e8952fcb7466c901f31e0492833240aa307454e2 | 9f8edafd2c4174ca2c0922d47e5896958b0a2a23 / 155fd75fb9428992adb3a40e3bcead384eb209c7 |

M&M four new source-owner field groups match the commit delta, including the
explicit optional accessory exception, narrowed restriction and two original
cross-references. The correction supersedes the prior semantic blob
19e909acdede83c507aafac613abb01e01b75623 at the same path; both historical
registrations remain in the live manifest. New registration pointer:
 /source_field_review/confirmed_reservoir_accessory_exception_2026_11_27/records/0.
The actual original index receipt has branch_and_commit_readbacks_equal=true
and exact_local_proposal_match=true. This receipt schema is unsupported by
the current inline verifier, as is the literal ampersand in the manifest path.
Do not discard the prior registration or infer a valid successor chain merely
from current blob equality. Semantic-to-index comparison is ahead_by=2;
the exact index parent is not independently established. The previous
M&M source hash retained in the original verification artifact is
6d4e25208e8ee3b8b8b05a7f9308ccdbf5a73f090f4d0b32a0916457a9dc5ec8.

Cannon Companion registration:
 /source_mechanics_reconciliation_2026_11_27_p118_appendix_launcher_variants/verified_semantic_records/0.
Index follows semantic commit directly; manifest at semantic commit has
blob 9167e6d9a41343d8185fe5c23a60677d21bf46ec, equal to original receipt's
prior_blob. Original index receipt contains explicit committed and live
readback attestations, matching index/blob aliases and semantic identity,
but is a further unsupported receipt schema. The three pinned core
reference cells were independently checked in the exact historical core
acceptance snapshot (blob 2d6ad408ffa7a07e887998bbe6fac3de6266c69f).
All three agree with the new record's description of the core version;
source-specific variants and unresolved shared precedence remain distinct.
Original source SHA retained:
7b979ed358aaa23bbe68eb95a0887b1315f302bedd6bcc04df00d8d68fbd84a4.
This verifies the reference comparison and original archive consistency,
not independent fresh source fidelity or source-wide closure.

Machine-readable diagnostic MM_CC_New_Receipt_Reconciliation_2026-11-27.json
SHA256 cf15913325212003098c5d32ac765b086140cdd4abcf6d155fe8981a3bf25afd.
Full production CLI still not executed: no authenticated full Git bundle
or independently pinned complete source review/bindings/evidence; the
connector's PR-only workflow listing for pinned main returned no runs.
No semantic writes, formal book acceptance, global page credit, or changes
to common gates or worker configuration.


## 2026-11-27 — retained M&M / Cannon index schemas and successor acceptance dependency

Closure-first engineering only. No semantic, manifest, checkpoint, schedule or protected gate mutation; zero global pages. The start HEAD was `47388b9e3b94735f2204f3ef0cc238a1f89d0a10`; live forward-ingestion-v2 read at `f289054db49b55dec6f9e5a6401abaa6588c2e69`. Restored four changed runtime dependencies locally, with exact blob verification: preservation_method.py `338caa42e355c7611247a0925b2b03c4fd76c1e3`, test_preservation_method.py `a7613a2320e698e39d6759e0490aab53283a4ac5`, transaction_recovery.py `bc15e089ae4557812a940ebf23056a179c978e5c`, tests/test_transaction_recovery.py `cd2ff87d33e9703c1d5f1bc0533f90d99d9c103f`. Actual protected tests: 29 editorial, 43 ingestion/preservation, 17 recovery passed.

The isolated validator now supports the exact observed three original receipt schemas, the literal M&M manifest path (not generic unsafe paths), source-local equipment_stat /intrinsic/ bindings, and the exact observed nested M&M registration shape with independently typed canonical class and source-review evidence. All original digest, readback, source identity, same-record, ancestry and independence requirements remain. The earlier four M&M accessory receipts without explicit original readback attestations are NOT certified. The old advisory blocker_triage pointer predicate still needs alignment with the validator's narrow /intrinsic/ support; it is not a basis for a formal decision.

| File under tools/expanded_acceptance/ | Tested exact blob | Contents commit |
|---|---|---|
| source_index_receipts.py | 7983546197e9f43ead75dd8e653d88ae65364783 | 1a39956b3913e664df12755ddcdad5fbc346abff |
| test_source_index_receipts.py | 100047cd15602bcf196dbbc38bcdc58b1ae298ee | fbf6e08e33a62b1ffa138da7a6586b27f4dcf68e |
| inline_index_receipt.py | eb6685e9f9ae1459f1ac00f05e6fb76a891b5192 | af82e18b0c995d3bce54ca0123f1a4ca69f43e4b |
| binding_schema.py | 8e9d07b24692b3ccfd9c36018852c42193ee4216 | c593009546be30e68866c1e54f77243e3261724f |
| test_binding_schema.py | 54d909095ee06d866470471e7907b29f0541e858 | 11b137eb9b722503649394d150c54f9561d313df |
| mm_successor.py | 466893ce02d765c4179485b624e044c8b1c9df51 | aeb2539239ed580732aef87b6af75bf99e80a6a5 |
| test_mm_successor.py | 96f49ea59ae534b06489b39807816294e4dfbf82 | 7df7e12387c60ee072662a997e0a97870d025ec0 |
| validator.py | a2e3daaed6de053bd7d77ec7a090d2e24defdae6 | e7ae40e27c4f8ad33cda9fe41aa453b6b467e964 |
| test_current_cli_integration.py | 240c941c78803a7d57379bd29e90d6cb83ed55b8 | f27134a031ef883b0bd8a74dc7b4fd335525c9e5 |
| test_mm_successor_evidence.py | 0103052d31c3920e5e01e9ef691245035c424ac7 | 72510144db59c815bce7b957b8d8ba8bfe79744c |

Actual 21 new synthetic tests passed locally (9 receipt schema, 4 binding, 6 Git successor history, 1 CLI integration, 1 full successor evidence with actual local Git and protected gate execution). The CLI synthetic fixture passes literal dash, original index receipt/snapshot, individual transition and actual source hash check; missing snapshot and null substitution are blocked. Full successor fixture passes only with both registrations and independent lineage review artifact, and blocks same reviewer/custodian and absent predecessor snapshot. Synthetic evidence is not production certification.

Three retained authentic archive index receipt/snapshot pairs rechecked against exact original Git blob pins, plus six tampered-artifact negatives rejected. These are previously recovered journals, not new recovery:

| Scope | Semantic commit / blob | Original index commit / manifest blob |
|---|---|---|
| M&M pp41-42 previous device effects | d4addd8922713e7c430a13dcb6a707c3b72459c6 / 19e909acdede83c507aafac613abb01e01b75623 | e9988c47623214872ecbf680478519fea85a4d8a / 4d0e3cbebec3f66d41402403fca8403505ae1191 |
| M&M pp41-42 current reservoir exception | fcb40a5cae126f46e8cb6592f1a26f9797540d9e / d2ffc488833f637f2930e00ec573ccaa20957862 | fb32ff23585256d00ff968e934b36f9e1a81a0b1 / 2b7e9c8c9651b7134d73c75a34c659dd28215961 |
| Cannon Companion p118/PDF119 launcher variants | 3d5dfa7dc9c3543bc7b60145ab29fd549601ce49 / e8952fcb7466c901f31e0492833240aa307454e2 | 9f8edafd2c4174ca2c0922d47e5896958b0a2a23 / 155fd75fb9428992adb3a40e3bcead384eb209c7 |

M&M previous archive Library libfile_6b693c0a7284819185119822d40c511b, SHA256 b74755b479b15ded676719e8bdaea227dd2feb293cd3788601f3398f68f204a1; current libfile_f85876c09e78819196bb39deb163fcda, SHA256 416279f05ec7489b765f4a1573210670ec90dbb949fe63ec76c88060c01d8198. Cannon libfile_2092b1ed83408191b498f5680573625f, SHA256 98c2c24eff125d5714573b8b0b05130f55cedd995aaeb9990a29347a38f25803. Source SHA pins retained, not freshly verified: M&M 6d4e25208e8ee3b8b8b05a7f9308ccdbf5a73f090f4d0b32a0916457a9dc5ec8; Cannon 7b979ed358aaa23bbe68eb95a0887b1315f302bedd6bcc04df00d8d68fbd84a4.

New bounded connector ancestry evidence: M&M previous semantic to index ahead 1/behind 0; previous index to current semantic ahead 12/behind 0. Current semantic to 2a9546671a22aeedabd2cd31f8e725c35f1791c1 ahead 1/behind 0 (docs only); that intermediate commit to current index ahead 1/behind 0 (M&M manifest only). Intermediate manifest blob still previous 4d0e3cbebec3f66d41402403fca8403505ae1191, path blob already current d2ffc488833f637f2930e00ec573ccaa20957862. Both exact nested registrations retained at observed live manifest 3948530837d51f056ae06ada7d68cdc9805a5b0d; live semantic path matches current blob. Cannon index follows semantic directly, previous manifest blob 9167e6d9a41343d8185fe5c23a60677d21bf46ec matches original receipt. Preserve Cannon variants and independently adjudicate edition precedence.

Production M&M proof for rules/cyberware/mm-implant-device-game-effects-p41-42.yml now mandates predecessor_transaction and successor_review_artifact on the current transaction, historical original artifact custody and both real index transitions. The successor_review_artifact is independently pinned JSON protocol sr3-mm-successor-review/v1 binding source, source_sha256, path, record_id, previous/current semantic commit/blob, previous/current index commit, reviewer distinct from source reviewer/custodian, original_review_locator, all_changed_fields_reviewed=true, same_edition_confirmed=true, current_controls=true. These flags require actual separate review, not manufacture from Git. Predecessor uses normal inline original baseline/candidate/prepare/confirm/editorial/index receipt/index snapshot. The actual complete production proof remains blocked by independent adjudication and full local history; connector compare evidence is not the full local Git verifier execution.

Coordinator handoff: ledger pin 3b70c1365638b8c5e393c1bd922bae06ede18b82 records previous authenticated history export at 4454f82eea80b020ca9c278ed795ce68e14512de, predating current records; current-head workflow lookup returned no runs through available PR-filtered connector, which does not prove no run exists. Current authenticated complete history and independently pinned original-derived source-wide review/bindings/evidence JSON were not acquired. Loose Alliances still needs successful original archaeology journal and Dragonheart lineage; move to the next eligible existing candidate once independently pinned inputs arrive, not another unchanged receipt replay. For Wastelands eight formal scopes and Companion remaining grapple/Rigger2 lineage, independent bindings remain outstanding. No new production blocker_triage or validator book verdict, source verification, mechanical fields, journals recovered, section/source certifications or page credit claimed in this run. Existing accepted core/Denver and ownership boundaries remain untouched.

### 2026-11-27 — Independent Loose Alliances and Sprawl Survival Guide bounded assessment

Observed main ac41a5ec00b293e6021c4130b1dc12978be74560. Qualified candidate ZIP 15244033288 (successful run 46098314462), seed 47388b9e3b94735f2204f3ef0cc238a1f89d0a10, ZIP SHA256 bb33235fe56adff2fbba89e7d6fb1614ec49dafa59fc457a382478b1882b538b, CRC verified; source packets matched the live manifest blobs below. Historical bundle 15183376250 SHA256 9c90961adc6d26aaf5f02087e16906ff57440c175da5905504fe4ddfc460ab6d verified, restored non-shallow history at 4454f82eea80b020ca9c278ed795ce68e14512de, 303 commits behind observed main; core receipt ancestry verified. Not a current-head production repository.

**FanPro25006 (Sourcebooks owner):** exact live manifest 90cae8c7a434fec68797ff88f4ea847b4bb6195e, fresh original PDF SHA256 5837dcdece5075140a57e743e0cd49a30d8530b13eb0ee94f39655f8b95ad6bf; actual verify-source returned source_pdf_hash_verified, 165 physical pages. Bounded independent original review of Archaeological Groups pp152–153 and the attributed Dragonheart account pp128–130, five normalized typed bindings matched; no new local mechanic established missing in these headings. The archaeological record options/characters/la-archaeological-teams-p152-153.yml semantic 1cff50029deeef5eb036687c96cb9b1218901804 / 58345acba5cd4193790cf82afe3b6697082b8042, index ec74a7d35f4a7e204a162233f29d9035efe1aba2 / d12952bbfedaac793a129416df28187b59b3b8bb, historical pointer /verified_semantic_records/23 and current /verified_semantic_records/33. Dragonheart references/loose-alliances/dragonheart-p129-130.yml semantic 2ab3a108a1c2f54493040ad688077e607545e40c / fd842e8d59f53433cd8de54a2b6d673de035d7db, index 47ea2051b9a3b1997f08a7e0511d128bea4dbe83 / f2a61f1bf1c6733c149d47538d90577959ccde2b, historical pointer /verified_semantic_records/0 and current /verified_semantic_records/2. Exact rows and individual historical index transitions actually verified from restored Git history. Original archaeology prewrite baseline/candidate/plan, confirm, editorial and original index receipt/snapshot remain missing; external artifact lineage unadjudicated. Actual blocker_triage on self-pinned partial original-derived inputs returned TRIAGE_ONLY (post-fix 18 blockers across receipt, inventory, original rule, independence and equivalence); current-head validator executed and BLOCKED, Git cat-file exit 128 (missing current commit). Complete independently pinned source-wide review, custody and current full history still required. No book PASS.

**FanPro10667 (Critters owner) — new precise mechanical correction candidates:** live manifest 7f7064b6f9941de0d1248b64f27ca9af2201933d; fresh original PDF SHA256 b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f, actual verify-source source_pdf_hash_verified, 146 pages. Inspected p123/PDF124 and lifestyle ambiguity loci p128/PDF129, p137/PDF138, pp143–144/PDF144–145. Nineteen typed comparisons matched. Retain paint/controller header anomaly, Housing vs Space and example modifier cap conflict without inferred precedence. While inspecting the actual cap paragraph, three distinct adjacent original p137 qualifications were found missing or narrower in rules/lifestyle/ssg-detailed-lifestyle-edges-flaws-p137-144.yml, exact live blob 865aedaca5f992bfdec61306246923168612a39d, semantic a838f8a617de31446e13756ed8e6aac5c15fccae, current registration /postscan_verified_mechanics_recovery/verified_semantic_records/27:
- /data/edges/0/effect (Astral Repellent): distinguish the general Willpower TN5 entry test for any astral being (including projecting metahumans and conjured spirits) from the spirit test immediately following successful conjuring inside the home, whose failure also fails conjuring. Existing effect conflates these. Preserve modifier and incompatibility.
- /data/edges/2/effect (Concerned Neighbors): add the two responses to noticed activity (check on character or call security) and coexistence of neighbor options for distinct neighbor sets, retaining Intelligence 3.
- /data/edges/3/effect (Defensive Setup): include familiar regular visitors and ability to move to gain the specified combat bonus; current effect narrows eligibility to residents and describes automatic benefit.
Seed/manifest lookup, exact live target bytes and bounded historical named-record search were checked; no assertion of corpus-wide absence. Route these three to existing Critters owner for independent original source review and real individual gated correction/index if confirmed; coordinator should update existing inventory upon disposition. Do not reopen the full book or treat the 25 original six-artifact gaps as new mechanics.

**Acceptance-only compatibility fix:** historical list positions demonstrably differ even when exact indexed rows persist. Inline transactions may explicitly supply historical_index_pointer (at original index commit) alongside index_pointer (at current pinned head). Omission retains original same-pointer requirement. Exact typed row equality, source/record identity, actual historical transition and original receipt/snapshot checks remain mandatory; no heuristic pointer search. Validator 9bf418405a9f019d15fcd8afccb3a6858751c1b4 / 60c3021e72e777605054c681cbe162073ef1ff91; triage 5b4a14fedc97f5b37613e88f0076f51fa9fed731 / 12dbb810bb7925ea050d3fa5d8bb062ff44620aa now uses shared narrow equipment intrinsic predicate and names both missing original index artifacts. Tests 7fc7bada25f633eff710692edc62a24484334619 / 90ac63a4e028e2b0fd10809d7a9418f381d22941 and 2b9fcb6626c34ee23fc7aa64cde62af644663a8e / 3c8f1333a1eb459d5b034731f38fca9500d89409; actual 35/35 focused tests passed, exact bytes read back. Restored changed protected dependencies locally, 89/89 protected tests passed, no protected code modified. Actual source-cache preparation 0.829s + 3.102s, ten selected images, zero cache hits; not worker-hour throughput. No new canonical mechanic written, no original receipt recovered, no book accepted, no global page advancement. Next: Critters owner p137 three exact deltas; coordinator secure independent LA inventory and archaeology journal plus external lineage, then continue Wastelands existing finite blockers if LA/SSG blocked.


### 2026-11-27 — Current authenticated history, Wastelands original receipts and bounded field handoff

Current-head history obstacle cleared at independently observed main 09840aeddf5314b45d0656b3d350e20fd2fcc627. Successful history export run 46110658144, artifact 15249527382; ZIP SHA256 052925f8a69a3dce71c82f3bd2fe580af0d811da0e6ce219f68eede3cccbbe2b, bundle SHA256 21af3befb5e4cd5ef3790d7b78cb559994e710c53177480b2bf68f4802c70bf0, CRC and actual git bundle verify passed; restored non-shallow repository contains 12,365 reachable commits. All three FASA7001 acceptance snapshot blobs match historical commit 6baeb5dffd92dbdcbe50aa451d637e8ae9702316, ancestor of this head. This is a pinned current-head observation, not a promise that later main is unchanged. Previous successful history run 46103916202 also restored; stale optional seed not used as authority.

**Three acceptance dependencies resolved.** Previous CI run 46103916169 had 181 passing and one obsolete CLI integration fixture failure: unintentional pycache in the synthetic single-path commit plus absent original index artifacts. Isolated fixture corrected 25a61be9a74b9acfc162f96d0663b1dc11159cb9 / 5dd038ec4888168a11c47ed25f95aa60d7cdbf36, not a gate relaxation. Wastelands original Alter Pressure exact receipt schema supported by c6610f16c49a925d97ee5eac81c96bd44f0c64d1 / 2c4a61291481aa5e5a6e7ddf01eef4f5e1929610 and tests 06067571ac2eed0735ac08f6e8f1f3cb156339ad / 1cff461f5939b294e1a6a5c8de57768c5fb95417. Explicit original readback, exact source and confirmed record/semantic pins, actual index-parent manifest blob, original snapshot bytes and strict seven-field schema are mandatory. Two polar original index receipts lack explicit historical readback attestations and remain blocked; do not relabel their present-day exact Git match as an original attestation. Validator's structural assessment also previously hardcoded commit/blob/gate before transition proof; the Wastelands exact ten-field row now verifies printed/PDF provenance, class, semantic/candidate/immutable hashes and gate status at both explicit historical/current registration pointers. Binding code 7bc48d46df72d95bf1d82bdf97f9308d0e40552c / 0133552daccce493bb303f8ee8cc2a5929b32056; validator ede9fb37cca5372b8813e9353c1422d0991c05ac / ee3358bdc3c100efe508421bad76601fb7183344; tests 09840aeddf5314b45d0656b3d350e20fd2fcc627 / 2024c957a95677068870d0cac7a282276fd430f7. Exact tested committed and main bytes matched. Actual GitHub Actions run 46110658130 succeeded with **195/195** expanded acceptance tests. Common gates unchanged.

**FanPro10653 original evidence:** live manifest b85aca83d1ff82d1d4ef3ed3c270f54ca65007d9, fresh catalog original SHA256 31db497dcbe649eda35b596ed2dff9475241518027137c65f35ea720b03d0c6b, 138 physical pages, actual verify-source source_pdf_hash_verified. Three newly recovered original prewrite/confirmed archive pairs, CRC and baseline/candidate/plan cross-archive bytes match; actual protected prepare and confirm rechecks matched each original plan/receipt. Actual complete Git single-path, ancestry, new registration transition, candidate bytes and archived index snapshot bytes matched each. Exact current/historical ten-field registrations independently checked at:
- Alter Pressure printed p130/PDF131: entity.spell.alter-pressure, ce79c483d0ee2243bd22d88e3fc011fcf3ee949a / f8b5056506ed33e0173b1476e761d4b6ef58a9e3; index 1866c0b1500b9e906602fa801c4973877cacfa30 / c39611d60a2bbd3aedfa9b9e07269f5390f3b1e9, parent semantic commit and manifest 27284d44c81a3dddb4d8d49745415f031ac1043f, /verified_semantic_records/35. Original index artifacts passed actual new verifier; still needs independently pinned historical editorial review.
- Polar gear pp122–123/PDF123–124: ca3d34332b90b553972024294409dc0a970a1db9 / fe540548df345c38ffe5df8c872eeb675936b8f4; index 109c311a53b17d7cbd86aaf2334cbe846358fac4 / cdf65604bb6863f26a20dd3abe6e092272191fcd, parent semantic commit and manifest 5d0b49c82169511276fe655d9cdec9a41feac7d6, /verified_semantic_records/31. Original explicit readback attestation absent.
- Polar hazards pp121–124/PDF122–125: f22db45afa808f23ff216a4983ee326fb1365fd0 / d9a9481bdc9db19ac94e8a0251fd5e2df97bdded; index 60e5ffc36300f77aa4b4df32b9c12432281ae5f8 / c228b16df7e0237be6e0f51efd9af01737203c06, parent semantic commit and manifest cdf65604bb6863f26a20dd3abe6e092272191fcd, /verified_semantic_records/32. Original explicit readback attestation absent.
- Prior mutation archive was already recovered, not a new receipt: now actual complete Git parent-to-index proof passes 85ef7b61046b2d26203b9e540f6ab2c6490cdec7 / 9047141e6ce053a8f075ed8e435e003fc8c4f173, index 30ee0558712c1e76f110a56be48eb85ea9286d03 / 6f0824a14454ea9bfb0d067a511f73112dd5c32f, actual parent e95fb3444460da62557e8805d563961c8817d58d / bbee09d6ed737937b4862b1c1c14471e3da1c383, /verified_semantic_records/27.

**Original coverage and precise owner handoff:** visually inspected PDF112–114, 122–125 and 131–133. Eight polar purchase table rows (48/48 typed fields) match current canonical record; this finite table is coverage-only, not formal acceptance. Seven Alter Pressure header/example comparisons match; hull cutters printed p131 literal 6MN matches both source records and remains uninterpreted. Silap Innua p124 combat pool F+1 is printed; the following Astral Combat Pool value is missing from the printed line and remains unresolved, not zero. Polar p123 Temperature Tolerance parenthesis says desert Survival Tests; retain variant. Radiation p111/p113 threshold wording discrepancy remains explicitly preserved. **New candidate for existing Critters/Wastelands owner:** printed p131/PDF132 Screaming Mimi fictional tabletop target-classification prerequisite is absent from entities/gear/target-wastelands-underwater-systems.yml /data/entries/2/rules, exact blob 3f12bdedacd3a87412dbfb5f4ab5d1b827dce7; related entities/gear/target-wastelands-underwater-qualifications.yml a9493b7531370509339824846fb28190b043fafa and rules/security/target-wastelands-underwater-detection.yml 93b45505e3cee6d7903da8068f43f716026f16f4 do not supply it. The original requires classification as hostile or foreign before activation; preserve it as a fictional game eligibility condition, no invented numeric test or real-world implementation. Route for owner's independently verified correction if confirmed; no semantic change by acceptance worker.

Actual blocker_triage on self-pinned partial original-derived inputs returned TRIAGE_ONLY, nine blockers (independence 1, inventory 2, original_rule 3, binding 1, receipt 2). Actual validator run against the freshly acquired original PDF and authenticated exact observed current head 09840aeddf5314b45d0656b3d350e20fd2fcc627 now BLOCKED specifically independent_review_required, not missing Git objects. Coordinator must supply independent custodian/reviewer, complete original-derived 138-page obligations and folio inventory, original editorial evidence for Alter Pressure, accepted transaction evidence for underwater systems and outstanding legacy journal/variant adjudications. No automatically accepted source. This is the current finite Wastelands proof, not reopening core/Denver or retro-certifying prior source work. Remaining eight source-owner formal scopes stay blocked. No canonical write, no newly confirmed mechanical fields, no fully certified scopes/books, zero global page advancement.


## FASA7905a p130 Actions — 38 bounded original index classifications and accepted-parent dispositions (2026-11-27)

Following the Wastelands verdict, independently reacquired both cataloged PDFs for this open *Companion* index scope and actually ran `preservation_method.py verify-source`: FASA7905a, 138 physical pages, SHA256 `8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5`, manifest `4c014f59d657cb872eef541f8a2693b26d8d2a6e`; FASA7001, 345 physical pages, SHA256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`, manifest `b0ebffa4985ab544e64857b99e98b17d69ee3184`. Both returned `source_pdf_hash_verified`. Source-cache renders inspected: Companion PDF131 and core PDF106–109, 172–174, 198, 289, 310. This was an open supplement index comparison, not reopening or modifying the closed core. Actual owner 38-row map checked against original labels and classes and exact current/historically accepted registered target bytes at pinned head `09840aeddf5314b45d0656b3d350e20fd2fcc627`; live manifest and all six target blobs separately rechecked. All 38 action classifications match their detailed original SR3 heading with the original qualifications retained; this is index coverage, **not** 38 equivalent full procedures.

Actual production invocation exposed a defect the original synthetic tests masked: the narrow p130 index-reference adapter and fixture both used a mistyped Companion digest (e63a363 instead of e63e363). Corrected to the authentic source SHA, with explicit rejection of the old digest, then restricted the expanded reference mode to the eleven original p130 Free labels, their exact General/Combat/Magic groups, accepted core record identity and full adjacent qualifying condition. Unreviewed combined magic label, wrong group, altered source, missing custody and dropped conditions remain rejected. Final implementation commit `4f788d77a72a0dc1b2533009cc9733d9a84f00c9`, exact blob `28b7b4652bb567ee42b2f1b51597588cf075aad1`; final regression commit `0570e336017473b83cd1904252438a78ec015552`, exact blob `d53ed9aa877a081912d3ad2567966e5dcdc44091`. Intermediate digest corrections `ad3784fc9f5212038f06a3d94a757b5096d8179e` and `b41521b7ddc093b55740f595a8372f82935ce38a`. Exact tested content and live/historical readback matched. 37 targeted local tests passed; final full GitHub Actions contract test run 46111537962, at 0570e336017473b83cd1904252438a78ec015552, actually passed **199/199** (6.958s). Earlier full local invocation exceeded its 30-second tool timeout; no unobserved local pass claimed.

**Actual historic core receipt**: `6baeb5dffd92dbdcbe50aa451d637e8ae9702316` / `d11888c9f20b5603f874f4e976dff3e23c8cde98`; accepted manifest `a79b28a3970668982ef44a5318642ed55848839a` and queue `366ee748f51dbf2b699a26edbc1215352743191d` actually checked. Eleven Free candidate descendants of accepted /data/selected_free_actions (phase blob `87371b67cf6ac9e57ffd276d44713eaa3cdafcfd`) now each reach the legitimate `independent_original_page_equivalence_review_required` blocker in the actual adapter against original source and full Git history, rather than the mistaken source identity or unsupported label. No fabricated independent reviewer supplied.

Of the 27 non-Free rows, **seven** have bounded alternative accepted-parent index routes (not yet full proof; preserve original qualifications outside the selected group):
- simple.combat[3] Insert Clip and [6] Remove Clip: procedure.firearms.sr3-core-ammunition-reloading, accepted /data/ammo_reloading_table/0/action; p280/PDF289, blob `6699745b7bad26e3ad808e360edb4f66f7f86fe7`, commit `ef9eea41d7f38ab23cbea11cb4ffa4100287fa17`. Core pp106–107 require ready weapon, prior removal for insertion and smartlink Free exception for removal.
- complex.combat[5] Reload Firearm: same table rows 2–7 for non-clip mechanisms, alongside p108/PDF109; do not collapse the Simple clip row or distinct Complex clip loading. The candidate is scoped, not an unconditional single-action rule.
- complex.magic[2] Astrally Project or Return: accepted /data/projection_actions/enter and /exit, p172/PDF173, blob `974e21185f2403741453da313896460641e0fb81`, commit `574b60401e774eb5cb99eb66daa10b4bb398ed18`. Preserve Exclusive, no maintenance action and other Exclusive-action limits.
- complex.magic[3] Banish Spirit and [9] Control Spirit: accepted /data/banishing/action and /data/controlling_spirits/action, p189/PDF198, blob `cb1253425d56ef7f027d69bcde0d0b3808a91cc0`, commit `8bbd438740c2c223e020d06a10f016923a20cd6f`. Preserve each separate tradition, eligibility, contest and astral limits.
- complex.magic[12] Erase Astral Signature: accepted /data/astral_signatures/timing, p172/PDF173, blob `b9bca9574a128959d2136fb95710c3b1fe7db0af`, commit `1eebb21415a99c63f19e2370251b21245b01edec`. Action count equals Force; retain astral perception, distinct skill/test and Drain requirements.

Twenty other non-Free rows match original classification but still lack a demonstrated alternative accepted parent in this bounded lookup (do not promote /data/action_economy, /data/wired_reflex_system or merely indexed rule paths into accepted field coverage). The existing adapter deliberately does not equate a label with a different typed procedure-class field; seven routes need an explicit independently attested qualified-index comparison and narrowly reviewed schema before acceptance. The remaining 112 shared noncore references remain separate in the owner's existing checklist. No new rule transaction, no historical receipt fabricated, no protected manifest or core changed. Next: coordinator authenticate independent original-page/custody evidence for the eleven supported Free rows, then adjudicate the seven qualified routes and the twenty missing accepted-parent addenda; use existing source-owner checklist for the 112 noncore references. No formal book acceptance or global page credit.


## 2026-11-28 — Target: Matrix bounded table and historical receipt compatibility

FASA7219 / source.fasa-7219, SR3, 138 physical PDF pages. Fresh cataloged original SHA256 `dc9fbba78b9eb5efc60941213a90dfa0be190275dc92ea671631ddb7db154c4b`; actual preservation_method.py verify-source returned `source_pdf_hash_verified` against manifest blob `aebf5466822d09016fb7fd1fce8da963667ca311`. Original images for the four tables on printed pp116–119/PDF117–120 were previously independently inspected; no new page review claimed. All 63 existing original-derived typed comparisons and their exact legacy leaf pointers now pass the bounded binding predicate, not full-book acceptance. The source, exact record path, rule class, printed/PDF page, and allowed table leaf paths are constrained. Arbitrary root metadata, altered source, wrong pages, unreviewed leaves and cross-source use are rejected.

Historical grid record `rules/matrix/target-matrix-grids.yml`: semantic commit `c20a2cc2ab8185ffb62c9782ac095eee980dc0f4`, blob `bd19f614f18e2e458dd14288a75c54e666f341f8`; actual verified index transition `57fbe17e58a587151ec500cc0c178553c2a6b3a3`, index manifest blob `f7662c4db910e93c6b5342112bdd6b3805e3d634`, pointer /grid_original_mechanics_reconciliation_2026_11_26/verified_semantic_records/0. Historical and snapshot-head registered entry equal. This is not recovery of the original grid prewrite/confirm/index archive.

Implementation commit/blob pins: target_matrix_binding.py `2735e73fc81e72630e0f7807c2aa8f2123b6b60a` / `fb45e4495b6b97eedbc8340d8dcd69b5ed0882c2`; test_target_matrix_binding.py `3aefbbf9647fdecff15514ea847ff4f37e54bf49` / `0a950d61d423d8f5462d1c2f1a8c55e4a0f2525c`; binding_schema.py `ba50c0cce0eabb01636ef861b472bdd36e2900c5` / `d65af5f6695619ae6d4f2a472122cc2046208e0b`; validator.py `8d42df7c74a96d60b40c1a6fd6cbc88b8f5cd962` / `ebfc205de4029155de2142fb9cd7cc3198e65ca8`; blocker_triage.py `8e2ca7f21a51a4f4c46f97b0c9192c7a3b63758b` / `082c161cda18d6706ca2cabc11152d749ad6c353`. Exact tested bytes read back. 26 local focused tests passed; actual GitHub Actions contract checks run 46117230401 succeeded.

Authenticated full history artifact 15252382048 (run 46117230408), actual ZIP SHA256 `a780f763e3c01f2b82e07f755f7c0a7b329caeb3bc93fb6113d82571a4a9a6fd`, bundle SHA256 `214834d96c25d7d2a6922b8631cb658c975ce46f32486adb4f2f38c621b875d1`. CRC, actual bundle verify, nonshallow clone, pinned HEAD and closed-core receipt/manifest/queue ancestry checked. Snapshot `8e2ca7f21a51a4f4c46f97b0c9192c7a3b63758b` has 12,407 reachable commits; later main `258820311d9f9f966b7774817d5c71324e1cbe55` was separately observed. Never describe the snapshot as subsequent main. Actual pinned-input diagnostic blocker_triage now reports five blockers: independent reviewer/custodian, physical page coverage, printed folio reconciliation, unresolved full inventory, grid transaction evidence. No binding blockers. Actual validator against this restored Git history and the freshly authenticated PDF exits 1 BLOCKED independent_review_required. Input SHA pins were generated for this diagnostic only, not independent attestations.

Recovered original organization prewrite/confirmed journal pair for printed pp96,98,102/PDF97,99,103. Archive CRCs passed; five overlapping retained prewrite members exactly match, original archived plan and confirm equal actual protected gate prepare/confirm results, semantic candidate and original indexed manifest bytes equal historical Git. Historical semantic `0939e64ef4b03e89a6884fbdf624de9df55711d7` / `e8aafd586be4bfd8b596dfffa494fda06f207625`; index `5a7c47436b5cae46a85c3c08fee2a43bbb5c000e` / `f98c2dc0fbb3d5b8eb3b0f91ed1de691d6df0a0f`; exact prior manifest blob `91243b85a23a87e091584a7168c11f557581cb88`; pointer /organizations_embedded_mechanics_reconciliation_2026_11_27/verified_semantic_records/0. Actual transition and original receipt/snapshot verifier returned consistent_original_index_artifacts with target-matrix-index-receipt/v1. Original index receipt SHA256 `15db89148f86f014547ad6060d1549de91eae18ac9f412428f3fb4b35df2cdbd`; snapshot SHA256 `1c9cf3f91b2dcb26c267e4f560fddc5138769dc7c4c41c713e4b5e2be2c62441`. New isolated receipt adapter commit `c3a2cce07945679704e1fee53e300b6b2a0a2c91` / `6dce081b6db2b184b008997232ffb57e6ef9b281`; regression commit `2838a53d3ed3a2e76d388a9c607fb3d6bb030c6d` / `e05fc893d31a6d7083ddf6dcb8154dc25a21e11f`. 14 focused tests passed, actual contract checks run 46117623536 succeeded. Full local suite timed out; no local full-suite pass claimed. No synthetic test used as production evidence.

The historical organization pair is not the current corrected DDS successor. Current registered semantic `54f3047ce7425f356dc04edbf43028a7289acefb` / `e1e6aba9e70b2b4806cab79ec3bf0d4ae4988683`, index `953de3d30f58245cf72b92c1eaa6043a70f60e96`, pointer /organizations_procedure_correction_2026_11_27/verified_semantic_records/0; prior blob matches recovered earlier transaction, but successor original archives were not retrieved in bounded lookup. Coordinator/source owner: supply the retained original DDS prewrite and confirmed archives, grid baseline/candidate/plan/confirm/editorial/index receipt/snapshot, independent custody and reviewed source-wide 138-page original obligation inventory. Existing source-owner dossier remains authoritative for scope routing; no new queue, independent chronology or formal book decision fabricated. New mechanical fields 0, new source-image coverage 0, authentic historical transaction pairs reconciled 1, independently accepted books 0, global pages 0. Protected files unchanged.
