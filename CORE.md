# Shadowrun Third Edition — Core

**The accepted FASA7001 rules/data package is delivered. Final core-completeness acceptance remains unresolved.**

Publication: FASA Corporation, Shadowrun, Third Edition, FASA7001. Original per-record printed/PDF provenance is retained.

## Open the core

[Canonical core entrypoint](docs/engine-readiness/CANONICAL_RULES_DIGEST_ENTRYPOINT_2026-11-10.json)

The entrypoint contains all **447 accepted, source-registered core records**: **409 protected mechanical records** and **38 associated guidance/context records**, organized through the original **15-section core ledger**. Each record links to its existing canonical path and carries its source range, content class, accepted commit, Git blob and SHA-256.

The earlier four-record November 10 digest is superseded by this entrypoint for all currently registered core records; its previous bytes remain in Git history. No canonical rule was rewritten for this delivery. Packaging all registered records does not by itself establish that every required original rule field is represented.

## Scope and evidence

- Accepted source snapshot: 5fa5713b684a277ebb13a9d259d8246c80f4c3f0.
- [Available-source consolidation receipt](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/94606db683acfc2574ccd5aecc478886688548e5).
- [Authoritative source manifest](sources/manifests/SR3.yml), blob c5f0b833cec300cc385a8ded353301e723f3b2f0.
- [Original-source chapter/field evidence and accepted closeout](docs/engine-readiness/FASA7001_CORE_RULES_CLOSURE_QUEUE_2026-11-11.yml), blob 25f26c0e532d2554654155c55fef32e12a7c867a.
- Original PDF SHA-256: 7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914.

All 447 original record byte hashes and IDs were checked during assembly. The existing original-source reviews and gate receipts provide the source evidence. The delivery creates zero new semantic records and zero authorized printed-page credit.

## Coverage

The core includes tests and dice; character creation and sample archetypes; skills; initiative/actions/combat/damage/healing; vehicles and drones; magic, spirits, spells and foci; Matrix rules; shadowrunning, lifestyle and security; Karma, advancement and hazards; contacts; spirits and dragons; gear, cyberware and market tables; sourcebook conversion; and sample character sheets. Associated source context remains labeled separately.

## Accepted limitations

Printed p308 remains an owner-accepted nonblocking scan omission. The current record mapping is p307/PDF316 then p309/PDF317; no absent content is invented. Preserve original internal rule discrepancies and edition/optional-rule distinctions as recorded.

## Final acceptance status — corrected November 21, 2026

The [core closure ledger](docs/engine-readiness/FASA7001_CORE_RULES_CLOSURE_QUEUE_2026-11-11.yml) records a scoped available-source mechanical closeout, while its completion block still records:

- `available_source_mechanics_scoped_consolidated: true`
- `complete_core_rule_normalization: false`
- `completeness_gate_passed: false`
- `numeric_table_inventory_fully_verified: false`

The source manifest also retains `scan_complete_normalization_pending`. The scoped closeout reports no demonstrated remaining available-source mechanical field gap in its reviewed ranges, but expressly limits what the reused bounded receipts establish. Those facts support the delivered package; they do not resolve the final core-completeness acceptance conditions.

The earlier unqualified completion statement was too broad. Reconcile the existing original-heading, numeric-field and content-class receipts into one explicit available-source core acceptance result. Reuse unchanged accepted evidence; inspect original source again only for a specifically uncovered or conflicting field. Do not invent new missing mechanics, repeat closed chapter audits, or mark the false completion fields true without supporting evidence and the applicable authorization. Record the owner's nonblocking scan-omission policy, without crediting unseen pages.

The same hourly worker must prioritize this outstanding core acceptance work before further unrelated supplement transcription. Existing supplement commits remain valid separate Pass B work. Full game-engine implementation and exhaustive narrative archiving remain separate scopes; neither is added as a prerequisite for the core rules/data deliverable.

## Export or load the core

Use the offline package core.json for a single JSON document containing all 447 accepted record objects. INDEX.json supplies provenance, chapter navigation and hashes; the original YAML files retain their repository paths.

From a repository checkout, reproduce the package with:

    python tools/engine_readiness/export_core_package.py --output dist/Shadowrun3E_Core.zip

The exporter requires Python and PyYAML, reads the pinned canonical files, and produces core.json, the original files, the index, source receipts and SHA256SUMS. It performs no network requests, source extraction or rule interpretation.
