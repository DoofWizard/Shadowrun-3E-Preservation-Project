# Pass B thread handoff — 2026-09-26

## Resume authority

Always read these first:
1. `INGESTION_WORKER_HANDOFF.md`
2. `WORKER_CHECKPOINT.yml`

The checkpoint is authoritative over chat summaries.

## Current durable state

```yaml
phase: pass_b
active_source: source.fanpro-10666
source_status: ingesting

completed_through:
  printed_page: 45
  pdf_page: 47

resume_at:
  printed_page: 46
  pdf_page: 48

last_commit: 0e2c3c4f4f3a8d6e8fbc4df1b9990c1c15e84457
```

Current source:
**FanPro10666 — Dragons of the Sixth World**

Completed:
- pp. 7–23: opening dragon biology/culture/magic overview scanned
- pp. 24–34: Draco Foundation chapter scanned
- pp. 35–45: Aden profile scanned and durably normalized

Resume:
- printed p. 46 / PDF p. 48
- next profile: **Celedyr**

## Open pending normalization items

- `pending.dragons.draco-foundation-p24-34`
- `pending.dragons.range-7-23`
- `pending.ssg.game-info-p118-126`
- `pending.ssg.detailed-lifestyles-p127-144`

These were not lost. They were fully scanned but richer GitHub payloads hit connector safety filters. Preserve them as pending until a compact/safe normalization route is available.

## Pass B source order

After Dragons of the Sixth World:
1. source.fanpro-10664 — State of the Art 2063
2. source.fanpro-10657 — New Seattle
3. source.fanpro-10655 — Shadows of North America
4. source.fanpro-10653 — Target: Wastelands
5. source.fanpro-10652 — Threats 2
6. source.fanpro-10651 — Target: Awakened Lands
7. source.fanpro-10650 — Year of the Comet
8. source.fanpro-10654 — Wake of the Comet
9. source.fanpro-10665 — Survival of the Fittest
10. source.fasa-7219 — Target: Matrix
11. source.fasa-7125 — Corporate Download
12. source.fasa-7124 — Cyberpirates
13. source.fasa-7123 — Underworld Sourcebook
14. source.fasa-7122 — Portfolio of a Dragon
15. source.fasa-7121 — Threats
16. source.fasa-7118 — Corporate Security Handbook
17. source.fasa-7117 — Bug City
18. source.fasa-7116 — Prime Runners
19. source.fasa-7115 — Lone Star
20. source.fasa-7215 — Target: Smuggler Havens
21. source.fasa-7214 — Target: UCAS
22. source.fasa-7213 — Aztlan
23. source.fasa-7212 — Denver
24. source.fasa-7211 — Tir na nÓg
25. source.fasa-7210 — Tir Tairngire
26. source.fasa-7209 — California Free State

Then proceed through SR3-era adventures/campaigns.
Legacy SR1/SR2 lineage is Pass C.

## Operating rules

- scan sequentially
- use directed scan depth for late-SR3/FanPro books
- preserve source/page provenance
- reuse canonical IDs
- do not infer supersession
- commit bounded semantic slices
- continue automatically between ordinary slices
- reference aids are deferred unless needed for discrepancy checking
- if a rich payload triggers the connector filter, preserve page-level progress and mark the detail range pending rather than stalling
- do not restart completed source scans

## Connector-filter note

The GitHub connector has intermittently rejected richer fictional payloads, especially dense game-mechanical or organization/identity detail. This is a connector filtering issue, not a determination that the fiction is real.

Working fallback:
1. preserve verified scan boundary in the source manifest
2. advance `WORKER_CHECKPOINT.yml`
3. add a concise pending normalization ID
4. continue sequentially

## Fresh-thread starter prompt

> Continue the Shadowrun 3E ingestion worker from DoofWizard/Shadowrun-3E-Preservation-Project. Read INGESTION_WORKER_HANDOFF.md, PASS_B_THREAD_HANDOFF_2026-09-26.md, and WORKER_CHECKPOINT.yml first. Resume from the exact durable checkpoint and continue automatically. Preserve provenance, reuse canonical IDs, do not infer supersession, commit bounded semantic slices, update the source manifest and checkpoint after each completed slice, and use the fixed Pass B order in the handoff. For image-only PDFs, use raw page images/OCR as necessary. If a rich fictional payload hits a connector filter, preserve the scan boundary, mark the detail range pending, and continue rather than stalling. Stop only for a true blocker that cannot be resolved from repository/source state.
