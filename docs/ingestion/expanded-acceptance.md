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
