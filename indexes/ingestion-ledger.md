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
| Man & Machine (FASA7126) | complete | Mechanical audit complete through printed p.160: cyberware/cyberlimbs, cybermancy, bioware, nanotech, chemistry/drugs, Stress/healing, surgery/medical rules, catalogs and lineage |
| Magic in the Shadows (FASA7907) | complete | Deep mechanical audit complete through printed p.170; pp.171-178 checked as reference/end matter |
| Cannon Companion (FASA7908) | ingesting | Detailed sequential ingest begins next |
| Rigger 3 (FASA7910) | structural_scan | TOC/domain map complete; detailed ingest next |

## Completed Bug City source

| Source | Status | Verified scope |
| --- | --- | --- |
| Bug City (FASA7117) | complete | Sequential coverage through printed p.160/PDF169; game information through p.151, illustration p.152, index pp.153-160. Historical Second Edition mechanics retain source provenance and explicit relationships without inferred SR3 supersession. Manifest and checkpoint agree, with no pending normalization. |

Completion verified on 2026-10-11: [manifest commit](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/34a6719befed317ba0c803ebf4d9334dad42d006), [checkpoint commit](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/3bc992688e9d64ffaa80f9e1e6df41e9425fe70c). The final recovery session advanced from printed p.137/PDF146 through p.160/PDF169 in five fully reconciled slices, adding 19 source-reviewed, gate-confirmed records. The former p.138 write rejection did not recur in this session; its historical root cause remains unconfirmed. Recovery sidecars were retained with retirement evidence.

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
