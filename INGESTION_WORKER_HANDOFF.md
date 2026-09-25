# Ingestion worker handoff — efficiency and thread rollover protocol

## Purpose

This document is the operational handoff for the active Shadowrun 3E ingestion worker.

Repository:
`DoofWizard/Shadowrun-3E-Preservation-Project`

The goal is to finish the Drive corpus efficiently without repeatedly rereading source material, wasting context on settled decisions, or allowing a long-running chat thread to become the project state.

## Core principle

**Read expensive source material once whenever possible; convert that read into durable structured state in GitHub.**

Conversation context is temporary working memory. GitHub is the durable project memory.

Do not repeatedly reopen previously audited page ranges merely to recover context. Revisit source imagery/text only when a new contradiction, ambiguity, provenance question, or validation failure actually requires it.

## Scan-depth model

Do not treat all sources equally.

### Deep scan
Use for primary SR3 mechanical sources:
- FASA7001 Shadowrun Third Edition
- FASA7905a Shadowrun Companion
- FASA7126 Man & Machine
- FASA7907 Magic in the Shadows
- FASA7908 Cannon Companion
- FASA7909 Matrix
- FASA7910 Rigger 3
- FASA7002 Critters
- FASA7003 Quick Start Rules where mechanically useful

Capture rules, entities, modifiers, options, exceptions, tables, lineage, conversions, and provenance in detail.

### Directed scan
Use for late-SR3/FanPro expansions and legacy mechanical books.

Primary questions:
- Does this add a mechanic not represented yet?
- Does it explicitly replace, convert, extend, clarify, or conflict with an existing mechanic?
- Is a historical version needed for lineage?
- Does it introduce reusable entities/options/modifiers?

Do not exhaustively reproduce prose that does not contribute to those questions.

### Sparse scan
Use for setting books, adventures, campaigns, reference aids, sheets, and similar material.

Extract only:
- canonical people/organizations/places
- chronology/world-state consequences
- unique creatures/equipment
- reusable or explicitly rules-bearing mechanics
- meaningful mechanical/world provenance

Ordinary narrative prose is intentionally skipped.

## Per-source workflow

Use this funnel:

1. **Route the source**
   - map table of contents / meaningful page ranges
   - classify ranges by domain and expected extraction type

2. **Scan sequentially**
   - avoid random page hopping unless resolving a concrete reference

3. **Create durable candidate facts**
   Keep compact provenance-bearing data:
   - source ID
   - printed page
   - PDF page if useful/known
   - domain
   - candidate concept ID
   - type: rule/entity/modifier/option/world/reference
   - relationship: new/extends/replaces/converts/clarifies/conflicts
   - concise evidence/summary
   - confidence or unresolved flag

4. **Normalize**
   - map candidates into canonical records
   - reuse existing canonical IDs instead of restating concepts in natural language
   - keep source contribution separate from current/effective rule

5. **Reconcile only when justified**
   - explicit errata/correction
   - explicit replacement/supersession
   - explicit SR3 conversion/update
   - otherwise classify as extension, clarification, option, modifier, exception, example, reference, or unresolved ambiguity

6. **Validate**
   - IDs
   - schema/YAML
   - references
   - page provenance
   - duplicate concepts
   - lineage links

7. **Commit a bounded slice**
   - difficult mechanical books: roughly 15–30 printed pages or a coherent semantic section
   - sparse books: chapter or whole source when appropriate
   - prefer semantic boundaries over arbitrary page counts

8. **Checkpoint and continue**
   - update durable resume state
   - do not ask for permission between ordinary bounded slices unless a true decision/blocker requires user input

## Ambiguity policy

Do not spend excessive reasoning budget trying to solve a conflict before all relevant evidence exists.

When evidence is insufficient:
- record the ambiguity
- identify the competing source/concept IDs
- state the unresolved question concisely
- continue ingestion

Resolve ambiguities in a later reconciliation pass when additional evidence exists.

**Extraction first; resolution only when justified.**

## Canonical IDs are the compression layer

As ingestion progresses, use canonical IDs and lineage records as shorthand.

Prefer:
`rule.foo — M&M extends; VR2 historical; SR3 baseline`

over repeatedly carrying paragraphs of prior conversational explanation.

If later sources require more and more old context instead of less, the normalization layer is failing and should be repaired.

## Source/status authority

Use these responsibilities consistently:

- `sources/catalog.yml`: what sources exist in the corpus
- `sources/manifests/*.yml`: authoritative per-source ingestion/completion state
- canonical records + indexes: normalized durable knowledge and lineage
- worker checkpoint: current execution/resume position

Do not trust `catalog.yml` alone for completion status when a source manifest exists.

Known example:
- `sources/manifests/M&M.yml` currently says **complete**
- the catalog still says **queued**

The manifest is authoritative for that source until catalog synchronization is fixed.

## Current known milestone

`Man & Machine: Cyberware` (FASA7126) is complete through printed page 160 according to its manifest.

Do not restart or re-audit M&M wholesale. Reopen only targeted evidence if later reconciliation requires it.

## Thread/context rollover policy

Do **not** make one conversation carry the entire corpus.

The repository is the continuous state; a chat thread is only a temporary worker.

Continue using the current thread while it:
- remembers the active source/page reliably
- does not reread completed material unnecessarily
- maintains coherent IDs and GitHub writes
- distinguishes old checkpoints from current state
- remains responsive and consistent

Prepare a successor handoff when any of these occur:
- active page/resume point is lost more than once
- stale checkpoint is treated as current
- completed material is repeatedly reloaded without cause
- duplicate concepts begin appearing
- old versions of decisions create hesitation/confusion
- tool interaction or reasoning becomes noticeably sluggish
- a major pass boundary is reached and a clean reset is cheaper

Natural rollover opportunities:
- end of Pass A
- end of Pass B
- end of Pass C
- before/after large setting/adventure batches

Do not wait for catastrophic context degradation.

## Successor-thread handoff format

Before retiring a worker thread, commit/validate the current bounded slice and leave a compact handoff containing:

```yaml
phase: <pass_a|pass_b|pass_c|pass_d|pass_e>
active_source: <source.id>
source_status: <ingesting|complete>

completed_through:
  printed_page: <n>
  pdf_page: <n|null>

resume_at:
  printed_page: <n>

last_commit: <sha>

open_conflicts:
  - <id>

next_sources:
  - <source.id>

instructions:
  - scan sequentially
  - preserve provenance
  - do not infer supersession
  - reuse canonical IDs
  - commit bounded completed slices
  - continue automatically
```

A successor should be able to continue from repository state plus this compact checkpoint without receiving the entire predecessor conversation.

## Efficiency target

The previous 47–91 hour estimate should be treated as a **ceiling/range, not a goal**.

The process should become cheaper per source as the canonical vocabulary grows.

Working budget:
- primary SR3 mechanics: up to ~25h
- late SR3/FanPro: ~15h
- legacy mechanics: ~18h
- setting/sourcebooks: ~13h
- adventures/campaigns: ~10h
- reconciliation/validation: ~7h
- rescans/problems: ~3h

Return unused time whenever a source can be classified or scanned faster.

A reasonable optimization target is closer to ~55–70 effective agent-hours if the compression/scan-depth strategy works as intended.

## Progress reporting

Do not measure progress only as “books completed.”

Track:
- sources triaged
- sources mechanically scanned
- sources complete
- canonical records committed
- unresolved conflicts
- active source + resume page

A dense 160-page rules supplement and a GM screen must not count as equivalent units of work.

## Immediate operational direction

Continue the active ingestion rather than stopping to redesign the repository.

Adopt this workflow incrementally:
1. preserve the current active source/resume point
2. stop unnecessary rereads
3. use bounded semantic commits
4. defer unresolved conflicts explicitly
5. keep manifests authoritative
6. establish/update a compact worker checkpoint
7. roll into a fresh conversation when context quality begins declining

The objective is that each expensive source read becomes durable structured knowledge that no later worker has to pay to rediscover.
