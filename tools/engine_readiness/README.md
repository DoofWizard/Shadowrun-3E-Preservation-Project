# Source-linked SR3 mechanics probe (developer checkpoint)

This directory is a **small, deliberately incomplete** executable sanity test for accepted rules from the fictional tabletop RPG *Shadowrun, Third Edition* (FASA Corporation, FASA7001). It does not reproduce the sourcebook's prose, function as a complete game, replace the source corpus or certify all source mechanics.

Run from repo root with Python 3.10+:

```bash
python -m unittest discover -s tools/engine_readiness -p 'test_*.py' -v
```

The 22 deterministic test vectors exercise existing canonical records:

| Tested behavior | Canonical source | Book page |
| --- | --- | --- |
| Individual-die success counting, target floor, Rule of One and Rule of Six | `rules/tests/{making-tests,target-numbers,rule-of-one,rule-of-six}.yml` | FASA7001 p38 |
| Reaction + ordinary initiative dice, 10-point initiative passes | `rules/initiative/{initiative,initiative-passes}.yml` | FASA7001 pp42,102 |
| General opposed-test tie vs special melee-exchange tie | `rules/tests/opposed-test.yml`, `procedures/combat/melee-attack.yml` | FASA7001 pp39,122–123 |
| Two-net-success Damage Level staging | `rules/combat/damage-staging.yml` | FASA7001 pp113–114 |
| Source-reviewed clip, break, magazine, cylinder and belt reload actions | `procedures/firearms/sr3-core-ammunition-reloading-p280.yml` | FASA7001 p280/PDF289 |

**Deliberate fail-closed boundaries:** tie-breaking inside initiative needs `rules/initiative/initiative-ties.yml`; the printed p280 ammunition belt Quickness/2 table does not itself state rounding for odd Quickness, so this probe raises `UnresolvedRule`; damage staging beyond the basic L/M/S/D level range requires the full rules and condition monitor; no open-test, magic, Matrix, social, cyberware or complete combat encounter implementation is claimed.

**Readiness categories:** `record_exists` ≠ `source_verified` ≠ `normalized_exact` ≠ `cross_source_reconciled` ≠ `code_tested`. This executable probe only tests the specific documented slices listed above; it does not establish broad engine implementation readiness.

See `docs/engine-readiness/MECHANICS_READINESS_24H_2026-11-09.md` and the relevant original source manifests. For any new mechanic, preserve precise source edition/page, author an original-page-reviewed record and complete the established transaction gates before referencing the record as authoritative. Do not modify the preservation worker.
