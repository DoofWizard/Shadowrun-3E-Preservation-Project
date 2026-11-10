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

## Manual recovery checkpoint (source-confirmed core and regression harness)

**Recorded 2026-11-10 UTC.** No other book, page or rule family is implicitly marked complete by this update. This is an incremental proof-of-work and specific remaining-dependency handoff.

**Source-verified core repair — FASA7001, Shadowrun Third Edition:** Original 112,507,704-byte PDF freshly retrieved from the connected Drive source; SHA-256 pinned in `sources/manifests/SR3.yml` as `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`. Source verification and original page inspection performed before candidate freeze.

| Accepted source-reviewed mechanics | Printed/PDF | Verified semantic commit | Git blob |
| --- | --- | --- | --- |
| `procedure.firearms.sr3-core-ammunition-reloading` — action/Quickness reloading table | p280/PDF289 | `ef9eea41d7f38ab23cbea11cb4ffa4100287fa17` | `6699745b7bad26e3ad808e360edb4f66f7f86fe7` |
| `equipment.ammunition.sr3-core-catalog-p281` — rocket/missile and ammunition acquisition/statistics tables | p281/PDF290 | `f47bf0b36ea35db0e83c714ba6d89468bbfa6d49` | `28ec27bdfe39c4838e8aa92282cb0ba7b20cc27a` |

Original baseline/candidate stage journals, exact UTF-8 GitHub readbacks, gate confirmations and editorial receipts were produced. Both rows are registered as *noncontiguous verified supplements* in authoritative source-manifest blob `71b8bb8d0bd7fadd9204069b070207ca3e98af31`, administrative commit `87c7ac7e9abf5af57ddde015222ec948318bbe6e`. Other dense p275–282 rows, p305–311, and conversion details are explicitly STILL OPEN.

**Companion optional-character recovery:** `sources/manifests/SRComp.yml` registers **seven** source-reviewed and confirmed semantic contributions from original FASA7905a printed pp34–43 (PDF35–44): shapeshifter creation, signed racial modifiers, numeric attribute limits, regeneration/silver/weapon-focus rules, dual nature, albinism and fourteen metahuman variants. The companion still has outstanding review obligations outside these accepted records, especially the rest of pp32–58. Do not assume all deferred Companion content is resolved.

**Executable test harness (source-linked but not comprehensive):**
- `tools/engine_readiness/rules_probe.py` — GitHub commit `1fca98d292559bdf4be69cdb94ec364a5a258ba9`, verified blob `6b74c7e6f173e9b03dcfee00e286a64313caadfc`.
- `tools/engine_readiness/test_rules_probe.py` — GitHub commit `394388be7ddfc718c071707232b0ff07315804d7`, verified blob `89b454ced73bc0793fe5aea1bcff85e0703b0b20`.
- Local command `python -m unittest discover -s /mnt/data/sr3_manual_sprint/engine_harness -p 'test_*.py' -v` completed **22 tests, all passing**. Re-run after pulling repository files with `python -m unittest discover -s tools/engine_readiness -p 'test_*.py' -v`. Tests exercise the limited dice, initiative, net-success staging and confirmed p280 reloading functions; they **do not** validate the full engine, full sourcebooks or magic/Matrix/rigging.
- See `tools/engine_readiness/README.md` for exact audited boundaries. `UnresolvedRule` is deliberately raised where a calculation or tie-break needs other records or source reinspection.

**Next fastest mechanical work:** finish source-verifiable missing SR3 Street Gear numeric tables, p305–311 and conversion material; finish Companion pp32–58 options; then Matrix FASA7909 programming pp76–94 and FanPro10667 Sprawl Survival Guide game information pp118–126. Reuse verified canonical IDs and preserve legal optional/supersession semantics; never substitute scanned prose or archival item counts for implemented mechanics.

### New source-confirmed optional training resolution

**Canonical ID:** `rule.training.srcomp-optional-skill-attribute-training`; `rules/skills/srcomp-optional-training-exact-p48-51.yml`. FASA Corporation *Shadowrun Companion* FASA7905a, SR3, original printed pp48–51/PDF49–52, original PDF SHA-256 as above. Exact normal GitHub record commit `c00381b6ef94e22f6c6f1f97f095999f10afe6d1`, readback blob `94221abe39c32a5f4234999cf56c87e0eb5d80a9`, `ingestion_gate.py confirm` verified. The existing higher-level `option.training.optional-training-rules` remains the option toggle; this **extends** it with source-specific executable inputs instead of replacing the baseline SR3 Karma system.

**State:** source-reviewed, normalized, independently confirmed and indexed; **optional, not active by default**. No engine tests executed. The source provides days-per-Karma multipliers, Skill Test TN, success rounding, interruptions, instructor qualifications and *success bonuses rather than bonus dice*, virtual instructor restriction, hour limits and suggested nuyen fee tables. The pp44–47 Athletics / fatigue / water mechanics and pp52–58 hiring/contact material are **not** declared complete by this record.

Additional candidate assertions for later implementation, not executed:

| Vector | Source inputs | Expected outcome |
| --- | --- | --- |
| `training.knowledge.2success` | 3 Good Karma spent to improve Knowledge skill; 2 Skill Test successes | Base `3*15=45` training days; `ceil(45/2)=23` days. |
| `training.active.instructor_bonus` | 6 Good Karma for Active skill; initial training Skill Test 2 successes; instructor achieves 2 successes on Instruction (4) | Base `6*7=42`; instructor adds **1 success to student's Skill Test success total** (not a die), resulting `ceil(42/3)=14` days. |
| `training.knowledge.failed_skill_test` | Knowledge-skill base 45 days; 0 test successes | `ceil(45*1.5)=68` training days. |
| `training.interruption` | Intelligence 5, new skill rating 3, 5 remaining training days; training interrupted 14 days | Interruption threshold `5+3=8` days is exceeded, so 10 extra training days are added to the remaining time. |
| `training.attribute.instructor` | 21 Good Karma for Charisma; Attribute (6) Test 2 successes; qualifying instructor adds 1 student success | `21*7=147` days; divided by 3 successes yields 49 days. |
| `training.daily.limit` | Willpower 6 | Normal maximum `ceil(6/2)+4=7` hours training per day. Additional practice is only effective if declared and supported by a Willpower TN 10 Test. |
| `training.fees.instruction_4` | Instructor Instruction rating 4, before other fee modifiers | Suggested fee 100 nuyen/day; class setting, specialization, subject rating and hours modifiers must then be applied per source with no invented rounding or precedence. |

**Total in Companion postcompletion recovery manifest after this update:** eight verified supplemental mechanics records. This number is a manifest count, not eight newly authorized contiguous pages or eight code-ready features.

## New FASA7001 p305-306 gear resolution

The original FASA Corporation *Shadowrun, Third Edition* (FASA7001) 112,507,704-byte PDF was freshly reacquired from the cataloged Drive source and verified against `sources/manifests/SR3.yml` SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`. Original printed page images p305/PDF314 and p306/PDF315 were inspected before baseline freeze. These source-reviewed `equipment_stat` records passed the normal staged journal, ordinary GitHub contents write, exact matching blob readback, and local `ingestion_gate.py confirm`; both were registered in source manifest commit `2067b301fa01fd8dd99d593d23ae7248619881f4` (blob `f7103397a0219718531a4f37de8c5b362bdaa73f`). No Denver contiguous progress is claimed.

| Subsystem | Canonical record ID and page | Exact verified GitHub commit/blob | Mechanical coverage and readiness |
| --- | --- | --- | --- |
| Magic item procurement | `equipment.market.sr3-core-magical-equipment-p305` — `equipment/sr3-core-magical-equipment-market-p305.yml`, printed p305/PDF314 | `16e21f05f209e6864f368e3b61c4be168360d5db` / `e0af2b0c66bf35e379984eff5689ac7b61696f50` | **Historical core; source-reviewed normalized; not code validated.** Seven focus purchase entries, three supplies, five fetishes, four spell-formula tiers; exact cost formulas, availability times, street index and source illegality rule. Later `rules/magic/spell-formula-market.yml` from MitS must be compared before choosing effective price/version. |
| Rigger procurement and vehicle adaptation | `equipment.rigging.sr3-core-rigger-vehicle-gear-p306` — `equipment/sr3-core-rigger-vehicle-gear-p306.yml`, printed p306/PDF315 | `12240d5e139c529d3bea91dd23d5a6bfb1f0064f` / `7fcf9e1360c733c1115612fcdddf5b44f01f6a8d` | **Historical SR3 core; source-reviewed normalized; not code validated.** Datajack/remote/vehicle control gear, RCD, ECCM rated cost tiers and legality, hitcher jack/displays/intercom; Sensor >=1, Pilot Rating 1, Cargo Factor and Load requirements. Later Rigger 3 explicit extensions/corrections still require lineage review. |

**Executable-example inputs, NOT test results:** A Force-2 power focus costs 210,000¥; a Rating-3 Hermetic Library per skill costs 9,000¥; a Reach-1 Force-2 weapon focus costs 380,000¥. Remote Control Gear for Body 4 costs 10,000¥; a Rating-3 remote-control deck costs 15,000¥; Rating-5 remote-control ECCM costs 75,000¥. A Vehicle Control Gear installation requires Sensor Rating >=1 and an existing datajack port or remote-control gear, and consumes 1 CF / 10 kg Load. These are recorded expected calculations; engine execution and supersession decisions remain open.

**Coverage separation:** Two original source pages independently re-reviewed; two distinct records gate-verified and indexed; **zero additional engine-passing mechanics tests** in this update. The larger deferred Street Gear pp305–311 obligation is still open for the omitted parts; this is not a completed range. Future mechanic work should finish vehicle tables, medical/gear rules and conversion pages without duplicating existing named canonical concepts.
