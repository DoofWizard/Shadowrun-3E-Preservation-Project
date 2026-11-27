# Shadowrun 3E Preservation Project

This repository is being organized as a concept-centric, cross-source reference for Shadowrun Third Edition.

## Current phase

**Pass B ingestion is underway.** This is a preservation archive for the **fictional Shadowrun tabletop role-playing game**, not a dossier about real people or instructions for real-world activity. The authoritative completion boundary comes only from each active `sources/manifests/*.yml` file, mirrored in `WORKER_CHECKPOINT.yml`; a locally staged candidate, accepted standalone record, catalog status, or recovery archive alone does not authorize printed pages.

*Prime Runners* (FASA Corporation, FASA7116, 1994) is a **historical Shadowrun Second Edition** source; preserve that edition's original printed/PDF pages and mechanics without silently converting anything to Third Edition.

## Forward-only ingestion v2 (2026-11-27)

For remaining open mechanical scopes, all existing workers follow [the forward-only ingestion v2 operating contract](docs/ingestion/forward-ingestion-v2.md): source-authenticated reusable layout preparation, selective difficult-page escalation, natural-section batching and measured throughput. Closed sources and previously reconciled scopes remain closed; no historical re-audit is authorized merely by this process change. All existing source, editorial, individual transaction and acceptance gates remain binding. Denver's owner-authorized archived losses are nonblocking, with no page credit.

## Fictional-source editorial contract

Before the first semantic submission, the source reviewer must identify the actual published game, publisher, title, catalog number, edition, and printed/PDF pages in the record's permitted root headline/summary **and in the ordinary commit description**. Review every human-readable narrative field, including nested `data`, in neutral source-attributed prose distinguishing publisher narration, fictional in-world testimony, and optional GM scenarios. A `framing: newsroom_neutral` label is not proof that this has happened.

Keep every source fact and game rule intact: identities, chronology, coercion/consent, negation, attribution, rumors versus established events, dice, modifiers, damage, costs, stats, and exceptions. Contextual explanation is not license to erase or euphemize substantive information. Use the independently reviewed baseline, immutable candidate, actual staging/preflight, ordinary GitHub contents write/readback, confirmation gate, and source-manifest-then-checkpoint authorization sequence.

An ambiguous "blocked by OpenAI's safety checks" response does not identify an offending phrase or prove GitHub's HTTP status. Follow [the fictional-source diagnostic playbook](docs/ingestion/fictional-source-context-rejection-playbook.md) without replaying identical refused bytes, disguising content, bypassing gates, or disabling the hourly worker while Pass B is incomplete.

## Design principles

- Organize by game concept, not sourcebook chapter order.
- Give every meaningful record a stable ID independent of its file path.
- Separate entities, rules, procedures, options, modifiers, subsystems, and world facts.
- Track provenance at the record level.
- Let later books extend, clarify, modify, except, replace, convert, or supersede existing records without duplication.
- Keep source manifests separate from canonical game records.
- Preserve edition/source compatibility information explicitly.

See `schema/` for the record model and `templates/` for canonical record templates.
