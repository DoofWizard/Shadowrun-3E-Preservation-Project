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

## Source-verified Companion mechanics supplement — November 9 late session

The **fresh original cataloged PDF** from connected Google Drive, *Shadowrun Companion* by FASA Corporation (FASA7905a, Shadowrun Third Edition), has SHA-256 `8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5`, matching the live Companion manifest. Original page images for the below ranges were inspected. The Companion manifest registers **seven** optional mechanics records (including already registered earlier records) with ordinary GitHub readback and transaction confirmation. These are source-reviewed **normalized optional rules**, not a tested game implementation, not a resolution of all Companion pp32–58 debt, and not contiguous Denver progress.

| Engine input and canonical record ID | Original source (printed/PDF) | Standing | Still missing for code readiness |
| --- | --- | --- | --- |
| `option.character-creation.shapeshifter-player-characters` | FASA7905a pp34–35/PDF35–36 | verified, optional | SR3 base priority/point-buy integration, complete alternate-character prerequisite checks, implementation tests |
| `rule.character-creation.srcomp-shapeshifter-racial-modifiers` | FASA7905a p36/PDF37 | verified, optional exact table, seven species | Correct application/precedence with separately calculated human/animal ratings |
| `rule.character-creation.srcomp-shapeshifter-attribute-limits` | FASA7905a p37/PDF38 | verified, optional exact table, 7 × 9 limit/maximum pairs | Validation against form-specific advancement and caps |
| `rule.character-creation.srcomp-shapeshifter-regeneration-silver` | FASA7905a pp36–37/PDF37–38 | verified, optional procedure | Dependencies on Critters Regeneration, SR3 Deadly damage and medical rules, Magic loss, Hand of God, focus and Drain resolution |
| `rule.character-creation.srcomp-shapeshifter-dual-nature` | FASA7905a p36/PDF37 | verified, optional procedure | Astral access, ward detection/collision, Masking, Combat Pool and projected-form handling |
| `option.character-creation.srcomp-metahuman-albinism` | FASA7905a p37/PDF38 | verified, optional | Edge/Flaw spending, Willpower racial-modified-limit propagation and racial maximum validation |
| `option.character-creation.srcomp-metahuman-variants` | FASA7905a pp37–43/PDF38–44 | verified, optional, 14 variants | Variant modifier precedence, vision/armor, movement, allergies, immunity choice and social-Reaction integration |

### Test vectors — specifications only, not executed

The following examples come from the reviewed original Companion pages and are **candidate executable assertions** for a future engine. No runtime or unit-test success is claimed.

| ID | Input | Expected source-rule outcome |
| --- | --- | --- |
| `shifter.deadly.ordinary.d6_1` | Normal Deadly physical injury; 1D6 = 1 | Regeneration fails; ordinary medical/damage rules determine survival rather than automatically asserting immediate death. |
| `shifter.deadly.ordinary.d6_2` | Normal Deadly physical injury; 1D6 = 2 | Regeneration succeeds; damage penalties apply in the injury Combat Turn, damage vanishes at start of next Combat Turn. |
| `shifter.deadly.massive.d6_2` | Deadly injury with massive tissue trauma; 1D6 = 2 | Regeneration fails (the exceptional failure set is 1 or 2). |
| `shifter.deadly.silver.d6_2` | Deadly silver injury; 1D6 = 2 | Regeneration fails and death is immediate under the special silver rule. |
| `shifter.silver.weapon_4L` | A knife doing 4L damage is made of silver | Weapon damage becomes 6M, and contact also causes a separate automatic Light Wound; preserve both effects. |
| `shifter.focus.force_3` | Deadly weapon-focus injury, focus Force 3 | First roll an Essence Test against target number 6; zero successes means death, at least one permits the normal regeneration roll. |
| `shifter.astral.perception` | Shapeshifter invokes astral perception | Simple Action; astral presence cannot be turned off. |
| `variant.cyclops.ranged_TN4` | Cyclops ranged attack, ordinary pre-variant target number 4 | Apply +2 ranged target-number modifier for depth-perception limitation: TN 6. |
| `variant.albino.willpower` | Optional albino, Willpower before this feature 3, applicable racial modified Willpower limit before feature 6 | Willpower becomes 4 and the racial modified Willpower limit becomes 7; one listed Flaw is mandatory without compensation. |
| `variant.koborokuru.immunity` | Koborokuru character at creation | Two Natural Immunity Edges (1-point and 3-point), no balancing Flaw, identify one natural and one man-made toxin; running multiplier 3. |

### Other engine lanes — sampled repository anchors, not yet source-image reverified

| Lane | Existing canonical IDs / repository-attributed printed page | Present status / missing implementation inputs |
| --- | --- | --- |
| Dice / tests | `rule.tests.making-tests`, `rule.tests.target-numbers`, `rule.tests.rule-of-six` (SR3 core; exact original pages **not** independently rechecked here) | Canonical records exist; rule-of-six exclusion for Initiative is expressed; need source-page comparison, interpreter semantics and tests. |
| Priority creation / advancement | `rule.character-creation.priority-system` (core p54), `rule.advancement.skill-improvement` (core p245) | Canonical records exist; verify master table values, effective rules and rounding, implement tests. |
| Initiative / combat | `rule.initiative.initiative-passes` (core p102), `procedure.combat.ranged-attack` (core p109), `rule.combat.damage-staging` (core p113) | Canonical records exist; no code-test claim; need full action-cycle, pool-refresh, attack/resistance and timing test fixture. |
| Magic | `rule.magic.drain` (core p162), optional Companion shapeshifter Drain above | Canonical record exists; need unified Force/Drain and special regeneration with exact timing. |
| Matrix / programming | `rule.matrix.system-test` (core p209), `procedure.matrix.programming` (Matrix p76) | Canonical records exist but FASA7909 pp76–94 deferred normalization still open; missing complete effective programming options/size/time/ratings reconciliation and executable program tests. |
| Cyberware / bioware | `rule.cyberware.essence` (core p296), optional Companion cyberware rejection above | Canonical records exist; core Street Gear pp275–282 and pp305–311 and cross-source equipment audit remain open. |
| Rigging | `subsystems/vehicles/design.yml` (repository anchor; precise original printed/PDF pages not checked in this session) | Record exists; source-image verification, complete design inputs and implementation tests remain. |

**Separation of claims:** source PDF and cited Companion pages were checked; the seven optional records are GitHub-confirmed and indexed; other listed canonical paths were checked for existence and stated edition/source references only. No `engine_ruleset_v0` executable code was generated or tested by this document. This snapshot does not mark any unresolved source range complete, does not change Denver, and should be revised with concrete tests only after running them.
