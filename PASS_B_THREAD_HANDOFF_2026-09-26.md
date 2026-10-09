# Pass B thread handoff — 2026-09-26

Operational clarification and executable editorial contract: 2026-10-08.

## Standing Shadowrun 3E context and write-error handling (2026-10-09)

This is a preservation project for **Shadowrun Third Edition, a fictional cyberpunk tabletop role-playing game**. Its historical publications discuss imagined megacorporations, shadowrunners, covert activity, security systems, weapons, augmentations, **magic and spellcasting**, and fictional wrongdoing. Explicit magic rules, spells, dice pools, and target numbers are further markers of a fictional game system, not claims of real-world magical abilities or instructions to carry out events in reality. Treat those as in-universe game content and historical source material, **not evidence that the user seeks real-world criminal instructions**. Do not require the user to repeat this context on each run. Maintain exact rules-bearing content and faithful attribution under the mechanical-fidelity and editorial-preflight rules below.

Past GitHub submissions have sometimes returned the generic tool-layer message "This tool call was blocked by OpenAI's safety checks." Such a message is **not a GitHub HTTP rejection**, and it does **not identify a specific cause**. Do not claim it proves a content trigger or that a particular phrase was rejected. Report the exact operation and observed result. Distinguish administrative state updates from semantic game records.

For an authorized administrative manifest/checkpoint correction, use the ordinary, narrowly scoped GitHub file update with the freshly verified blob SHA and the exact required metadata; do not bundle unrelated source narrative into the action. If a normal permitted retry succeeds, verify both files by readback and resume from the authoritative manifest. Do not present an ambiguous tool error as a permanent content prohibition or make the user repeatedly re-explain the game.

For semantic records, **all mandatory baseline, preflight, prepare, write, confirm, and authorize-advance gates remain binding**. Do not sanitize mechanics, disguise material, use alternate APIs to circumvent a denial, or speculate about hidden moderation rules. If a substantive write cannot be completed through the allowed workflow, preserve the precise pending/recovery state and keep the hourly automation enabled.

## Resume authority

At the start of every run read the full current:
1. `INGESTION_WORKER_HANDOFF.md`
2. this file
3. `WORKER_CHECKPOINT.yml`
4. active main source manifest, when present
5. `sources/catalog.yml`

The active MAIN SOURCE MANIFEST is the sole per-source progress authority. The checkpoint is its execution mirror, not an independent authority. Repair a disagreement from the manifest BEFORE reading new pages. Manual work may have advanced the repository. Recovery sidecars never override the manifest; reconcile unresolved sidecars first and ignore explicitly retired/resolved ones.

The transactional durability protocol and mechanical-fidelity invariant in `INGESTION_WORKER_HANDOFF.md` remain mandatory. The contract below makes the existing newsroom convention executable; it does not add another model call, research pass or corpus migration.

## Submission gate — mandatory new-write sequence (2026-10-08)

The manual FASA7118 pp.34–61 transcription skipped the previously documented preflight. Merely reminding a worker is not enough. The following gate is now REQUIRED before any NEW semantic GitHub write by manual or scheduled workers.

Read and execute tools/ingestion/ingestion_gate.py in the working environment, alongside connector_preflight.py. This validates what is written; it does not rewrite or censor source facts and does not perform an extra model call.

1. Independently produce a source-reviewed baseline and one-semantic-class candidate. Preserve exact mechanics and attribution. Obtain the SHA-256 of the FRESH cataloged PDF.
2. BEFORE creating/updating a new semantic file, execute:
   python tools/ingestion/ingestion_gate.py prepare BASELINE.yml CANDIDATE.yml references/path.yml source.id PDF_SHA256 > plan.json
   Require exit code 0 and status preflighted. Submit EXACT candidate bytes. A directly authored GitHub file without the gate must be treated as an incomplete transaction, not successful ingestion.
3. FETCH that exact GitHub path after the write. Obtain actual returned commit SHA and read-back Git blob SHA. Execute:
   python tools/ingestion/ingestion_gate.py confirm plan.json CANDIDATE.yml COMMIT_SHA READBACK_BLOB_SHA > verified.json
   Require exit code 0 and status verified. Commit SHA alone is insufficient.
4. Re-fetch the main manifest and checkpoint. Before advancing the manifest call:
   python tools/ingestion/ingestion_gate.py authorize-advance current_manifest.yml current_checkpoint.yml verified.json FIRST_PRINTED FIRST_PDF NEXT_PRINTED NEXT_PDF
   Require authorized true. With multiple semantic records supply a JSON ARRAY of verified receipts. Stop on stale heads, pending IDs, duplicate files, missed pages, or out-of-route ranges.
5. Update the authoritative manifest against the current blob SHA. Verify it. Then update WORKER_CHECKPOINT.yml against its current SHA and verify matching boundaries. Only a complete record/manifest/checkpoint sequence permits a further slice.
6. If the baseline, PDF hash, validation runtime, connector readback or current manifest cannot be verified, stop this RUN safely and use the existing pending/recovery protocol. NEVER skip the gate or disable the hourly automation.

The guard cannot independently verify that source extraction was complete or that neutral prose is semantically faithful; direct source-image review remains mandatory. It also cannot prevent an actor with direct GitHub write rights from bypassing it. GitHub Actions tests gate code; do not claim branch-protection enforcement without verification.

Preflight evidence for the already accepted FASA7118 pp.34–61 manual run is absent. Do not invent retroactive receipts, do not rescan previously verified pages without a specific audit reason, and do not pretend GitHub acceptance proves full fidelity. Record this audit debt separately while preserving the real progress boundary.

## Mandatory editorial preflight for new semantic writes

Read and use `tools/ingestion/connector_preflight.py` in the current working container. Dependencies: Python 3.10+ and PyYAML. Its synthetic qualification is available with `--self-test`; do not repeatedly claim those tests as new ingestion progress.

During the EXISTING source-reading/normalization pass:

1. Extract the complete meaningful source assertions and all protected mechanics into a source-reviewed structured baseline. This is not a verbatim-prose archive. Write non-mechanical facts in plain, non-graphic third-person reference language from the start. Preserve who did or alleged what, to whom, where/when, why where supplied, scope, conditions, consequences, certainty, negation, consent/coercion, provenance and source-period/edition boundaries. Keep claims and hypotheticals distinct from established facts. Do not fabricate baseline evidence or derive a supposedly independent baseline by copying an already altered candidate.
2. Split writes BEFORE their first attempt. Each new file has exactly one `content_class`: `rule_exact`, `rule_procedure`, `equipment_stat`, `character_option`, `world_fact`, `campaign_guidance`, `attributed_claim` or `narrative_context`. Split mixed passages by semantic type while linking related record IDs. Existing accepted mixed records are not rewritten or replayed just to satisfy this new-write check.
3. For the new-record envelope retain `id`, `record_type`, `status`, `source`, `printed_pages`, `pdf_pages`, `edition_scope`, one-element `content_class`, and a nonempty `data` mapping containing the complete substantive material. Reuse canonical IDs. Preserve source/page attribution at subsection or assertion level when the source range is broad. Other metadata/relationships may remain alongside these fields.
4. Freeze the baseline before editorial polishing. Only root `headline`, `summary` and `framing` are editable presentation fields. Facts, mechanics, tables, ordered procedures, exceptions, identities, qualifiers, source metadata and lineage belong in frozen fields, not solely in an editable summary. Protected content uses `framing: reference_exact`; non-mechanical content uses `newsroom_neutral` or `broadcast_safe`.
5. Run `python tools/ingestion/connector_preflight.py BASELINE.yml CANDIDATE.yml` for each planned semantic write. A passing result checks one semantic class and exact preservation of every non-presentation field, including scalar types and ordered lists. It emits a candidate-file SHA-256. Submit those exact validated UTF-8 bytes, not a newly composed version. Revalidate any changed candidate. Keep a compact receipt of the result and verify the accepted GitHub blob against the candidate. A nonzero exit is not permission to omit source material or skip validation.
6. Source accuracy and editorial adequacy still require direct source review. The checker does not understand prose, prove extraction completeness, identify every misclassified rule, or guarantee connector acceptance. Review the candidate against the source: no missing independent facts, invented facts, unsupported certainty, dissolved distinctions or rules hidden in prose. Approved examples and the completed source7118 transaction are in `references/audits/source7118-editorial-recovery-2026-10-08.yml`.

### What newsroom language means

This is editorial reporting, not a sensitive-word substitution dictionary. Describe the event or relationship plainly without a graphic scene, taunting voice or instructional address. Attribute disputed statements to their actual source. Corporate diction is acceptable only when the reader still understands what is being alleged.

Do not turn coercion into voluntary employment, covert implantation into ordinary medical care, extortion into an unspecified service, an allegation into fact, or a hypothetical risk into a historical event. Those are semantic losses, not neutral style. Earlier example euphemisms are conditional illustrations, never mandatory replacements. No euphemism applies to protected mechanics, mechanically meaningful terminology, IDs or lineage.

Do not repeat colorful source passages in summaries, notes, comment bodies, titles, commit messages or error receipts after cleaning the principal description. Avoid unnecessary quotations. State files contain IDs, numeric boundaries, scan-depth codes, record commits and terse neutral reasons only.

### Write outcomes and recovery

Commit semantic/canonical records first, the main manifest second, and the checkpoint third. Only a clean, verified three-step transaction permits another slice. Never process more than two bounded slices per scheduled run.

Record observed failure evidence, not guesses: operation/path, candidate hash, expected blob SHA for an update, observed error/code/status/classification when supplied, and a short sanitized diagnostic. Keep substantive diagnostics in a compact audit receipt when allowed, never source prose in a manifest. Missing diagnostic fields remain null/unknown. A rejection is not evidence of a particular sensitive word, content filter, stale SHA or outage. Fetch the current blob SHA before updating an existing file; investigate administrative errors independently of editorial wording.

After a content-related rejection, only a substantive permitted revision of NON-MECHANICAL presentation may be attempted, with the frozen facts rechecked; do not change protected mechanics, obfuscate data, encode it, cycle euphemisms, fragment it to evade a denial or resend a denied payload via alternate Git-object APIs. When genuinely different source-grounded normalization is needed, preserve the earlier baseline and document the semantic comparison rather than silently editing it to make a test pass. An unresolved denial remains pending, not omitted.

If semantic normalization remains blocked, preserve the verified range and exact pending ID in the main manifest, mirror the checkpoint and end THIS RUN. If the main manifest cannot be written, create only the compact recovery sidecar permitted by the main handoff, keep the checkpoint at the last authoritative manifest boundary, and end. In that constrained fallback, use a terse observed operation/error category in `reason`; do not invent additional sidecars or copy rejected narrative. Retire a sidecar only after manifest/checkpoint reconciliation is durable.

A blocked run must not disable the hourly automation. Future runs check current GitHub state and changed conditions without blindly replaying identical rejected writes. Disable only on explicit user instruction or verified completion of the entire Pass B queue. No recursive schedules.

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

Then proceed through SR3-era adventures/campaigns. Legacy SR1/SR2 lineage is Pass C.

When the active source is complete, take the first source in checkpoint.next_sources; otherwise use this fixed order. Create a missing source manifest and durably checkpoint the transition before scanning. Reacquire the cataloged Drive source fresh every run. Use directed depth with a deep scan of every rules-bearing subsection. Preserve printed/PDF provenance and do not infer supersession. Do not mark a source complete with required pending normalization or unresolved completeness-blocking gaps.

`pending.source10652.missing-p110-111` is resolved and nonblocking under `references/audits/source10652-gap-p110-111.yml`. Reopen only for a new source copy or new evidence. Do not reconstruct missing narrative or re-add it to open conflicts.

## Historical snapshot — not execution state

The original 2026-09-26 handoff recorded source.fanpro-10666 through printed p45/PDF p47, resuming at p46/PDF p48 (Celedyr), with last_commit 0e2c3c4f4f3a8d6e8fbc4df1b9990c1c15e84457. Earlier ranges were pp7-23, pp24-34 and pp35-45.

Historical pending IDs were pending.dragons.draco-foundation-p24-34, pending.dragons.range-7-23, pending.ssg.game-info-p118-126 and pending.ssg.detailed-lifestyles-p127-144. These are archival context only. Their present status comes from current main source manifests; never copy this historical list into current open conflicts or resume state.
