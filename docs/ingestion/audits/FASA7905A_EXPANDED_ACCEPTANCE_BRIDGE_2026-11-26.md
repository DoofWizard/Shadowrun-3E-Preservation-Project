# FASA7905a / Shadowrun Companion — accepted-core equivalence handoff

**Purpose:** Remove one demonstrable sourcebook-certification bottleneck without inventing historic receipts, changing canonical source rules, or declaring the full rules corpus complete. This is a *read-only engineering and independently reviewed evidence handoff*, **not** a book acceptance receipt.

## Actual original-source and repository evidence

- Original FASA7905a *Shadowrun Companion* PDF: **138 physical pages**, SHA-256 `8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5`. The original image of **printed p130 / physical PDF131** was opened and examined for this handoff.
- The p130 Actions appendix explicitly references several source families: SR3, *Virtual Realities 2.0*, *Magic in the Shadows* and Critters from the SR3 gamemaster screen. Therefore **150 shared action references are not 150 core-rule equivalents**, and earlier-edition rules must not be silently converted.
- Live `sources/manifests/SRComp.yml` owner-authored finite checklist: **187 action labels** (Free 36, Simple 48, Complex 103); **37 source-owned exact bindings**, **150 other source/shared receipt links**, **zero unmapped shared rows**. These are inventory coverage claims, not historical receipt recovery or formal acceptance.
- That manifest's existing `srcomp_book_closure_checklist_2026_11_25.actions.shared_core_row_bindings` documents **38 present-day core matches**, of which **27 literal action labels** and **11 qualified/nonliteral rows** require independent meaning/scope review. Group mapping: Free General 7; Free Combat 3; Simple General 5; Simple Combat 8; Complex General 2; Complex Combat 3; Free Magic 1; Simple Magic 3; Complex Magic 5; Complex Rigging 1. These are **recorded owner comparisons**, not 38 newly certified source comparisons in this handoff.
- The two existing shared-core targets are `rules/actions/sr3-core-combat-phase-action-timing-p104-108.yml` (original source-specific Git blob `87371b67cf6ac9e57ffd276d44713eaa3cdafcfd`) and `rules/cyberware/sr3-core-muscle-reaction-wired-reflexes-p301.yml` (blob `e7f0ba6f6738a0fe7d16dc5406dd4df095766be9`). Exact committed/current target blobs were checked via GitHub source reads.
- The genuine FASA7001 accepted-core receipt is `references/audits/fasa7001-available-source-mechanical-core-acceptance-confirmed-2026-11-21.json` at commit `6baeb5dffd92dbdcbe50aa451d637e8ae9702316`, Git blob `d11888c9f20b5603f874f4e976dff3e23c8cde98`, `status: verified_core_acceptance`. Its **historical source-manifest blob** is `a79b28a3970668982ef44a5318642ed55848839a` and **historical obligation-queue blob** is `366ee748f51dbf2b699a26edbc1215352743191d`. Those exact blobs were independently fetched at the receipt commit and match the receipt. **Current** SR3 manifest and queue are legitimately newer; a proof must use the *accepted snapshot*, not mistake current differences for historical fraud.
- Original FASA7001 PDF SHA-256 `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`; the accepted core packages **15 sections, 451 indexed records and 1,010 field bindings**. Original printed p104/PDF105 also inspected directly during this handoff.

## Implemented changes (normal GitHub Contents writes)

1. `tools/expanded_acceptance/core_equivalence.py` implements **`sr3-accepted-core-equivalence/v1`**: requires the actual historical accepted-core receipt and snapshot, exact original source/edition, a unique indexed core record and substantive `/data/` field, byte-exact *historical and current* target rule data, typed source-value identity, and a separately reviewed exact-restatement comparison for scope, conditions, exceptions, units and optional status. It does **not** silently equate SR2 material, conflicting values or partial/narrower scopes.
2. `tools/expanded_acceptance/validator.py` now routes an explicitly opted-in accepted-core field to the above proof checker, while leaving all original source-local historical journal and split-archive gates intact. Accepted-core reused fields are omitted from the source-local **duplicate** historical `prepare` loop. The output records `accepted_core_match_candidates` separately from source-local records. All paths still require an independent full original-page inventory and the real source PDF. This is a **candidate** verifier, not a formal acceptance action.
3. `tools/expanded_acceptance/blocker_triage.py` now distinguishes an explicit accepted-core proof from unreviewed external equivalence and does not demand an invented Companion historical receipt for an already accepted FASA7001 target. An absent accepted-core receipt, exact obligation or independently reviewed comparison still produces named blockers.
4. `.github/workflows/sr3-expanded-acceptance-contract-tests.yml` is committed for future pushes/PRs and exercises existing expanded-acceptance integration, archive, negative and core-equivalence tests. **No GitHub Actions run conclusion was independently retrieved for this handoff.**

## Execution receipts and limitations

- **17/17** `test_core_equivalence.py` local synthetic tests passed, including wrong source edition, altered current accepted-core bytes, fake or unindexed acceptance receipts, wrong typed field, wrong core obligation, unreviewed exceptions and missing independent original-image comparisons. Exact GitHub module blob: `009a305bec2c30dd91dfd5693f337f9cce759e77`; exact GitHub test blob `6db98954ef4c050a3c1c03380f851767305c9349`.
- **14/14** `test_blocker_triage.py` local synthetic tests passed after accepted-core mode support. Exact committed module blob `e5757595a0c910dc56b14efff770cb84ab4317e0`; test blob `f09a83159a586ef366506ce7db82b65ee95dd6c1`.
- Full current repository integration and the new GitHub CI workflow **were not independently executed/observed in this handoff**; do not claim 31 tests are equivalent to sourcebook certification.
- This handoff has **no newly formalized Companion row acceptance**, no recovered historical prewrite/confirm/index receipts, no modified source semantic record, no revised SR3 effective precedence, and no Denver or global page advancement.

## Concrete next acceptance operation

**Owner: existing SR3 Expanded Rules Acceptance worker; independent decision: existing Pass B coordinator.** Reuse the existing 138-page/18-scope Companion original inventory as a *starting review*, not an automatically independent, fully complete `validator.py` input. Construct a separately pinned original-derived `review.json` (every PDF page and original field), `bindings.json` and `evidence.json` with authenticated original transaction artifacts. For 38 previously mapped core rows, distinguish the **27 literal candidates** from **11 qualified nonliteral rows**; supply one exact core-accepted `obligation ID` and full source/target original-page comparison for each **truly identical** row. Run `blocker_triage.py` to identify all outstanding inputs in one execution, then run the full real `validator.py` with the freshly obtained original PDF and pinned Git commit. Leave any qualified, discrepant, optional or 2E-derived row blocked until independently adjudicated; for Critters, MiTS, Matrix, rigging and other sources use their own accepted snapshots and actual historical receipts, not the accepted-core shortcut.

The coordinator must issue an explicit book-level authorization using the existing rules and valid evidence, or produce a precise BLOCKED result. **Even a validator candidate PASS does not auto-certify the sourcebook.** Never invent historic journal files, implied source reviews, blank-page dispositions, semantic writes or new page credit.


## Accepted-core inventory granularity: verified gap

A second read-only audit queried the **historical FASA7001 closure queue at the original verified acceptance commit** `6baeb5dffd92dbdcbe50aa451d637e8ae9702316`, not the newer working queue. That accepted inventory contains these exact obligations for the two canonical core records used by the Companion p130 comparison:

- `rule.actions.sr3-core-combat-phase-action-timing-p104-108`: `/data/turn_sequence`, `/data/action_economy` and the **complete** `/data/selected_free_actions` group.
- `rule.cyberware.sr3-core-muscle-reaction-wired-reflexes-p301`: `/data/muscle_replacement`, `/data/reaction_enhancer`, `/data/wired_reflex_system`.

**Critically, those specific accepted obligations do not contain** `/data/selected_simple_actions`, `/data/selected_complex_actions`, or `/data/reflex_trigger` even though the underlying original-edition canonical files contain the actual structured data. This is an **acceptance-field inventory/evidence gap**, *not* proof that those rules are absent from the repository.

The source owner's **38 mapped core row candidates** split by action class as follows:

| Class | Mapped candidates | What the above accepted snapshot permits |
| --- | ---: | --- |
| Free (General 7, Combat 3, Magic 1) | **11** | Potential accepted-*group* descendant proofs under `/data/selected_free_actions`, but each still requires authentic independent original-page comparison, typed equality, exact field pointer, context and source scope verification |
| Simple (General 5, Combat 8, Magic 3) | **16** | The shared `selected_simple_actions` group is **not a named accepted obligation** in this accepted snapshot; do not certify it by an unrelated `action_economy` field |
| Complex (General 2, Combat 3, Magic 5, Rigging 1) | **11** | Same problem for `selected_complex_actions`; use independently accepted equivalent source binding or obtain a distinct source-reviewed/authorized group addendum, never rewrite the historical core acceptance |
| **Total** | **38** | **At most 11** candidates currently have an identified source-accepted parent group; zero automatically certified |

The separate **27 literal-label / 11 qualified-label** split is a *different classification* of the same 38. A literal label match does **not** establish identical rule conditions, exceptions, source scope, edition or optional status.

The revised `core_equivalence.py` accepts a nested substantive field only when its JSON pointer descends from the **precisely accepted** group pointer and an independently reviewed comparison names the accepted parent group, exact subfield pointer and original core group review locator. Nonmembers, unreviewed descendants and unaccepted groups remain BLOCKED. Tests increased from **17/17 to 20/20 locally passing**, with matching GitHub source blob `105b434a047d8e1203185d08ebc28d0c599421fb` and test blob `73d9a061e14f07e24f10bbabfb6b5d4753c7f1ff`. Main validator integration remains committed but was not independently run end-to-end in this handoff.

Original printed Core p105/physical PDF106 was also directly inspected alongside Companion p130/PDF131: the core explicitly lists the relevant Free Actions with their conditions. That original source comparison supports pursuing the 11 Free candidates; it does **not** replace independent per-row certification.

**Immediate owner action:** Finish those 11 Free-row original comparisons against the accepted group (or explicitly block discrepancies). For the other 27, find *other already accepted original-source obligations* that cover the exact typed action-field and conditions, or prepare independently original-reviewed **supplementary accepted obligations** through the authorized source-specific process. Do not fabricate or mutate the November 21 core receipt. The coordinator decides acceptance after independently checking every source-specific comparison, chronology and historical record. Other 112 shared sourcebook rows and the overall 150 historical receipt references remain separate work.
