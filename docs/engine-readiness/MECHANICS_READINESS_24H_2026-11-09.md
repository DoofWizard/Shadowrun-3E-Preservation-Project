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

### Original p312/PDF320 vehicle-market and drone values

**Accepted and manifest-indexed record:** `equipment.vehicles.sr3-core-drones-mounts-weapons-p312`, `equipment/sr3-core-vehicle-drones-mounts-weapons-market-p312.yml`, FASA Corporation *Shadowrun, Third Edition* FASA7001. Independently reviewed original printed p312/PDF320 (original SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`). Ordinary GitHub semantic commit **`9e449be22e65944be4580db8879c67ace73d52d9`**, exact readback blob **`e5d91ad70ab46ec28f9c151db4547a0b48274d83`**, normal local source-review/editorial staging and `ingestion_gate.py confirm` **verified**. Indexed as *noncontiguous supplementary* `equipment_stat` in source-manifest commit **`702f126df77a8e39a09a949322d8c560701a7907`**, blob **`63d18e5d725d89f10fcc8d877da36b684446ff7c`**. No contiguous Denver/SR3 progression.

This preserves **four named original drone specification rows**, **seven original vehicle-mount configurations** (CF, load, Availability, price, Street Index, legality, recoil code), and **two vehicle-grade weapon entries** including the gamemaster-determined acquisition fields. The established **`rule.vehicles.weapon-mounts`** from *Rigger 3* (later SR3 source) already captures expanded mount mechanics: reuse it, but retain core FASA7001 historical raw numeric details for source lineage; no silent supersession. Current code status **source-reviewed and normalized, not engine-tested**.

**New unresolved in-source discrepancy to gate code implementation:** printed p312/PDF320 labels the Water Cannon's Mode **"SA"**, whereas original printed p307/PDF316 expressly describes firing **always autofire, 10 shots/action, without recoil**. Both statements are accurately preserved in the record. A ruling/erratum/edition-specific engine interpretation remains **ambiguous**; no mechanical behavior was invented. Suggested unexecuted examples: two pintle mounts cost 100¥; external firmpoint plus internal hardpoint consume 8 CF; original Roto-Drone Body 2/Pilot 1/Sensor 1 costs 6,600¥. None are claimed as engine test passes.

**Scan mapping audit debt, identified from original image numbers:** physical PDF316 visibly has printed page **307**, while the **immediately following PDF317** visibly has printed page **309**. There is no intervening PDF image displaying printed p308 in this original PDF sequence. This contradicts the broad legacy SR3 manifest note treating printed pp305–311/PDF314–319 as if each printed page were present. **Disposition: pagination anomaly, possible omitted printed p308 requiring targeted continuity/index review**; not enough evidence here to classify that printed page definitively as substantive or blank. Do not synthesize p308, assert complete original scan coverage, or collapse the p307→p309 mapping. The rest of p305–311 and conversion normalization remains open. Source-level scan coverage, normalized record coverage, and code-tested readiness are three different metrics.

## FASA7001 printed p282/PDF291 source-reviewed firearm accessory mechanics — November 9 22:58 CST

**Scope, publication and source assurance:** FASA Corporation, *Shadowrun, Third Edition* (fictional tabletop RPG, FASA7001, source.sr3-core). Fresh Google Drive source SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914` matched the live core manifest; original printed p282/PDF291 was examined visually before independently prepared baseline/candidate transactions. No claims regarding missing printed p308 or other deferred pages.

| Subsystem / original-source contribution | Canonical ID, exact GitHub path | Evidence / code status |
| --- | --- | --- |
| 22-row firearm/weapon accessory market table, original mount/conceal/rating/weight/availability/cost/street index/legality strings | `equipment.firearms.sr3-core-weapon-accessory-table-p282`; `equipment/sr3-core-firearm-weapon-accessory-market-p282.yml` | Source-reviewed original FASA7001 p282/PDF291. Semantic commit `075cec37c6ad8824a0b58fd0181bbb434d59adc3`, readback blob `581bcc3d32c0eb4a488fea674e30d9ce27c3d64f`, transaction confirmation **verified**. Existing `rules/firearms/accessory-mounts.yml` reused. **Normalized exact; not engine-tested or cross-supplement supersession-resolved.** |
| Tripod setup and ultrasound sight/goggle special rules | `rule.firearms.sr3-core-tripod-ultrasound-usage-p282`; `rules/firearms/sr3-core-tripod-ultrasound-use-p282.yml` | Source-reviewed original FASA7001 p282/PDF291. Semantic commit `d4c3ac11ecae83cc0e68bf803285e0fec8c854ff`, readback blob `f1cc43f1a58ef7bf1e5a291f3973c04aebd9ecc0`, transaction confirmation **verified**. **Normalized exact; not engine-tested.** |

Both contributions are registered as **noncontiguous verified supplements** in the core `sources/manifests/SR3.yml` (latest readback blob `53ae048166e6a79ab6f5ea82784a6158e11fe91c`; registration commits `1bc0e8b536b5f479eb47c4e9d62fdfa88478a82f`, `80f406f1fc754937a08faa179f96ae78d7d60be1`). They do not authorize any new contiguous Denver pages, close the larger p275–282 / p305–311 debt, or prove full core normalization.

**Unexecuted, source-grounded future test vectors:** (1) ultrasound lighting TN modifier +3 becomes +2 after halving and rounding upward; (2) lighting +4 and invisibility +3 become +2 and +2 respectively, without halving unrelated TN modifiers; (3) tripod takes one Simple Action to set up and grants 6 recoil-compensation points when used sitting or prone, not a fabricated standing exception; (4) table-to-inventory parsing must preserve the blank original tripod Legal cell and `Weapon`/`+100%` smartgun market cells without inventing default values. All vectors remain **specifications only** in this update, not executed tests or implementation acceptance.

**Next dependencies:** compare p282 table against later firearm/gear catalogs without assuming supersession; verify the remaining printed p275–281 equipment detail, the original p307→p309/PDF316→317 pagination discrepancy, other p305–311 gear, and mapped end-of-core edition-conversion procedures. Distinguish source-image coverage, normalized canonical coverage and code-tested readiness.

## P0 numerical closure: master priority and Condition Monitor (November 10)

The original FASA Corporation *Shadowrun, Third Edition* (FASA7001) PDF, SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`, was freshly obtained from the cataloged Google Drive item, verified with `preservation_method.py verify-source`, and the original scanned page images were examined: printed p54/PDF55 and printed pp125–126/PDF126–127. These are **new independent numeric supplements to existing general canonical concepts**, not replacements or fresh contiguous Denver authorizations.

| Dependency / canonical exact record | Original source | Normalized status; GitHub receipt | Code readiness and genuinely open inputs |
| --- | --- | --- | --- |
| `rule.character-creation.sr3-master-priority-numeric-p54`; `rules/character-creation/sr3-master-priority-numeric-p54.yml` | FASA7001 p54/PDF55 | Verified source-reviewed `rule_exact`: A–E numeric Attributes, Skills and Resources; original racial and Magic priority constraints. Commit `c6f4dfc6c5125d61a087ec4fe488773d2566c939`, blob `abd65c856673513042f0563ace7b4bfc5bc2a2e3`. Indexed in `sources/manifests/SR3.yml` commit `3090ad4b6673818fcbf177d85bc01f6a610a25a4`. | `core_extensions.py` implements a bounded budget validator. Still need full creation pipeline integration: racial adjustment/limits, spell-point handling, skill assignment, nuyen spend and elective Companion variant/point-buy precedence. |
| `rule.condition.sr3-damage-monitor-numeric-p125-126`; `rules/condition/sr3-damage-monitor-numeric-p125-126.yml` | FASA7001 pp125–126/PDF126–127 | Verified source-reviewed `rule_exact`: L/M/S/D 1/3/6/10 boxes, separate 10-box Stun and Physical tracks, overflow > Body death, untreated Physical overflow timing, additive Physical/Stun modifiers, wound table TNs. Commit `d8569cc0f7c80c25e2a067db21ca4cfff7aff5bf`, blob `5ba510e3e51b53eebbac30865f2cddc230bf1219`. Indexed in same SR3 manifest commit above, verified blob `86fc60af5f2ff50e54a5fd42c6bc07543f70775a`. | `condition_core.py` implements a bounded condition application/overflow adapter. Still need time-step Physical-overflow blood-loss, healing, first aid, specialized optional damage variants and effective supersession analysis. |

### Numeric test vectors and verification boundaries

- Priority A Attributes→30, C Skills→34, E Resources→5,000¥; Elf race→C. Inputs/expected values originate in printed p54, with their tests specified in the new numeric record.
- Serious staged damage→6 boxes; 6 Stun + Serious Stun→10 Stun and 2 Physical; Body 5 and 15 Physical boxes→not instantly dead, 16→dead; 3 Stun plus 1 Physical→combined injury TN +3 and initiative −3. These example expectations originate in printed pp125–126 and are specified in the new numeric record.
- A local run of `python -m unittest discover -s tools/engine_readiness -p 'test_*.py' -v` using freshly fetched current repository Python files completed **79 tests, all passing**. These test the bounded existing Python consumer prototypes, not an entire playable engine or archival source correctness. The newly staged canonical YAML records' example vectors have **not** been separately run as YAML-driven acceptance tests.
- **Coverage categories remain distinct:** three original printed pages visually reviewed; two additional source-reviewed numeric records accepted, confirmed and indexed; bounded prototypes passing their existing tests; **zero newly authorized contiguous Denver printed pages**. No other source range is declared complete.

**Open priorities:** FASA7001 other Street Gear pp275–282 and pp305–311, the printed p308 scan anomaly, conversion procedures, Companion remaining pp32–58 details, Matrix FASA7909 pp76–94 programming, FanPro10667 pp118–126 and full effective-rule lineage. Source-manifest status `scan_complete_normalization_pending` is unchanged, as are Denver's gap and checkpoints.

## FASA7909 Matrix programming numerical recovery — November 10, 2026

Fresh cataloged Google Drive PDF of FASA Corporation *Matrix* (FASA7909), historical Shadowrun Third Edition fictional tabletop supplement, verified SHA-256 `b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe` using the actual source-verification script and live Matrix manifest. Original printed pp81–83/physical PDF82–84 visually inspected before creating independently reviewed one-class baselines and presentation-only candidates. These are **noncontiguous canonical additions**, not a full programming-range closure, source-transition gate, or Denver boundary movement.

| Engine subsystem and canonical ID | Source/page, exact normalized rule coverage | Transaction receipt and readiness |
| --- | --- | --- |
| Matrix programming upgrade and optional bug subsystem — `rule.matrix.program-upgrades-optional-bug-and-glitch-p81-82`; `rules/matrix/matrix-program-upgrades-optional-bug-glitch-p81-82.yml` | FASA7909 pp81–82/PDF82–83: source-code prerequisites; upgrade-time minimum 25%; Bug Open Test modifiers and 8 named programming-language variants; 2D6+Rule of Six Glitch Table; occurrence tracking; debug time/modifiers; *bugs explicitly optional*. | Source-reviewed original images; preflighted candidate, staged, GitHub commit `f179e1c14db28964aa70d611731b51af0a05233b`, matching readback blob `80123bc30317d7869212ea7dc6bdf58d0dcb4456`, gate-confirm **verified**. No consumer test or final playable-engine claim. |
| Matrix option size/rating/cost — `rule.matrix.program-options-sizes-ratings-costs-p82-83`; `rules/matrix/matrix-program-options-sizing-rating-cost-p82-83.yml` | FASA7909 pp82–83/PDF83–84: option-adjusted actual/design Mp distinction, option rating cap, rating-before-sequential-percentage size calculation, base Programming TN, 200¥ per design Mp retail formula, book examples; optional scope preserved. | Source-reviewed original images; preflighted candidate, staged, GitHub commit `63348d911aff44d8586303fa6f79dba6f43dff86`, matching readback blob `bae77ee809c24fff3c9869d271ee49711f70ff1c`, gate-confirm **verified**. No consumer test or final playable-engine claim. |

**Proposed, unexecuted engine vectors:** upgrade new base time 100 days vs old 90 days → minimum 25 days; 5 program options → bug Open Test modifier −3; 3-person programming team → −2; base programming rating 4 with area option rating 4 → programming TN 4; two successive 50% reductions of 180 Mp → 45 Mp; retail design sizes 108 and 300 Mp → 21,600¥ and 60,000¥. All are source-derived specifications; they were not run against a game engine.

**Registration and remaining dependencies:** both verified records indexed in `sources/manifests/Matrix.yml` as source-reviewed supplements; the manifest explicitly retains `full_printed_pp76_94_deferred_normalization_resolved: false`. Existing `procedures/matrix/programming.yml`, `options/matrix/program-options.yml` and previously indexed pp78–80 numeric record were reused, not overwritten. Outstanding: individual utility/IC options and option compatibility, purchased programs, command sets, and autonomous-code detail from printed pp83–94, plus other unresolved source-specific mechanics. Numeric archive normalization is **not** equivalent to a code-tested Matrix subsystem. Denver remains printed p45/PDF46 and source-completion is not newly authorized.

## SSG Game Information exact-table recovery — 2026-11-10

**Provenance:** *Sprawl Survival Guide*, FanPro, FanPro10667, Shadowrun Third Edition. Fresh cataloged Google Drive PDF SHA-256 `b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f`; independently visually reviewed printed p120/PDF121 and p122/PDF123. Source verification was executed locally against the SHA-pinned main manifest. This is a partial, noncontiguous rules supplement; full printed pp118–126 normalization remains open. Other manual work may concurrently expand Matrix mechanics.

| Subsystem | Verified canonical record/path | Designation | Engine gaps and specification-only test vectors |
| --- | --- | --- | --- |
| Matrix example host | `rule.matrix.ssg-dataterm-host-sheaf-p120` — `rules/matrix/ssg-dataterm-host-sheaf-p120.yml`, printed p120/PDF121, commit `3147c4ee6362a6ee52d15c3cb39b381f0f8705fd` | Source-verified exact table; **example** of Green 4-8/8/8/8/8 host, not a globally effective rules override | Implement host alert/countermeasure trigger execution; specification cases: step 25→Passive Alert, step 30→Probe-6 with Killer-8 trap, step 60→Shutdown. No live game-engine implementation. |
| Household drone market | `equipment.ssg-household-drone-tables-p122` — `equipment/ssg-household-drone-market-p122.yml`, printed p122/PDF123, commit `0c554521cb2a47b6b0dab0e75138587ce0b5ceee` | Source-verified eleven-row paired equipment-stat tables; supplemental market, no Rigger 3 override implied | Implement exact vehicle construction/command compatibility and market lookup; specification cases: SynthCat 9,500¥, Butlerbot Pilot 2 (4), Mr. Fix-It 27,000¥. No live game-engine implementation. |

**Evidence layers:** scanned/read original source pages = yes, specifically p120 and p122; new normalized record coverage = two confirmed and registered paths; engine code-validation = **no new engine execution**. Six local file-structure/example assertions passed but only validate the records' internal shape. Individual receipt files contain reviewed text-field paths. Neither local checks nor GitHub acceptance proves extraction completeness.

**Companion directed audit:** Original FASA Corporation *Shadowrun Companion* (FASA7905a), Shadowrun Third Edition, printed pp52–58/PDF53–59 visually rechecked from fresh SHA-matching source. This segment is primarily an in-world fictional employment document, with printed p53 full-page illustration; no newly confirmed reusable numeric game-rule record from these reviewed pages. Other Companion deferred range pp32–58 is **not** thereby closed.

**Still open:** SSG p118–126 other content classes, including telecom access procedures, drone feature relationships and optional ID mechanics; source-specific rule applicability and engine tests. Denver printed p46–47 gap remains independently deferred, with completed-through p45/PDF46 unchanged. Do not promote this supplemental work to contiguous page authorization.

### SSG p124/PDF125 source-verified market supplement

The same freshly verified cataloged FanPro10667 source was independently visually reviewed for the **Common Costs** table on printed p124/PDF125. New exact canonical reference `reference.economy.ssg-common-costs-p124` in `references/economy/ssg-common-costs-p124.yml` was staged/preflighted, accepted/read back, confirmed, and independently registered in the SSG main manifest; semantic commit `708f8a3e1222d8554c8652f73f94f15579d3a727`. It carries 49 source-published service/market price rows and original scope/price footnotes, not binding global rules. **Code readiness: not executed.** Specification-only tests: a 24-hour coffin-hotel visit 30¥; one-week car rental 500¥; city bus/rail 1¥ per 10 km. Literal source price strings preserve decimal notation, range bands, unit/time qualifiers and the optional GM nature of average costs. The extended SSG p118–126 normalization debt is still open and none of these noncontiguous records authorizes Denver page advancement.


## Verified Matrix programming p92–94 supplements — 2026-11-10 06:34 CST run

**Independent source:** *Matrix* (FASA Corporation, FASA7909, Shadowrun Third Edition), fresh connected Google Drive cataloged PDF SHA-256 `b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe`, verified locally against the live Matrix manifest. Original printed pp92–94 / physical PDF93–95 visually reviewed. Content represents fictional tabletop Matrix mechanics, not real-world computer instructions. Local source-review receipts list all audited nested text-field paths. Both records used original-source-reviewed, independently frozen baseline/same-substance candidate; staged via `transaction_recovery.py stage`, passed `ingestion_gate.py prepare`, were submitted only through ordinary GitHub contents `create_file`, exact readback matched the staged bytes and each `ingestion_gate.py confirm` returned `verified`. A successful transaction is not proof of completeness or engine execution.

| Subsystem | Canonical ID and exact path | Provenance and designation | Missing implementation/test dependencies |
| --- | --- | --- | --- |
| Program purchase, inspection and application guidance | `rule.matrix.purchased-software-verification-p94`; `rules/matrix/matrix-purchased-programs-verifying-applications-p94.yml`; semantic commit `e10384551caff5c3a80e956ad0eb4868d15cfad6`; blob `4aba94ab934b545fd21c4759ec31124e3e0158cd` | FASA7909 printed p94/PDF95, **source-verified exact game rule** for market rating bands, prices, Availability, Software Contents Verification; **optional GM guidance** for applications | Program-size derivation from p78; Computer (Programming) successes/extra-success time, Matrix Analyze Icon; market lookup and stepwise information disclosure not code tested. Test specifications only: rating5, size8 Mp → 1,600¥, Availability 4/7 days; 4 successful offline verification successes reveal four listed categories; recheck TN 4→6. |
| Fictional worm programs, infection and variant rules | `rule.matrix.worm-infection-and-variants-p92-94`; `rules/matrix/matrix-fictional-worm-programs-p92-94.yml`; semantic commit `4a065ee368c1b41b83d53dc8c6d9c6cafcd9a645`; blob `053b797934c8659913f756fb2d74c5743435195b` | FASA7909 printed pp92–94/PDF93–95, **source-verified exact fictional Matrix procedures** for file/subsystem/terminal infection, detection/cleanup and 6 named variant outcomes, not a real-world procedural guide | Matrix p82 Glitch Table and p98–99 Disinfect/Infect operations; Computer Test, cybercombat/initiative, hardening and MPCP integration; no executable tests run. Specifications only: worm5 infection file TN5; worm5 vs terminal hardening2 with exactly two successes does not infect; deathworm rating5 → tabletop +2 TN; cleanup TN 4+3−2=5. |

**Administrative indexing:** Both source-reviewed supplements registered in the authoritative `sources/manifests/Matrix.yml`, ordinary GitHub commit `865f66470c26662467f22965b3e229f36a531780`, fresh readback blob `e860f4e0efef3276695004532f6b3ce711320603`. Matrix programming **printed pp76–94 deferred detail remains only partially normalized**; accepted pp78–88 and pp91–92 records reused, no duplicate claim. Scanned coverage: original pp92–94 independently inspected in this run. Normalized record coverage: 2 newly verified and indexed. Code-validated readiness: no new game-engine tests. All statuses per subsystem are separate; no readiness percentage inferred. Denver's independent authoritative boundary remains printed p45/PDF46, next missing p46/PDF47, with no advancement or checkpoint change.


**Duplicate-source reconciliation warning (same run):** A fresh *directory-level* reuse audit discovered `rules/matrix/matrix-program-market-verification-p94.yml` (ID `rule.matrix.program-market-and-verification-tables-p94`, blob `fc3587be644312dfa183cb67f4a16ea415b44eef`, semantic commit `572590a10504537472d24e67c0c0c46459680d58` at 2026-11-10 12:31:21Z) was already accepted **before** this run's p94 write. The current run's `rule.matrix.purchased-software-verification-p94` overlaps its exact numerical price/availability and verification tables, though the new record also carries application guideline/context. **Do not count these as two independent market-rule discoveries or implement both as separate effective rules.** The older accepted record was not listed in the Matrix manifest's `verified_semantic_records` at the time of this audit; its own independent gate/journal/indexing status requires a bounded reconciliation, not invented confirmation. Both files and earlier transaction receipts are preserved; no silent deletion, rewrite, or duplicate promotion is authorized. The newly created record's real GitHub commit/readback/gate receipt remains valid as a separate historical write. New source-normalized record count for this run is two, but genuinely distinct new Matrix mechanic clusters are **one worm cluster plus contextual purchase/applications coverage overlapping an existing numeric market record**.

## November 10, 07:06 CST — recovered Matrix rating limits and indexed pre-existing frame/agent mechanics

**Source and limits:** The original cataloged FASA Corporation *Matrix* (FASA7909), Shadowrun Third Edition, 90,863,077-byte PDF was freshly downloaded from connected Google Drive. SHA-256 `b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe` matched the live source manifest, and `preservation_method.py verify-source` returned a verified original-source hash. Original page images printed p76/PDF77 and pp88–91/PDF89–92 were independently reviewed. First-pass editorial/source-field reviews, local transaction staging, and source gates were run for the two distinct records below; the second existed before this run and was **reused**, not duplicated. Neither is code-validated, and `pending.matrix.range-76-94` remains unresolved.

| Engine subsystem | Canonical ID, provenance | Confirmed receipt | Effective scope / remaining dependency |
| --- | --- | --- | --- |
| Matrix programming limits | `rule.matrix.program-rating-constraints-p76` — `rules/matrix/matrix-programming-rating-constraints-p76.yml`; FASA7909 printed p76/PDF77 | **NEW semantic commit** `8b6160a1ffa548cc47c5fcc15cfedbd89a5a8e52`, blob `0c9a3cdd6c27a46c78c94bc60d8382d27723d8fc`; confirmed `ingestion_gate.py confirm` | **Original supplemental SR3 exact rules, source-reviewed, not code-tested.** Ordinary maximum program rating equals the programmer's Computer (Programming) skill; persona programs use floor(1.5× skill); an effective design rating reduced below 1 is treated as 1 for time and memory. Must combine with existing FASA7909 printed pp78–80 programming formula and any source-specific exception; not a replacement for the parent programming procedure. |
| Frame/agent design and operation | `rule.matrix.frames-agents-design-operation-p88-91` — `rules/matrix/matrix-frames-agents-design-operation-p88-91.yml`; FASA7909 printed pp88–91/PDF89–92 | **Previously accepted semantic commit reused without resubmission:** `c1afd23fc0a4224885a888b35384d44b0b5c5283`, blob `36eb028588d78f6a736c00c28ac7cc4fda5c4187`; independent original-page re-review and `ingestion_gate.py confirm` completed for recovery | **Original optional Matrix exact rules, source-reviewed, not code-tested.** Frame/agent programmer caps, frame points, persona allotments, Pilot, utility payload, initiative, Hacking Pool, command/control and Security Tally. Requires linked Program Size Table, program-option compatibility, core Matrix action economy and the source's Comprehension difficulty lookup before a full executable implementation. |

**Verified administrative registration:** `sources/manifests/Matrix.yml` now includes both previously unindexed IDs, commit `0ccfae926161e316f71deb72609df530ca97f6e5`, exact readback blob `135ec2396d854ee1714bb22b3f881ba2f8c5249a`. Verified supplemental registrations increased **9 → 11**; this is *not* two new semantic commits and *not* two newly completed contiguous printed pages. The accepted duplicate p94 market record flagged earlier remains a consumer-selection issue, not a newly discovered second price table.

**Illustrative executable test specifications (UNRUN):** programmer skill 4 ⇒ ordinary program rating maximum 4; programmer skill 5 ⇒ persona rating maximum 7; effective rating reduced to 0 ⇒ design-time and memory computation uses rating 1; frame designer skill 8 ⇒ dumb/smart/agent core caps 16/12/8; agent core 8 ⇒ 48 Frame Points, 16 persona attribute points, Hacking Pool 8; agent with four extra initiative dice costs 12 Frame Points, giving a total of 5D6. All depend on the published game's own source and cross-reference rules; passing a future adapter test will not substitute for separate canonical-source and transaction gates.

**Boundaries:** Matrix programming printed pp76–94 remains a targeted normalization/reconciliation obligation. The Denver FASA7212 authoritative printed p45/PDF46 boundary is unchanged, with printed pp46–47/PDF47–48 missing and no replacement search. The original single hourly worker remains the only worker. No other source manifest, checkpoint, or edition rule was promoted. Separate scanned, canonical normalized, and code-tested states remain unmerged.


## SSG Game Information optional Matrix and identity-test recovery — November 10, 08:04 CST

This section indexes **two independently source-reviewed, newly verified semantic GitHub records**, both using original *Sprawl Survival Guide* by FanPro (FanPro10667, Shadowrun Third Edition), rather than inferring mechanics from scan coverage. Fresh original PDF SHA-256 `b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f` matched the main source manifest; printed pp123–127/PDF124–128 were inspected from original page images. Both records passed candidate immutability preflight, transaction staging, normal GitHub contents write, exact blob readback, and `ingestion_gate.py confirm`. Source-fidelity judgement is separate from structural gate confirmation.

| Engine lane / status | Canonical record path and source range | Actual gate receipt | Needed next |
| --- | --- | --- | --- |
| Fictional credstick authentication/reader/Matrix *optional tabletop game procedures*, code untested | `rules/matrix/ssg-fictional-credstick-system-tests-p123-125.yml`, FanPro10667 pp123–125/PDF124–126 | commit `88fb5ac5ca54e283ea1327ee57a5add7e50c3d9b`; blob `422da7dc1f38a880ef3c64f4c44a64be34a0ced4`; gate verified | Implement isolated, source-specific dice TN table and reader outcomes; retain core encryption/Electronics dependencies and no real-world applicability. |
| Fictional optional ID-creation and ID Edge/Flaw checks, code untested | `rules/identity/ssg-fictional-id-creation-options-p125-127.yml`, FanPro10667 pp125–127/PDF126–128 | commit `108ae8b1a0d13592b49ae1d1cdd51fefa8c17936`; blob `66cde561d2a93485f496b8a072507f30291aabf6`; gate verified | Implement optional source-specific target number, game-time, contacts, nuyen and ID rating; retain ambiguity on Deterioration scheduling; regression tests needed. |

**Existing-record reuse:** `rule.matrix.ssg-dataterm-host-sheaf-p120`, `equipment.ssg-household-drone-tables-p122`, `reference.economy.ssg-common-costs-p124` were already registered; no duplicate submissions. The SSG manifest now indexes five postscan supplements, but `full_game_info_p118_126_deferred_normalization_resolved: false` is intentionally preserved. This does not resolve every Game Information content class, advance Denver, pass the source-completion gate, or certify executable code readiness. No game-engine unit tests were executed in this ingestion run.

**Executable test-vector specifications (not executed):** credstick gold test TN 14 and ebony TN 18; fictional Counterfeiting rating 4 adjusts base TN 12 to 8; optional ID rating 4 with three contacts and two successes uses TN 9, 25 days and 1,600 fictional nuyen; Home Turf rating 3 rounds up to local rating 5; Limitation rating 1 automatically fails in its designated jurisdiction; Expiration Date with rating 3 and D6 result 4 is 12 fictional months.

## November 10, 08:31 CST — SSG home telecom and domestic-drone command recovery

The original connected Google Drive PDF for **FanPro, Sprawl Survival Guide (FanPro10667), Shadowrun Third Edition** was freshly reacquired and the actual preservation_method.py verify-source command reported matching source SHA-256 b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f. Original printed pp118–121/physical PDF119–122 were independently inspected, with first-pass review of source assertions and nested candidate fields. Two frozen baseline/same-substance candidates passed actual local transaction_recovery.py stage / ingestion_gate.py prepare, ordinary GitHub contents writes, fresh exact blob readbacks and ingestion_gate.py confirm. These receipts do not prove independent engine implementation or complete game-information coverage.

| Engine dependency | Canonical record/source and designation | Verified GitHub receipt | Unresolved consumer obligation |
| --- | --- | --- | --- |
| Household telecom components / public dataterm equipment | equipment.ssg-home-telecom-public-dataterm-p118-121; equipment/ssg-home-telecom-public-dataterm-p118-121.yml; FanPro10667 printed pp118–121/PDF119–122; original fictional published equipment statistics, source-reviewed, **not code-tested** | New semantic commit 7eb3f009058ede6f19b8251cc0667f8a0240d7cf; readback blob 599bbd1c4fab9d654b96c02a89162759ed1969c9; local gate verified | Optional Blue-4 telecom host with source ACIFS 8/8/6/6/6, Probe-2 and GM substitution; public dataterm booth Maglock-4, Barrier-8, credstick reader Rating-1, anti-tamper Rating-6. Already accepted rule.matrix.ssg-dataterm-host-sheaf-p120 has the host trigger table: **reuse, do not duplicate**. Example specification only (UNRUN): basic telecom Blue-4/Probe-2, public terminal reader 1. |
| Optional domestic drone command/control package | rule.ssg-domestic-drone-command-p120; rules/matrix/ssg-domestic-drone-command-p120.yml; FanPro10667 printed p120/PDF121; original optional fictional tabletop rules, source-reviewed, **not code-tested** | New semantic commit 98a6dbb98ffbd980c7a22d92143e2c5e166c95e8; readback blob 6ad99450fdbd2467ca9c3e245135092429dc1b85; local gate verified | Original optional components: Matrix wireless link, remote-control utility and Rigger 3 emulation module. Consumer-grade components typically Rating 1 or 2. Basic scheduled tasks/diagnostics are described without new target numbers. Example specification only (UNRUN): three named components and typical ratings in {1,2}; linked source-specific operations still need engine tests. |

**Administrative indexing:** sources/manifests/SprawlSurvivalGuide.yml contains these 2 new supplements alongside 5 previously accepted distinct registrations. Ordinary GitHub manifest commit b8060a3443b72ea88083c764ac9df864009ab3bc and exact readback blob 567d93db73b654565dc72bfba0216e865c75ff2c were verified. The manifest flag full_game_info_p118_126_deferred_normalization_resolved: false is preserved; do **not** mark all printed pp118–126 closed. Scanned coverage, independently normalized record coverage and code-validated readiness are different criteria. No game-engine tests were run.

**Pass B independence:** Denver FASA7212 remains authorized only through printed p45/PDF46, pending its missing printed pp46–47. No Denver manifest/checkpoint changes, contiguous-page authorization, source completion or automation schedule change.
