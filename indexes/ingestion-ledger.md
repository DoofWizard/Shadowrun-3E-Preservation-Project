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

## Full-rules consolidation — live source-shard reconciliation (2026-11-23)

**Milestone:** The available-original FASA7001 mechanics/data core is formally accepted:
15/15 core sections; 451 canonical records (413 protected mechanical + 38 guidance).
The accepted `sources/manifests/SR3.yml` blob is
`b0ebffa4985ab544e64857b99e98b17d69ee3184`.
This **does not** certify all expanded rules, narrative archiving, or a runnable
game engine. FASA7001 printed p308 remains unobserved/nonblocking.

**Current all-expanded-rules verdict: NOT ACCEPTED.** Source-manifest
`status: complete`, the number of accepted records, scanned pages, or individual
closed sections does **not** establish complete original-source mechanical scope.
No independently executed final all-expanded-rules acceptance receipt is
recorded here. Existing individual source gate receipts must be reused, never
retrospectively invented.

**Live corpus catalog:** `sources/catalog.yml` has **104 entries**:
10 primary rules, 15 legacy rules/source, 10 mixed, 33 sourcebook-mixed,
32 adventure/campaign, and 4 reference aids. These are corpus *roles*, not
104 proven distinct rules-bearing books; mixed and adventure publications
must still be checked for unique mechanics. Historical 97/105 estimates
must not be used as the current count.

### Ten exclusive rules-first source shards

| Source / sole source owner | Source evidence already usable | Next independent rules-completeness obligation |
| --- | --- | --- |
| **FASA7001 core** (accepted/read-only) | 451 accepted records, 15/15 scoped sections, final source acceptance | Do not reopen; compare expansions against accepted core without duplication |
| **FanPro10662 Rigger 3 Revised** (coordinator) | Live `sources/manifests/Rigger3Revised.yml`; Power Plant appendix pp194–201 source-locally reconciled, reported 50 verified registrations | Chassis pp202–205 and remaining whole-book mechanical scope; keep FASA7910 a separate historical edition |
| **FASA7907 Magic in the Shadows** (Magic owner) | Live `sources/manifests/MitS.yml`, verified Centering/Cleansing and other supplemental transactions | Original-TOC field-level closure of remaining modifiers/tables, including historical mechanical discrepancies |
| **FASA7126 Man & Machine** (Augmentation owner) | Live `sources/manifests/M&M.yml`, verified bioware/implant corrections; source status 'complete' only archival | Reconcile unresolved bioware overlap, Stress and healing conditions, deferred transaction receipts, and whole-book closure |
| **FASA7908 Cannon Companion** (Combat owner) | Live `sources/manifests/CannonCompanion.yml`, BattleTac, parachutes and underwater equipment source-local work | Underwater Activity pp107–112 corrections need actual verify-source + full transaction confirmation; remaining combat/equipment section audit |
| **FASA7905a Shadowrun Companion** (Character owner) | Live `sources/manifests/SRComp.yml`, point-based chargen pp13–15 and Enemies pp68–72 scoped closed; Contacts corrections confirmed | Special Contacts, New Contacts and historical gate conflicts; all-book original mechanic checklist |
| **FASA7909 Matrix / FASA7219 Target Matrix** (Matrix owner) | Live `Matrix.yml` and `TargetMatrix.yml`, Matrix Skills pp24–26 and Programming pp76–94 independently scoped closed | Remaining Matrix-user exceptions and Target Matrix Host Rules/eligibility coverage; no duplicate Programming |
| **FanPro10664 SOTA2063 / FanPro25004 SOTA2064** (SOTA owner) | Live `StateOfTheArt2063.yml` has five closed Game Information scopes; `StateOfTheArt2064.yml` has adept, Old World Magic, and Games of State equipment scoped closeouts | Directed original mechanics outside these ranges; qualitative Behind the Badge rules, section-wide original TOC acceptance |
| **FASA7109 ShadowBeat + unassigned unsuperseded 2E** (Legacy owner) | Live `ShadowBeat.yml`, 23 previously confirmed registrations; sports pp58–73 scoped closed | Simsense pp74–83, media and equipment, with per-mechanic SR3 supersession proof; keep original 2E mechanics unconverted |
| **FASA7002 Critters; FanPro10667 SSG; FanPro10650 Year of Comet; FanPro10666 Dragons; FanPro10653 Target Wastelands** (Critters owner) | Live `Critters.yml`: 53 original powers pp7–14 source-locally closed; SSG pp118–126 prior scoped closure | Weaknesses pp14–15, mutant/toxic pp15–17, creatures pp20–48 and all four other books' unique mechanics |
| **FASA7118 Corporate Security Handbook; FASA7115 Lone Star; FASA7215 Smuggler Havens; FASA7124 Cyberpirates; FanPro10657 New Seattle; other unassigned SR3 mixed books** (Sourcebook owner) | Live `CorporateSecurityHandbook.yml` retains accepted source-specific security corrections; other source manifests have historical registrations | Corporate Security original pp34–61 gate debt, security personnel and original NPC pp106–124, Lone Star missing p4, then novel mechanics across other owned books |

This matrix records **evidence-backed areas of progress and exact near-term
obligations**, not a declaration that each full source's TOC/field matrix is
already exhaustive. Sources not individually named must still be assigned
only within the ten existing exclusive source ownership contracts; do not
create another worker or edit another worker's manifests.

### Acceptance distinctions and immutable guards

1. **Verified source acquisition:** Fresh cataloged original PDF bytes match the
   source-specific live SHA-256; execute actual `preservation_method.py verify-source`.
   Hash matching alone never proves that a mechanic/section was examined.
2. **Original review:** Inspect original printed/PDF page images; account for
   every unique game-affecting rule, number, option, exception, conditional
   interaction, statblock and table cell. Preserve paper-original ambiguities.
3. **Semantic acceptance:** Independently review original BASELINE and
   same-substance CANDIDATE, run actual stage/prepare, normal GitHub Contents
   write, exact-byte/blob/commit readback, actual confirm and legitimate
   source-specific manifest indexing. A staged draft is not accepted.
4. **Section and book closure:** Use a finite original-TOC-derived per-field
   checklist and verified receipts. Do not promote `status: complete`
   merely because a historical sequential archive pass finished.
5. **Final expanded-rules acceptance:** A distinct corpus-wide gate must
   demonstrate all available applicable original rules-bearing sources are
   individually source-closed, with explicit legacy 2E supersession/adapter
   uncertainties or documented local omissions, before declaring the
   all-expanded-rules milestone. This is **not** the existing FASA7001 core gate.
6. **Global checkpoint:** `WORKER_CHECKPOINT.yml` remains active at
   **Denver FASA7212 completed printed p45 / PDF46; resume p46/PDF47**.
   Printed pp46–47 are archived source gaps. All out-of-order specialist
   source receipts give **zero globally contiguous page credit**.
   Lone Star printed p4 remains a separate deferred manual obligation.
7. **Workers / concurrency:** Exactly ten existing enabled hourly tasks, one
   coordinator plus nine exclusive specialists. One source owner writes
   each source-specific manifest/record. No automatic spawning or cadence
   changes. The separate draft-runner code does not count as source
   acceptance or an already-running persistent host.

**Next coordinator action:** Reconcile the latest individual original-source
section audits and gate receipts into field-level source/book closure, resolve
Rigger chassis from its owner, and keep this single ledger current; never
substitute an additive record-count percentage for verified all-rule scope.

## Completed Bug City source

| Source | Status | Verified scope |
| --- | --- | --- |
| Bug City (FASA7117) | complete | Sequential coverage through printed p.160/PDF169; game information through p.151, illustration p.152, index pp.153-160. Historical Second Edition mechanics retain source provenance and explicit relationships without inferred SR3 supersession. Manifest and checkpoint agree, with no pending normalization. |

Completion verified on 2026-10-11: [manifest commit](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/34a6719befed317ba0c803ebf4d9334dad42d006), [checkpoint commit](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/3bc992688e9d64ffaa80f9e1e6df41e9425fe70c). The final recovery session advanced from printed p.137/PDF146 through p.160/PDF169 in five fully reconciled slices, adding 19 source-reviewed, gate-confirmed records. The former p.138 write rejection did not recur in this session; its historical root cause remains unconfirmed. Recovery sidecars were retained with retirement evidence.

## Corpus inventory

The current 104-entry Drive inventory is stored in `sources/catalog.yml`. Every item remains in the queue until it is marked complete here or in its source manifest.

## Completion rule

A source is not marked `complete` until:
- all mechanical additions have canonical records or explicit links to existing records,
- all explicit replacements/supersessions/conversions have lineage entries,
- optional rules are marked optional,
- world-only material has been routed to world records where appropriate,
- ambiguous conflicts are preserved rather than silently reconciled,
- source/page provenance is present.
