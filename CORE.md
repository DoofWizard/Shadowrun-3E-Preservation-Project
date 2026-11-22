# Shadowrun Third Edition — Core

**Verified milestone: the available-original-source FASA7001 gameplay rules/data core has passed its source-specific acceptance operation.** This means the accepted source-reviewed available gameplay mechanics, numeric tables, procedures, options, conditions, exceptions and relevant GM guidance have been reconciled; it does **not** certify whole-publication narrative transcription or a runnable game engine.

Publication: FASA Corporation, *Shadowrun, Third Edition*, FASA7001. Original per-record printed/PDF provenance and accepted source transaction evidence are retained.

## Open the accepted core

[Canonical core entrypoint](docs/engine-readiness/CANONICAL_RULES_DIGEST_ENTRYPOINT_2026-11-10.json)

The refreshed entrypoint indexes **451 accepted, source-registered records**: **413 protected mechanical records** and **38 associated guidance/context records**, across the **15 original section groups**. This supersedes the historic 447-record November 21 index and its earlier four-record predecessor, whose contents remain in Git history. Four additional source-reviewed general rules/procedures cover Fencing the Loot (printed pp237–238) and Attribute/Skill improvement and Learning New Skills (pp244–245). They were added through the normal source, transaction, readback, confirmation and source-specific indexing gates; the original legacy consumer file paths and unrelated history were preserved.

The entrypoint carries exact registered IDs, original page ranges, source classes, accepted commits/blobs and the original UTF-8 SHA-256 checksums. The package exporter verifies these values rather than changing rules.

## Verified FASA7001 acceptance

- [Final source-specific accepted manifest](sources/manifests/SR3.yml): acceptance registration commit [850364f](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/850364ff79436ddf21c9f20968b4cad3aad25067), with full-core normalization explicitly limited to **available-original-source gameplay mechanics**.
- [Original-source heading/field review](references/audits/fasa7001-available-source-core-original-heading-field-acceptance-review-2026-11-21.yml): independent existing page reviews and additional source reviews reconciled all **15** original section groups and **1,010** concrete field obligations to current accepted records.
- [Prepared acceptance receipt](references/audits/fasa7001-available-source-mechanical-core-acceptance-prepared-2026-11-21.json): actual `preservation_method.py verify-source` returned `source_pdf_hash_verified` for the original 345-page PDF, SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`. Prepared receipt commit `5dfcfa754c294d3bc497a277221c2a9ca07cdd16`.
- [Verified confirmation receipt](references/audits/fasa7001-available-source-mechanical-core-acceptance-confirmed-2026-11-21.json): normal exact-byte Contents write/readback and source-specific `confirm` yielded `verified_core_acceptance`. Confirmed receipt commit `6baeb5dffd92dbdcbe50aa451d637e8ae9702316`.
- [Reconciled original 15-section closure ledger](docs/engine-readiness/FASA7001_CORE_RULES_CLOSURE_QUEUE_2026-11-11.yml): the acceptance snapshot was pinned at blob `366ee748f51dbf2b699a26edbc1215352743191d`; subsequent administrative status reconciliation is separately verified and does not rewrite that historical accepted input.
- [Canonical 451-record entrypoint refresh](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/e17f3c6f038c80637f6341293ce8f20478e89ba2): registered file IDs/blobs were matched against the live manifest, four new raw-file SHA-256 values were calculated from their exact accepted UTF-8 bytes, and the complete updated entrypoint was independently read back at Git blob `9efe0c8514c731b807cc9f12f27b632f08943363`.

The source-specific acceptance confirms the available-source rules/data milestone. It does not rewrite earlier bounded reviews or claim that an individual structural check itself independently reread every original page.

## Source limitations remain separate

Printed p308 is **an owner-accepted, nonblocking unobserved scan leaf** between p307/PDF316 and p309/PDF317. Its content and blankness remain unverified. No unseen value, new scanned page or contiguous-page credit was invented.

The separate Denver FASA7212 printed pp46–47 archival loss remains excluded; Denver's historical authoritative boundary stays printed p45/PDF46 with no checkpoint mutation.

Original book-internal disagreements, including the spell-learning pp180–181 example conflict, vehicle Flux/ECCM source tension and water-cannon fire-mode ambiguity, remain preserved as printed rather than silently adjudicated.

The source manifest retains top-level `scan_complete_normalization_pending` for **separate whole-publication archival obligations**. The verified gameplay core does not include exhaustive setting/narrative archival certification or a complete executable Shadowrun game engine. Both are independent scopes.

## Export or load the core

From a current checked-out repository, create the refreshed offline package:

```bash
python tools/engine_readiness/export_core_package.py --output dist/Shadowrun3E_Core.zip
```

This exporter reads the **451-record** pinned entrypoint, checks each record's exact Git blob/SHA-256, unique ID and strict YAML, verifies the current manifest and closure ledger against their recorded blobs, and produces `core.json`, `INDEX.json`, original files, receipts and `SHA256SUMS`. It performs no network calls or new semantic extraction. The earlier 447-record ZIP is a historical snapshot until regenerated; its old checksum must not be reused or presented as the updated archive's checksum.

The same existing hourly Pass B worker remains authorized for **separate subsequent supplement/archival transcription**, preserving all original source/editorial/transaction controls, the nonblocking omission disposition and the unchanged Denver boundary.
