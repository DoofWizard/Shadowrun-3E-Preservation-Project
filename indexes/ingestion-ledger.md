# Corpus ingestion ledger

This file tracks corpus-level ingestion progress. It is not a source of game rules.

## Status values

- `queued`
- `structural_scan`
- `ingesting`
- `complete`
- `needs_review`

## Processing policy

Books are analyzed for:
1. new canonical records,
2. extensions to existing records,
3. explicit replacements or supersessions,
4. conversion/update instructions,
5. optional rules,
6. cross-book references,
7. source/page provenance.

A later publication is never assumed to overwrite an earlier rule solely because it is newer.

## Current priority pass

| Source | Status | Current scope |
| --- | --- | --- |
| SR3 Core (FASA7001) | ingesting | Core concepts + chargen + Skills + Combat + Vehicles/Drones + core Magic baseline complete; Matrix next |
| Shadowrun Companion (FASA7905a) | ingesting | Alternate chargen, optional training, Karma options begun |
| Matrix (FASA7909) | ingesting | Source lineage, SOTA, construction, programming/options begun |
| Man & Machine (FASA7126) | ingesting | Detailed ingest underway: cyberware/grades, cybermancy, bioware, nanotech, chemistry/drugs, stress/healing, surgery; equipment/entity coverage and completeness audit remain |
| Magic in the Shadows (FASA7907) | structural_scan | TOC/domain map complete; detailed ingest next |
| Cannon Companion (FASA7908) | structural_scan | TOC/domain map complete; detailed ingest next |
| Rigger 3 (FASA7910) | structural_scan | TOC/domain map complete; detailed ingest next |

## Corpus inventory

The complete 97-item Drive inventory is stored in `sources/catalog.yml`. Every item remains in the queue until it is marked complete here or in its source manifest.

## Completion rule

A source is not marked `complete` until:
- all mechanical additions have canonical records or explicit links to existing records,
- all explicit replacements/supersessions/conversions have lineage entries,
- optional rules are marked optional,
- world-only material has been routed to world records where appropriate,
- ambiguous conflicts are preserved rather than silently reconciled,
- source/page provenance is present.
