# FASA7001 available-source core acceptance

This operation closes the **available original-source game-mechanics** milestone
for FASA Corporation's *Shadowrun, Third Edition*, FASA7001. It is independent of
the active global source checkpoint. Denver's archived pages are not inputs.
It does not authorize printed-page advancement, whole-publication narrative
completion, engine implementation, or a change to the hourly task's schedule.

`tools/ingestion/core_acceptance.py` adds a source-specific acceptance operation;
it does not modify or replace `prepare`, `confirm`, `authorize-advance`, transaction
recovery, the ordinary GitHub Contents write path, or first-pass editorial review.

## Existing evidence is reused

Keep the 447 accepted-record package, existing source reviews and their historical
limits. The final inventory belongs under **`core_acceptance_inventory` in the
existing `FASA7001_CORE_RULES_CLOSURE_QUEUE_2026-11-11.yml`**, not in another queue.

Construct its required fields from the original-heading/field/content-class
reviews already on record. Reuse unchanged evidence. Inspect an original page
again only for a specific missing or conflicting assertion. Never derive the
required-field inventory solely from whichever canonical records happen to exist;
that would conceal an untranscribed field. Do not set a review flag to true without
actually completing the review it describes. Synthetic unit-test fixtures are not
source evidence and must never be copied into the live inventory.

Each `required_fields` item represents a concrete source obligation: an identified
rule, procedure, table row/column group, condition, exception, option, or relevant
GM direction. A table may bind to its complete structured table field when its
review explicitly covers every required row/column and exception. One generic
entry per chapter is not sufficient. No new semantic record is needed when an
accepted record already represents the complete obligation.

The original 15-section ledger covers printed pp36-329. The source-inventory review
must also retain the already reviewed introductory and back-matter dispositions;
nonmechanical fiction, art and blank forms are not new gameplay requirements.

## Inventory contract

Root fields inside `core_acceptance_inventory`:

- `schema_version: sr3-core-obligation-inventory/v1`
- `source: source.sr3-core`
- `source_pdf_sha256`: the authenticated original FASA7001 PDF SHA-256.
- `scope: available_original_mechanics`
- `independently_reviewed_original_headings_fields_and_classes: true` only after that actual review.
- `unresolved_mechanical_fields: []` only when no required available-source field remains unresolved.
- `source_inventory_review`: an exact reference to independently authored source-review evidence.
- `sections`: the 15 sections listed in `core_acceptance.SECTIONS`, once each.
- `bindings`: a mapping keyed by every required-field ID, with no missing or extra IDs.

Each section has `id`, its original inclusive `printed_range`,
`heading_field_content_class_inventory_complete`, `source_review`, and
`required_fields`. Only Seattle may have no required mechanical fields, with its
explicit existing source disposition and `no_independent_game_mechanics: true`.
Other sections require actual fields, including the sample character options.

Each required field has:

- A unique `id` and actual `source_heading`.
- Exactly one `content_class`: `rule_exact`, `rule_procedure`, `equipment_stat`,
  `character_option`, or mechanically relevant `campaign_guidance`.
- `printed_pages` and `pdf_pages` as sorted explicit page lists, not inferred
  global offsets. Ranges are expanded only to pages actually relevant to the field.

Each binding has `record_id`, `record_pointer`, and `source_review`.
`record_pointer` is a JSON Pointer to an existing substantive field under `/data/`
in the indexed record. The binding's content class and printed/PDF provenance must
match the accepted record. Presentation summaries do not satisfy a required field.

A review reference contains `path`, `pointer`, and `value_sha256`. The pointer
identifies the actual independently authored review fragment. Its digest is
`core_acceptance.digest(fragment)`: SHA-256 of UTF-8 JSON with sorted keys,
compact separators, unescaped Unicode, and a final newline. This permits precise
reuse of historical fragments in the existing queue without a self-referential
whole-file hash. A reference into `core_acceptance_inventory` itself is rejected.
Preparation additionally pins the entire current manifest, queue and referenced
review-document Git blobs, so later changes require reconciliation.

The program checks the structure and integrity of the supplied evidence. **It
cannot read the original book or establish the truth/completeness of an inventory
by itself.** The identified independent original-source reviews supply that
evidence; the program must never be reported as their replacement.

## Existing-worker sequence

1. In the existing scheduled invocation, reconcile current main and finish any
   coherent transaction already in progress. Preserve accepted records and
   interleaved changes. Do not start a second run.
2. Complete the finite source-obligation mapping above from existing evidence.
   Resolve genuine new semantic gaps through all normal original-source,
   independent-baseline/candidate, stage/prepare, ordinary Contents write,
   exact-readback, confirm and source-index gates. An unindexed legacy record
   needs legitimate recovery/index evidence, not a manufactured semantic revision.
3. Commit the reviewed inventory within the existing closure queue through an
   ordinary Contents update and verify its exact bytes. Do not yet flip completion
   flags or the whole source status. This inventory write is administrative work.
4. Run the nonmutating assessment:

   ```bash
   python tools/ingestion/core_acceptance.py assess --repo-root .
   ```

5. Freshly acquire the cataloged original Drive PDF under the existing worker
   protocol. Prepare the source-specific receipt:

   ```bash
   python tools/ingestion/core_acceptance.py prepare --repo-root . \
     --fresh-pdf /actual/fresh/FASA7001.pdf --output /actual/work/core-acceptance.json
   ```

   Preparation actually executes the repository's `preservation_method.py
   verify-source`, independently hashes the supplied bytes and checks that core
   inputs did not change during the operation. A hash does not prove fresh Drive
   acquisition or replace original-image review; the caller still performs the
   established source-acquisition protocol.
6. Publish the exact prepared JSON as a source-specific acceptance receipt through
   an ordinary GitHub Contents create/update. Independently read back its complete
   bytes and real commit/blob SHA. Then run:

   ```bash
   python tools/ingestion/core_acceptance.py confirm --repo-root . \
     --plan /actual/work/core-acceptance.json \
     --readback /actual/work/core-acceptance-readback.json \
     --commit ACTUAL_COMMIT_SHA --readback-blob ACTUAL_BLOB_SHA \
     --output /actual/work/core-acceptance-confirmed.json
   ```

   The command re-evaluates current source/record/review inputs and refuses stale
   plans or differing readback bytes. A synthetic commit string in a unit test is
   never a substitute for a real ordinary-write and readback receipt.
7. Only after actual confirmation, record the verified acceptance receipt in the
   source-specific manifest and existing closure ledger through ordinary updates
   with current SHAs and exact readbacks. Preserve unrelated data and historical
   limitations. Reconcile the CORE entrypoint with that verified scoped result.
   Do not claim whole narrative-publication completion, engine execution, a Denver
   transition or printed-page credit. Those authorizations are not returned by
   this operation.

The owner-accepted p308 omission remains visible and nonblocking. A rule cannot be
bound to unseen p308 content, and the omission cannot create scan/page credit.

## Tests and initial live assessment

Run `python -m unittest test_core_acceptance -v` from `tools/ingestion`.
Tests cover missing field bindings, incomplete sections, changed source evidence,
unverified or mismatched records, incorrect provenance/classes, readback/stale
plan failure, rejected source verification, and nonblocking omissions without
fabricated rules or page credit. Tests use synthetic fixtures exclusively.

The first nonmutating assessment of manifest
`c5f0b833cec300cc385a8ded353301e723f3b2f0` and closure queue
`25f26c0e532d2554654155c55fef32e12a7c867a` verified the 447 registered file byte,
identity and class relationships, then correctly reported
`missing_source_reviewed_heading_field_inventory` at `core_acceptance_inventory`.
That result identifies the unfinished acceptance input. It does not assert that
447 records prove source completeness or that a particular new mechanic is missing.
