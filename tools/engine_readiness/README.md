# Source-linked SR3 mechanics probe (developer checkpoint)

This directory is a **small, deliberately incomplete** executable sanity test for accepted rules from the fictional tabletop RPG *Shadowrun, Third Edition* (FASA Corporation, FASA7001). It does not reproduce the sourcebook's prose, function as a complete game, replace the source corpus or certify all source mechanics.

Run from repo root with Python 3.10+:

```bash
python -m unittest discover -s tools/engine_readiness -p 'test_*.py' -v
```

The 40 deterministic regression vectors cover a limited source-reviewed portion of existing canonical records and new bounded consumer adapters:

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

**Deliberate fail-closed boundaries:** `initiative_passes()` still rejects ties unless the caller separately applies the new **two-actor** `initiative_tie_winner()` adapter; multi-actor ties and voluntary delays are not implemented. The printed p280 ammunition belt Quickness/2 table does not itself state rounding for odd Quickness, so the probe raises `UnresolvedRule`. Ranged attack outcome assumes the caller already resolved attack/dodge/Body dice and their target numbers; it does not calculate weapon Power, armor, Combat Pool availability or the Condition Monitor. No open-test, magic, Matrix, social, cyberware or complete encounter implementation is claimed.

**Core source mapping verified:** early core printed pp54, 102 and 113 appear at physical PDF pp55, 103 and 114 respectively; later printed pp275–282 appear at PDF pp284–291. Do **not** apply a single fixed offset across the whole book. The source manifest separately documents an unresolved p307→p309 scan discontinuity (possible absent printed p308).

**Open canonical normalization:** the master character-creation table's numeric values are implemented in a **source-checked consumer adapter**, but the existing `rules/character-creation/priority-system.yml` describes the table without encoding those numbers. It still needs ordinary source-reviewed canonical record staging and gate confirmation. Likewise verify the p113 damage boundaries and all deferred core tables against the authoritative canonical record set; a passing adapter test is not an ingestion authorization.

**Readiness categories:** `record_exists` ≠ `source_verified` ≠ `normalized_exact` ≠ `cross_source_reconciled` ≠ `code_tested`. This executable probe only tests the specific documented slices listed above; it does not establish broad engine implementation readiness.

See `docs/engine-readiness/MECHANICS_READINESS_24H_2026-11-09.md` and the relevant original source manifests. For any new mechanic, preserve precise source edition/page, author an original-page-reviewed record and complete the established transaction gates before referencing the record as authoritative. Do not modify the preservation worker.
