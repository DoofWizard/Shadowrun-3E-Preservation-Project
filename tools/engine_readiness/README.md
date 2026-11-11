# Source-linked SR3 mechanics probe (developer checkpoint)

This directory is a **small, deliberately incomplete** executable sanity test for accepted rules from the fictional tabletop RPG *Shadowrun, Third Edition* (FASA Corporation, FASA7001). It does not reproduce the sourcebook's prose, function as a complete game, replace the source corpus or certify all source mechanics.

Run from repo root with Python 3.10+:

```bash
python -m unittest discover -s tools/engine_readiness -p 'test_*.py' -v
```

The original deterministic regression vectors (extended below) cover a limited source-reviewed portion of existing canonical records and new bounded consumer adapters:

| Tested behavior | Canonical source | Book page |
| --- | --- | --- |
| Individual-die success counting, target floor, Rule of One and Rule of Six | `rules/tests/{making-tests,target-numbers,rule-of-one,rule-of-six}.yml` | FASA7001 p38 |
| Reaction + ordinary initiative dice, 10-point initiative passes | `rules/initiative/{initiative,initiative-passes}.yml` | FASA7001 pp42,102 |
| General opposed-test tie vs special melee-exchange tie | `rules/tests/opposed-test.yml`, `procedures/combat/melee-attack.yml` | FASA7001 pp39,122–123 |
| Two-net-success Damage Level staging | `rules/combat/damage-staging.yml` | FASA7001 pp113–114 |
| Source-reviewed clip, break, magazine, cylinder and belt reload actions | `procedures/firearms/sr3-core-ammunition-reloading-p280.yml` | FASA7001 p280/PDF289 |
| Exact priority A–E attribute, skill and nuyen budgets, baseline race/magic priority restrictions | `rules/character-creation/priority-system.yml` plus `core_extensions.py` (consumer adapter, not an archival record) | FASA7001 p54/PDF55, p55/PDF56 |
| Initiative ties: first-pass score, adjusted/natural Reaction, repeated d6 | `rules/initiative/initiative-ties.yml` plus `core_extensions.py` | FASA7001 p102/PDF103 |
| Ranged outcome: Dodge > attack is complete dodge; otherwise add dodge to resistance | `rules/combat/dodge-test.yml`, `rules/combat/damage-staging.yml`, `core_extensions.py` | FASA7001 p113/PDF114 |
| Damage staging boundaries: above Deadly stays Deadly; below Light = no damage | `rules/combat/damage-staging.yml`; executable correction in `rules_probe.py` | FASA7001 p113/PDF114 |
| Condition Monitor: L/M/S/D = 1/3/6/10 boxes, separate Physical/Stun tracks, Stun-to-Physical overflow, cumulative wound modifiers, Body death threshold | `rules/condition/condition-monitor.yml` (general canonical anchor), `condition_core.py` (bounded source-checked executable adapter) | FASA7001 pp125–126/PDF126–127 |
| Integration vectors: starting character → scripted success tests → ranged attack outcome → Condition Monitor damage and penalties | `test_core_integration.py` (consumer harness only) | FASA7001 pp38,54,113,125–126 |

**Deliberate fail-closed boundaries:** `initiative_passes()` still rejects ties unless the caller separately applies the new **two-actor** `initiative_tie_winner()` adapter; multi-actor ties and voluntary delays are not implemented. The printed p280 ammunition belt Quickness/2 table does not itself state rounding for odd Quickness, so the probe raises `UnresolvedRule`. Ranged attack outcome assumes the caller already resolved attack/dodge/Body dice and their target numbers; it does not calculate weapon Power, armor, or Combat Pool availability. The separate `condition_core.py` adapter applies final staged damage boxes and baseline incapacitation, **not** advanced healing, action interrupts, or Man & Machine p131's additional consciousness mechanics. No open-test, magic, complete Matrix system-operation/intrusion, social, cyberware or complete encounter implementation is claimed.

**Core source mapping verified:** early core printed pp54, 102 and 113 appear at physical PDF pp55, 103 and 114 respectively; later printed pp275–282 appear at PDF pp284–291. Do **not** apply a single fixed offset across the whole book. The source manifest separately documents an unresolved p307→p309 scan discontinuity (possible absent printed p308).

**Consumer-code-only status:** `core_extensions.py` and `condition_core.py` derive executable calculations from source-reviewed original pages, but they are **not** canonically normalized records and no archival transaction receipt or source manifest advancement is claimed for those new adapters. The source is FASA7001, original PDF SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`.

**Updated canonical source linkage (2026-11-10):** The formerly missing exact numeric master-priority table and Condition Monitor table have now been separately source-reviewed, accepted, confirmed and indexed as `rules/character-creation/sr3-master-priority-numeric-p54.yml` (FASA Corporation, *Shadowrun Third Edition*, FASA7001, printed p54/PDF55; commit `c6f4dfc6c5125d61a087ec4fe488773d2566c939`) and `rules/condition/sr3-damage-monitor-numeric-p125-126.yml` (FASA7001 printed pp125-126/PDF126-127; commit `d8569cc0f7c80c25e2a067db21ca4cfff7aff5bf`). The bounded `core_extensions.py` and `condition_core.py` remain consumers, not archival receipts. Verify the effective links and p113 damage boundaries within the eventual engine, then separately reconcile still-deferred core tables, p308 source anomaly, optional supplements, and code test coverage. This README update is documentation only and authorizes no page advancement.

**Readiness categories:** `record_exists` ≠ `source_verified` ≠ `normalized_exact` ≠ `cross_source_reconciled` ≠ `code_tested`. This executable probe only tests the specific documented slices listed above; it does not establish broad engine implementation readiness.

See `docs/engine-readiness/MECHANICS_READINESS_24H_2026-11-09.md` and the relevant original source manifests. For any new mechanic, preserve precise source edition/page, author an original-page-reviewed record and complete the established transaction gates before referencing the record as authoritative. Do not modify the preservation worker.

## Verified consumer-code checkpoint — 2026-11-10 (FASA7001 original, not semantic ingestion)

Independent local source check: freshly downloaded Google Drive FASA Corporation *Shadowrun, Third Edition* core source **FASA7001** matched SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914` through the actual repository `preservation_method.py verify-source` command. Original source images were inspected for printed p111/PDF112, p279/PDF288, and p307/PDF316. Printed p308 remains absent between core p307/PDF316 and p309/PDF317; no source page or fact was fabricated.

The locally executed test command `python -m unittest discover -s tools/engine_readiness -p 'test_*.py' -v` passed **129/129 tests** (79 existing + 50 new), with Python compilation passing for three new bounded adapters. All 29 original connector-preflight self-tests also passed. These are **consumer executable tests**, not GitHub ingestion gates or verification of a fully implemented game.

| Newly executable bounded adapter / tests | Existing source-reviewed canonical record(s) | Source-specific implementation boundary |
| --- | --- | --- |
| `vehicle_mounts_core.py` + `test_vehicle_mounts_core.py`: 25 vectors | `rule.vehicles.sr3-core-original-mounts-p307` / `rules/vehicles/sr3-core-original-mounts-p307.yml` | Original FASA7001 p307/PDF316: point capacity, hardpoint vs firmpoint, mini/full turret, installation TN/base time, side-fire handling plus required Crash Test, exact even recoil halving, Signature only where explicitly sourced, and aircraft missile racks up to Body and 300kg each. Odd recoil rounding, unresolved Signature cases, Rigger 3 lineage, launch control and water-cannon mode conflict stay fail-closed |
| `firearms_ammo_core.py` + `test_firearms_ammo_core.py`: 11 vectors | `rule.firearms.sr3-core-ammunition-class-compatibility-p279` / `rules/firearms/sr3-core-ammunition-class-compatibility-p279.yml` | FASA7001 p279/PDF288 and Weapon Range Table p111/PDF112: class matching and explicit shotgun pistol/rifle ammo compatibility; no guessed caliber, weapon model, ammunition TYPE or unknown-class conversions |
| `weapon_range_core.py` + `test_weapon_range_core.py`: 14 vectors | `rule.combat.range-target-number` / `rules/combat/range-target-number.yml` | FASA7001 p111/PDF112: 13 numeric firearm/heavy-weapon rows and exact Short/Medium/Long/Extreme base TNs 4/5/6/9; source-linked integration into existing ranged outcome + Condition Monitor. Grenade/missile minimum-range rules, STR-scaled thrown weapons, unique weapon-model exceptions and Cannon Companion additions stay outside this adapter |

**Edition lineage constraint:** Original FASA7001 vehicle mounts must not silently be replaced by FASA7910 *Rigger 3* or newly recovered FanPro10662 *Rigger 3 Revised*. A short-barrel Defiance T-250 can use heavy-pistol *range* per FASA7001 p279 while still sharing shotgun *ammunition*; the code explicitly keeps range identity separate from ammo class. No new semantic record, source status or administrative boundary was claimed or advanced. Denver FASA7212 continues to require missing printed pp46–47, and the existing hourly task remains unmodified.

## Additional bounded programming consumer — Matrix FASA7909, Third Edition (2026-11-10)

A new **noncanonical** pure-Python adapter, `matrix_programming_core.py`, implements only the printed numerical procedures independently checked in original FASA Corporation *Matrix* (FASA7909, Shadowrun Third Edition) printed pp76 and 78–80, physical PDF77 and 79–81, SHA-256 `b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe`. Printed **p77/PDF78 is full-page illustration**, so it is not an untranscribed numerical rules page. Canonical inputs already exist at `rules/matrix/matrix-programming-rating-constraints-p76.yml` and `rules/matrix/matrix-programming-size-plan-suite-team-p78-80.yml`; this code **does not create semantic ingestion records**, does not close Matrix's explicit complete-pp76–94 normalization deferral and does not advance Denver.

The bounded adapter checks original rating/multiplier tables, program/suite size, planning hours/memory/TN, required program memory, programming modifier TN, successful and failed task periods, and permitted team limits/averages. It refuses unsupported rating/multiplier ranges, team sizes, impossible 2D6 totals and zero-success success claims. A caller remains responsible for effective program options, correct utility size multipliers, active/stored memory, eligibility of complimentary dice/host environments, and all actual Matrix operations.

**Verified readbacks:** adapter commit `b60941258488741448da566439485dbd067f1f20`, blob `2094aa512e78b8633d549b9229ff46e0f46338eb`; tests `test_matrix_programming_core.py` commit `8edc56c0f0038edc965d932ae249f92617d4ba56`, blob `7d63a88b95ca1214deba9c70bb410ab49f4ddd43`. Both readbacks matched the exactly locally tested bytes.

**Local regression receipt:** The original prior **58-test core archive** together with **24 new Matrix tests** ran as `python -m unittest discover -s engine_harness -p 'test_*.py' -v` and produced **82/82 pass, zero failures**. This was a bounded copied-code run, **NOT** execution of the larger current repository's entire test suite; the prior README's separately reported 129 tests are a different historical run. The compact inventory at `docs/engine-readiness/SR3_CORE_EXECUTABLE_READINESS_V0.json` distinguishes scan, confirmed canonical records and executable coverage. The existing single ingestion worker, source manifests, Denver p45/PDF46 boundary and checkpoint were left unchanged.

## Optional fictional ID resolution — FanPro10667 (2026-11-10)

The original Google Drive PDF of FanPro's *Sprawl Survival Guide* (Shadowrun Third Edition, FanPro10667), SHA-256 `b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f`, passed the repository's actual `preservation_method.py verify-source` check against the current source manifest. Original printed pp125–127/PDF126–128 were independently inspected. Reused **accepted** canonical record `rule.identity.ssg-fictional-id-creation-options-p125-127` at `rules/identity/ssg-fictional-id-creation-options-p125-127.yml`; no semantic duplication, new source-transaction receipt, deferral closure, or Denver page advancement.

New consumer-only `ssg_identity_core.py` and `test_ssg_identity_core.py` implement/test the game's optional fictional-ID rating test, contact deficits, nuyen costs, successes and zero-success elapsed time, GM's optional 1D6 Edge/Flaw assignment, additive 20% purchasing modifiers, Home Turf and Limitation rounding with the rating-1 failure, and ID Expiration Date. **21 targeted local unit tests passed**, including source example Rating 4, three contacts, two successes → TN 9, 25 days, 1,600 fictional nuyen. Exact fractional results remain fractional instead of inventing rounding; the ambiguous Deterioration interval fails closed. This tests only a consumer's specified arithmetic, not identity creation in real systems or a functioning Matrix engine.

**Readiness matrix:** source scan *previously reported complete*; exact canonical normalization *verified for this specific ID subsystem only*; consumer code *21 local tests passed*; cross-system Matrix/SR3 integration *not tested*; overall Game Information pp118–126 deferred normalization *still open*. The authoritative `sources/manifests/SprawlSurvivalGuide.yml` and Denver `sources/manifests/Denver.yml` remain unchanged by this checkpoint.
