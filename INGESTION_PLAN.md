# Corpus ingestion plan

## Objective

Normalize every relevant book in the Drive corpus into concept-centric records while preserving:
- every source contribution,
- page provenance,
- explicit additions/clarifications/exceptions,
- optional-rule status,
- explicit replacements/supersessions,
- conversion rules,
- the currently effective SR3 treatment.

## Precedence rule

Ingestion order never determines mechanical precedence.

A later-ingested older book cannot become current simply because it was processed later. Current state changes only when the source evidence establishes:
1. errata/correction,
2. explicit replacement or supersession,
3. explicit SR3 conversion/update,
4. otherwise the contribution is an extension, clarification, option, modifier, exception, example, or reference.

Unresolved contradictions remain marked ambiguous.

## Pass order

### Pass A - SR3 baseline and primary rules
- FASA7001 Shadowrun Third Edition
- FASA7905a Shadowrun Companion
- FASA7126 Man & Machine
- FASA7907 Magic in the Shadows
- FASA7908 Cannon Companion
- FASA7909 Matrix
- FASA7910 Rigger 3
- FASA7002 Critters
- FASA7003 Quick Start Rules
- GM screen / official character sheets as reference verification only

### Pass B - late SR3/FanPro mechanical expansions
- State of the Art 2063
- Year of the Comet
- Target: Awakened Lands
- Threats 2
- Target: Wastelands
- Shadows of North America
- New Seattle
- Dragons of the Sixth World
- Sprawl Survival Guide
- other FanPro-era books in the corpus

### Pass C - legacy mechanical sources
Processed as historical/provenance sources unless an SR3 book explicitly carries their material forward:
- Rigger 2
- Virtual Realities 2.0
- Grimoire 2E
- Shadowtech
- Cybertechnology
- Awakenings
- Rigger Black Book
- Street Samurai Catalog
- Fields of Fire
- Paranormal Animals volumes
- other pre-SR3 mechanical books

### Pass D - setting/sourcebooks
Ingest world records and any mechanics they introduce:
- Seattle / New Seattle
- regional and national sourcebooks
- corporate / underworld / security books
- Target books
- Threats books
- cultural/economic/media sourcebooks

### Pass E - adventures and campaigns
Ingest:
- canonical people/places/events,
- unique entities,
- adventure-specific mechanics only when reusable or explicitly rules-bearing,
- chronology/world-state consequences.

Adventure prose itself is not reproduced.

## Per-source completion checklist

A source is complete only when:
- its table of contents/domains have been mapped,
- every mechanical addition has a canonical record or relationship,
- explicit replacements/supersessions are represented in lineage,
- optional rules are marked optional,
- all references to older rules are classified,
- new entities/options/modifiers are represented,
- world records have been routed separately,
- ambiguous conflicts remain explicit,
- the source manifest is marked complete,
- the ingestion ledger is updated.

## Query surfaces

- `sources/catalog.yml` - complete Drive inventory
- `sources/manifests/` - normalized source metadata and coverage
- `indexes/rule-lineage.yml` - current/effective rule lookup plus history
- canonical record trees - full normalized data
