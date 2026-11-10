# Core + advanced mechanics readiness — 24-hour recovery window

**Snapshot:** 2026-11-09 20:40 America/Chicago; sprint ends 2026-11-10 20:40 CST.  
**Role:** evidence-backed engineering backlog, NOT a semantic ingestion receipt, source verification receipt, completion authorization, or assertion that a rule is executable.  
**Source corpus:** fictional *Shadowrun Third Edition* tabletop game (FASA Corporation and historical FanPro SR3 publications). Source and edition provenance must travel with every game-rule dependency.  
**Automation:** preserve the single existing hourly Pass B worker and its schedule; do not create another ingestion worker. Denver FASA7212 printed pp46–47 remains independently deferred, completed-through printed p45/PDF46. Do not credit missing pages.

## Evidence and known facts

This triage reviewed current default-branch GitHub source manifests and sampled canonical records. Original page images were **not reacquired for this triage document**; no new source-fidelity, mechanical-correctness, or transaction-gate claim is made here.

- `sources/manifests/SR3.yml`, source.sr3-core / FASA7001: `scan_complete_normalization_pending`. Entire core was scanned; **printed pp275–282** dense Street Gear tables; **pp305–311** additional Street Gear; and **end-of-book edition-conversion pages** remain explicit normalization issues. Map exact conversion-page boundaries from original evidence rather than guessing.
- `sources/manifests/SRComp.yml`, source.srcomp / FASA7905a: marked `complete`, yet notes explicitly defer detailed material in **printed pp32–43** (alternate characters) and **pp44–58**. Treat these as open until record-level source verification proves otherwise; do not silently change the source status.
- `sources/manifests/Matrix.yml`, source.matrix / FASA7909: marked `complete`, yet notes retain **pending.matrix.range-76-94** (program options, command sets, autonomous-program structures, infection-related code, purchased-program behavior). A core programming procedure exists, but it does not by itself close this debt.
- `sources/manifests/SprawlSurvivalGuide.yml`, source.fanpro-10667: `scan_complete_normalization_pending`; **pending.ssg.game-info-p118-126**. Its lifestyle pp127–144 are separately described as normalized. Prioritize the deferred range's *actual* rules before further lifestyle/world narrative.
- `sources/manifests/StateOfTheArt2063.yml`: `ingesting`; detailed mechanics reviewed through printed p53. Later mechanics have **not** been declared fully normalized here; inspect genuine gaps after primary SR3/Companion/Matrix obligations.
- `sources/manifests/MitS.yml`, `Rigger3.yml`, `CannonCompanion.yml`, `M&M.yml`, `Critters.yml`, `QuickStart.yml` report completed mechanical scans. This is evidence of available coverage, **not** automatic executable or regression-tested status.
- The larger setting, historical Second Edition, and adventure-source backlog is not a prerequisite for a first testable SR3-inspired mechanical engine. Do not silently import historical Second Edition procedures as operative SR3 rules.

## Known canonical implementation anchors (verified repository paths)

| Engine lane | Existing canonical record or procedure | First validation obligation |
| --- | --- | --- |
| Test kernel | `rules/tests/making-tests.yml`; `rule-of-six.yml`; `target-numbers.yml`; `opposed-test.yml` | Dice-by-die successes, TN floor 2, exploding 6s, exceptions and ties |
| Character state | `procedures/character-creation/standard.yml`; `rules/character-creation/priority-system.yml` | Resolve actual numeric Master Character Creation Table; choices/prerequisites/attribute and skill spending |
| Action loop | `rules/initiative/initiative.yml`; `initiative-passes.yml`; `rules/combat/combat-turn-sequence.yml` | Initiative dice are not exploded; combat pool refresh and next-pass timing |
| Combat | `procedures/combat/ranged-attack.yml`; `melee-attack.yml`; `rules/combat/damage-resistance.yml`; `damage-staging.yml` | Attack/dodge/body/power/armor, melee tie exception, staging and condition monitor |
| Magic | `subsystems/magic/sorcery.yml`; `rules/magic/drain.yml` | Casting/sustaining/Force and Drain damage, source-specific exclusions and modifiers |
| Matrix | `rules/matrix/system-test.yml`; `procedures/matrix/programming.yml` | System/security concurrent resolution; unblock FASA7909 pp76–94 numeric/program-option details |
| Rigging | `subsystems/vehicles/design.yml`; `sources/manifests/Rigger3.yml` | Exact vehicle design tables, loading, control, drone orders and optional modifiers |
| Progression | `rules/advancement/skill-improvement.yml` | Cost factors, linked-attribute thresholds, rounding, Karma spending |

All links use stable canonical IDs, optional status and source relations as defined by `schema/conventions.md` and `indexes/rule-lineage.yml`. References are not a license to infer missing values or to treat a source's `complete` status as program correctness.

## Source-fidelity recovery order (bounded original-page review)

1. **P0: playable numerical foundation.** For the above anchors, explicitly enumerate each required field, canonical ID, exact printed/PDF provenance, formula, conditional modifier, exception, dependency and example. Verify source-specific numerical tables are really present and not merely named.
2. **P0: SR3 core deferred mechanics.** Independently review original printed pp275–282 and pp305–311 and edition-conversion material. Reuse existing records; for any missing or truly incorrect contribution, create independently reviewed baseline/candidate, run original staging/prepare, normal GitHub contents write and exact readback/confirm. Do not update unrelated lore.
3. **P0: Companion optional character rules.** Independently review pp32–43 and pp44–58, resolve only genuine gaps, and annotate optional vs effective core status. Do not erase older baselines.
4. **P0/P1: Matrix programming pp76–94.** Reconcile all numeric programming plan/time/size/rating, command-set, program-option, purchased-program and autonomous-code mechanics with accepted canonical records. Record the exact rules still lacking source or transaction proof.
5. **P1: Sprawl Survival Guide Game Information pp118–126.** Close actual mechanics only, preserving optional lifestyle and social-rule scope.
6. **P1: Additional advanced mechanics.** Continue remaining State of the Art 2063 and other authentic SR3 source mechanics only if earlier gaps are closed, blocked or safely delegated to later review.
7. **P2: Gameplay-independent preservation.** New Seattle lore/illustrations, deferred Denver, older setting detail and unrelated character biographies continue as archival work but cannot displace P0/P1 during the sprint.

**Stop/go rule:** A page scan, canonical YAML path, completed source manifest or structural validator alone is insufficient. Show original-page confirmation and legitimate transaction/readback/authorization as applicable. Mark unresolved source-specific gaps openly.

## Engine-ready acceptance contract

Create a separate read-only consumer snapshot, with explicit schema version and source/edition provenance, from the **accepted** canonical files. Every encoded implementation mechanic must include: `id`, `effective status`, `source/page`, exact inputs, output, deterministic resolution, modifier precedence, tie behavior, optional toggles, dependency IDs, and a source-reviewed test reference. Separate: `record_exists`, `source_verified`, `normalized_exact`, `cross_source_reconciled`, `code_tested`.

Prioritize source-reviewed examples for:
- TN floor 2 and individual-die counting; exploding-six chain; Rule of Six exclusion for Initiative
- opposed-test ties versus melee's explicitly different tie behavior
- initiative passes subtracting 10; action and Combat Pool refresh timing
- hit, dodge, damage resistance, two-net-success staging and final Condition Monitor
- character-creation priority table, attribute/skill limits and Karma cost rounding
- spell Drain Force-vs-Magic consequences; defensive allocations
- concurrent Matrix System/Security Test outcomes, then programming task periods/options
- basic vehicle/drone tests and advanced optional-rule isolation

**Deliverable:** A reviewed `engine_ruleset_v0` manifest and runnable test-vector specifications for the *mechanical foundation*, plus a precise list of unresolved rule IDs/printed-PDF pages. This is a documentation and rule-normalization milestone, not a claim that a full game has been coded. Do not replace the ongoing preservation project or reproduce publication prose/art in an end-user product.

## 24-hour reporting

Each subsequent run report should list: actual mechanically important rules normalized with exact paths/commits/blobs and readback/gate result; how many priority obligations were closed versus merely reviewed; the exact newly discovered gaps; target example/test-vector progress; and separately the authoritative Denver printed/PDF boundary and any unrelated forward work. **Never use the count of lore or illustration records as a proxy for game-engine readiness.** At sprint expiry, restore the prior normal transcription priority automatically while keeping the existing hourly task enabled and its original schedule unchanged.
