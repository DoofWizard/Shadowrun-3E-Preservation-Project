# FASA7905a p130 — three apparent Free Action discrepancies resolved as source-index references

**Disposition:** Original-page classification established for three references; **not** a new semantic rules transaction, 3 formally accepted rows, a book-level acceptance decision, or restored historical journal evidence. Retain the detailed accepted SR3 conditions. Additional independent reviewer/custody and full-source authorization remain required for the production acceptance validator.

## Exact original-source inspection

| Publication | Source | Original inspected | Original PDF SHA-256 | Page image from the verified PDF |
| --- | --- | --- | --- | --- |
| *Shadowrun Companion*, FASA Corporation, SR3, FASA7905a | `source.srcomp` | printed p130 / physical PDF131 | `8c52409108459a130ff6292722d98dc1f7a65cf870e63a363c34dc1dc299afd5` | SHA-256 `531ff51e2c6d9200602f7cfa1d9aba2cf54c51cb16e24cf04e5b489f25fb54c2` |
| *Shadowrun, Third Edition*, FASA Corporation, FASA7001 | `source.sr3-core` | printed p105 / physical PDF106 | `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914` | SHA-256 `1d518ebd9fa1c846b5473ab72756d5f93ed3c8d5826cced7acee0bddce0726eb` |

Original PDFs directly re-opened and SHA-256 compared to live original-source manifests. Companion is 138 physical pages; SR3 Core is 345 physical pages. Both original images directly read. The Companion's one-page **Actions** section expressly introduces itself as a list of actions whose detailed rules are described in several other publications, including SR3. It has Free, Simple and Complex headings and categories, not a new procedure for each line.

## Three source-specific findings

| Companion printed p130, Free → General | Accepted SR3 core printed p105 rule | Why this does not create a rule contradiction |
| --- | --- | --- |
| `free.general[1]` **Activate Cyberware** | `/data/selected_free_actions/8/action` + adjacent `condition` | The appendix is an abbreviated label. SR3's Free Action applies to cyberware that requires activation rather than continuous control; the appendix does not independently lift that prerequisite |
| `free.general[6]` **Observe** | `/data/selected_free_actions/7/action` + adjacent `condition` | The core limits the Free Action to immediately obvious information. Detailed perception is a separate Simple Action, also distinctly identified in the Companion index |
| `free.general[7]` **Speak a Word** | `/data/selected_free_actions/12/action` + adjacent `condition` | The appendix provides the action class only. SR3's conversational and GM-discretion qualifications remain in force; it does not grant unrestricted speech during a Free Action |

The three *condition discrepancies* reported by the earlier acceptance review are therefore **index abbreviation versus full-rule detail**, not demonstrated opposing mechanical values. Preserve their original labels and exact Free Action class without creating new optional exceptions or a competing action cost. If later source evidence shows an actual exception, reopen that field with exact evidence instead of forcing equivalence.

## Actual accepted-core provenance, not an inferred link

- Verified accepted core receipt: `references/audits/fasa7001-available-source-mechanical-core-acceptance-confirmed-2026-11-21.json`, original historical Git commit `6baeb5dffd92dbdcbe50aa451d637e8ae9702316`, blob `d11888c9f20b5603f874f4e976dff3e23c8cde98`, status `verified_core_acceptance`.
- The receipt's **historical accepted snapshot** uses FASA7001 source manifest blob `a79b28a3970668982ef44a5318642ed55848839a` and field-inventory queue blob `366ee748f51dbf2b699a26edbc1215352743191d`. Both were separately fetched at the historical receipt commit and verified equal to the stored receipt references. Modern manifest/queue blobs have advanced since the acceptance and are not substituted.
- Accepted original field obligation `obligation.rule.actions.sr3-core-combat-phase-action-timing-p104-108.selected_free_actions` binds to `rule.actions.sr3-core-combat-phase-action-timing-p104-108` at `/data/selected_free_actions`. This accepted group and record were present in the historical FASA7001 manifest/queue.
- Rule path `rules/actions/sr3-core-combat-phase-action-timing-p104-108.yml`, accepted historical blob **and unchanged current blob** `87371b67cf6ac9e57ffd276d44713eaa3cdafcfd`. All three source names are in the accepted core record at the exact individual subfield pointers above, alongside their distinct preserved conditions.

## Fail-closed acceptance engineering

`tools/expanded_acceptance/core_equivalence.py` adds a **narrow** `indexed_action_reference` comparison relation (under the existing `sr3-accepted-core-equivalence/v1` protocol). It is limited to these three original Companion p130 Free General labels and to their accepted FASA7001 `selected_free_actions` entries. The proof must name actual historical core receipt, original source/page, exact typed label and class, accepted group/subfield, exact adjacent core `condition`, and independently reviewed confirmation that the appendix imposes no replacement. All original core conditions and exceptions remain controlling.

- Accepted core module locally tested and committed at Git blob `6f7dde7fdbeb42fb96f3e98f2869a43a64fe2852`, semantic commit `58ce5f1be549a2fb45dfdf294f8ae4f64d9cb38e`.
- Its 13 new positive/negative regression methods are in `tools/expanded_acceptance/test_index_reference.py`, Git blob `674b7d4be6b134493380760d72d2dbfe43299243`, final test commit `d67d47ec49f656d9e9af73ee5768a6cf9bd57ed6`.
- Local test invocation: `PYTHONPATH=/mnt/data/sr3_core_equivalence python -m unittest discover -s /mnt/data/sr3_core_equivalence -p 'test_*.py' -v`. **33 unique test methods passed**: 20 original core-equivalence tests + 13 new index-reference checks. Synthetic fixtures do not certify actual history, independently authenticate authorship, or produce production book PASS.
- New mode returns `CORE_ACTION_INDEX_REFERENCE_CANDIDATE`, **not** `CORE_FIELD_MATCH_CANDIDATE` or `formal_acceptance: true`. Missing independent attestation, wrong action class, wrong original p130 provenance, a modified accepted rule, rejected obligation, or dropped core qualification block it.

## Coordinator handoff / remaining critical path

This source review **resolves the three action *interpretation* mismatches** and removes the need to model them as three rival procedures. It does NOT count the three rows as independently accepted: an independent coordinator must authenticate full source-book inventory, actual review custody and historical/current evidence in a production validator run.

The previously recorded Companion p130 inventory remains 187 action labels, 37 Companion-owned entries and 150 shared references; the earlier core shortlist was 38 source comparisons, **not 38 certifiably equivalent procedures**. The 27 non-Free candidates still lack individual accepted group scope; 112 additional shared references involve Critters, MiTS, Matrix, Rigger and legacy sources. A complete local Git history or separately independently authenticated historic commit evidence remains necessary for full `validator.py` execution, as do production original-review and receipt packs. Do not mark the 138-page Companion or the whole SR3 expansion corpus complete because of this narrow classification.

No protected source YAML, source manifest, original gate, global Denver checkpoint, edition precedence or other worker's source has been modified by this audit.
