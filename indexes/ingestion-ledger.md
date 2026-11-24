# Corpus ingestion ledger

This file tracks corpus-level ingestion progress. It is not a source of game rules.

## Status values

- `queued`
- `structural_scan`
- `ingesting`
- `complete`
- `needs_review`

## Processing policy

Books are analyzed for:
1. new canonical records,
2. extensions to existing records,
3. explicit replacements or supersessions,
4. conversion/update instructions,
5. optional rules,
6. cross-book references,
7. source/page provenance.

A later publication is never assumed to overwrite an earlier rule solely because it is newer.

## Full-rules consolidation — live source-shard reconciliation (2026-11-23)

**Milestone:** The available-original FASA7001 mechanics/data core is formally accepted:
15/15 core sections; 451 canonical records (413 protected mechanical + 38 guidance).
The accepted `sources/manifests/SR3.yml` blob is
`b0ebffa4985ab544e64857b99e98b17d69ee3184`.
This **does not** certify all expanded rules, narrative archiving, or a runnable
game engine. FASA7001 printed p308 remains unobserved/nonblocking.

**Current all-expanded-rules verdict: NOT ACCEPTED.** Source-manifest
`status: complete`, the number of accepted records, scanned pages, or individual
closed sections does **not** establish complete original-source mechanical scope.
No independently executed final all-expanded-rules acceptance receipt is
recorded here. Existing individual source gate receipts must be reused, never
retrospectively invented.

**Live corpus catalog:** `sources/catalog.yml` has **104 entries**:
10 primary rules, 15 legacy rules/source, 10 mixed, 33 sourcebook-mixed,
32 adventure/campaign, and 4 reference aids. These are corpus *roles*, not
104 proven distinct rules-bearing books; mixed and adventure publications
must still be checked for unique mechanics. Historical 97/105 estimates
must not be used as the current count.

### Ten exclusive rules-first source shards

| Source / sole source owner | Source evidence already usable | Next independent rules-completeness obligation |
| --- | --- | --- |
| **FASA7001 core** (accepted/read-only) | 451 accepted records, 15/15 scoped sections, final source acceptance | Do not reopen; compare expansions against accepted core without duplication |
| **FanPro10662 Rigger 3 Revised** (coordinator) | Live `sources/manifests/Rigger3Revised.yml`; Power Plant appendix pp194–201 source-locally reconciled; 50 current registrations, three chassis corrections fully gated (one reclassified as historical reuse) | Complete Chassis pp202–205 field-to-canon audit and remaining whole-book mechanical scope; keep FASA7910 a separate historical edition |
| **FASA7907 Magic in the Shadows** (Magic owner) | Live `sources/manifests/MitS.yml`, verified Centering/Cleansing and other supplemental transactions | Original-TOC field-level closure of remaining modifiers/tables, including historical mechanical discrepancies |
| **FASA7126 Man & Machine** (Augmentation owner) | Live `sources/manifests/M&M.yml`, verified bioware/implant corrections; source status 'complete' only archival | Reconcile unresolved bioware overlap, Stress and healing conditions, deferred transaction receipts, and whole-book closure |
| **FASA7908 Cannon Companion** (Combat owner) | Live `sources/manifests/CannonCompanion.yml`, BattleTac, parachutes and underwater equipment source-local work | Underwater Activity pp107–112 corrections need actual verify-source + full transaction confirmation; remaining combat/equipment section audit |
| **FASA7905a Shadowrun Companion** (Character owner) | Live `sources/manifests/SRComp.yml`, point-based chargen pp13–15 and Enemies pp68–72 scoped closed; Contacts corrections confirmed | Special Contacts, New Contacts and historical gate conflicts; all-book original mechanic checklist |
| **FASA7909 Matrix / FASA7219 Target Matrix** (Matrix owner) | Live `Matrix.yml` and `TargetMatrix.yml`, Matrix Skills pp24–26 and Programming pp76–94 independently scoped closed | Remaining Matrix-user exceptions and Target Matrix Host Rules/eligibility coverage; no duplicate Programming |
| **FanPro10664 SOTA2063 / FanPro25004 SOTA2064** (SOTA owner) | Live `StateOfTheArt2063.yml` has five closed Game Information scopes; `StateOfTheArt2064.yml` has adept, Old World Magic, and Games of State equipment scoped closeouts | Directed original mechanics outside these ranges; qualitative Behind the Badge rules, section-wide original TOC acceptance |
| **FASA7109 ShadowBeat + unassigned unsuperseded 2E** (Legacy owner) | Live `ShadowBeat.yml`, 32 verified transaction entries; sports pp58–73, Simsense pp74–83, skills/options pp84–87 and equipment pp88–99 source-locally closed in live manifest | Remaining media/music/news coverage and per-mechanic SR3 supersession proof; keep original 2E mechanics unconverted |
| **FASA7002 Critters; FanPro10667 SSG; FanPro10650 Year of Comet; FanPro10666 Dragons; FanPro10653 Target Wastelands** (Critters owner) | Live `Critters.yml`: 53 original powers pp7–14 source-locally closed; SSG pp118–126 prior scoped closure | Weaknesses pp14–15, mutant/toxic pp15–17, creatures pp20–48 and all four other books' unique mechanics |
| **FASA7118 Corporate Security Handbook; FASA7115 Lone Star; FASA7215 Smuggler Havens; FASA7124 Cyberpirates; FanPro10657 New Seattle; other unassigned SR3 mixed books** (Sourcebook owner) | Live `CorporateSecurityHandbook.yml` retains accepted source-specific security corrections; other source manifests have historical registrations | Corporate Security original pp34–61 gate debt, security personnel and original NPC pp106–124, Lone Star missing p4, then novel mechanics across other owned books |

This matrix records **evidence-backed areas of progress and exact near-term
obligations**, not a declaration that each full source's TOC/field matrix is
already exhaustive. Sources not individually named must still be assigned
only within the ten existing exclusive source ownership contracts; do not
create another worker or edit another worker's manifests.

### Acceptance distinctions and immutable guards

1. **Verified source acquisition:** Fresh cataloged original PDF bytes match the
   source-specific live SHA-256; execute actual `preservation_method.py verify-source`.
   Hash matching alone never proves that a mechanic/section was examined.
2. **Original review:** Inspect original printed/PDF page images; account for
   every unique game-affecting rule, number, option, exception, conditional
   interaction, statblock and table cell. Preserve paper-original ambiguities.
3. **Semantic acceptance:** Independently review original BASELINE and
   same-substance CANDIDATE, run actual stage/prepare, normal GitHub Contents
   write, exact-byte/blob/commit readback, actual confirm and legitimate
   source-specific manifest indexing. A staged draft is not accepted.
4. **Section and book closure:** Use a finite original-TOC-derived per-field
   checklist and verified receipts. Do not promote `status: complete`
   merely because a historical sequential archive pass finished.
5. **Final expanded-rules acceptance:** A distinct corpus-wide gate must
   demonstrate all available applicable original rules-bearing sources are
   individually source-closed, with explicit legacy 2E supersession/adapter
   uncertainties or documented local omissions, before declaring the
   all-expanded-rules milestone. This is **not** the existing FASA7001 core gate.
6. **Global checkpoint:** `WORKER_CHECKPOINT.yml` remains active at
   **Denver FASA7212 completed printed p45 / PDF46; resume p46/PDF47**.
   Printed pp46–47 are archived source gaps. All out-of-order specialist
   source receipts give **zero globally contiguous page credit**.
   Lone Star printed p4 remains a separate deferred manual obligation.
7. **Workers / concurrency:** Exactly ten existing enabled hourly tasks, one
   coordinator plus nine exclusive specialists. One source owner writes
   each source-specific manifest/record. No automatic spawning or cadence
   changes. The separate draft-runner code does not count as source
   acceptance or an already-running persistent host.

**Next coordinator action:** Reconcile the latest individual original-source
section audits and gate receipts into field-level source/book closure, resolve
Rigger chassis from its owner, and keep this single ledger current; never
substitute an additive record-count percentage for verified all-rule scope.

### Coordinator follow-up: Rigger maintenance field discrepancy (2026-11-23)

The revised Power Plant Table pp194–201/PDF196–203 already has a source-local closure audit (`references/audits/r3-revised-power-plant-table-complete-original-review-2026-11-23.json`, blob `09f1e742229bc0e63e5a1564b335e22fb7a84fba`): 10 categories, 331 rows, 50 revised-source verified registrations in manifest blob `c02aa1470425d2173a94493bd98d77e1744cc72a`. The three most recent semantic blobs (battery, fuel cell, diesel) were checked live against their existing verified journals and match. These are prior receipts, not new transactions.

Fresh original FanPro10662 (SHA-256 `88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909`) and FASA7910 (SHA-256 `0857d118371309c73e5393caa0849a94ec11e1c0009c2eda8fa56169e515e860`) PDF downloads independently hash-matched. Original images of both editions' Maintenance and Overhead section were compared (revised printed pp28–29/PDF30–31; historical printed pp28–29/PDF28–29). No revised-edition change was demonstrated, but the historical canonical record `rules/vehicles/maintenance-overhead.yml` (blob `23843646d9b4f882dcf8fac881a8b4b8bcb0b626`) misplaces the rounding rule. Both original editions round **the one-percent Cost Value component upward before adding ten times the past month's Stress Points**. The original worked example uses 1,250 nuyen cost value and 13 nuyen base overhead. Existing canonical text instead says to round the Stress component. Additional explicit source conditions to reconcile: use published base value rather than actual purchase price; failed catch-up maintenance test consumes payment without removing the penalty; current-month maintenance remains due separately. Other observed values (lifestyle discounts, cumulative missed-month modifier, per-month B/R test target and base time) already match the historical record.

Disposition: shared historical canonical discrepancy, not a novel revised-edition rule or authorization to modify FASA7910. Keep it open for a source-owner-authorized, fully gated correction or explicit lineage clarification; never count duplicate revised facts. Chassis Table pp202–205 full reconciliation remains outstanding. This read-only image/hash comparison did not execute the current repository verify-source, preflight, stage, prepare or confirm in the current runtime; no new semantics, section acceptance or globally authorized pages are claimed.

### Coordinator follow-up: Chassis original-image reconciliation (2026-11-23)

**Open source-fidelity conflicts, not new acceptance.** Re-examined all four revised Chassis Table original images (FanPro10662 printed pp202–205/PDF204–207) and FASA7910 printed pp202–205/PDF202–205, following rows across page breaks. Both mounted original PDFs independently hash-matched their registered hashes. Recovered the unchanged common Python scripts from existing local copies, matched their Git blob IDs to current GitHub, and actually executed connector preflight self-test (29/29 pass). The complete live revised manifest was retrieved through GitHub Contents but its exact bytes were not materialized into the local execution environment; therefore no actual verify-source invocation against that exact manifest or new semantic transaction is claimed.

Three prior transaction-confirmed revised-source records have original-image contradictions. Prior transaction receipts prove byte acceptance, not independent correctness:
- `equipment/vehicles/r3-revised-chassis-vehicle-capacity-p202.yml` blob `1653b631070a07d4f89c3bf40339b6e1febaa3f5`: wheeled APC seating is **1b in BOTH** original images, not revised 1. The two helicopter maximum-CF differences (Utility 75→150, Medium Tilt-wing 96→300) are genuine. Remove only false seating delta through authorized correction gates.
- `equipment/vehicles/r3-revised-drone-chassis-corrections-p204.yml` blob `dfe889b95110c7f68cb5cfe00e53567ee6d828ec`: Extra-Large and Large Walker sensor/sonar are **0/— in BOTH** original images, not revised 1/—. Micro crawler start/max inversion and small crawler sensor/sonar correction remain genuine. Correct only the two erroneous delta assertions through source-owner gates.
- `equipment/vehicles/r3-revised-added-submarine-chassis-p205.yml` blob `8b1907b7cd59deba66a682a245073d8f6fb32a05`: Attack Submarine, Bathyscaph and Boomer are present in original FASA7910 **p204**, below the drone rows, then reflowed to revised p205. The historical p205 comparison alone produced a false novelty inference. Reconcile original historical chassis canonical bindings, reclassify as reuse rather than addition, preserve genuinely identical source stats; do not double-credit rows or erase old receipts. Original-image evidence directly contradicts the manifest's historical absence assertion.
- The eight rail/trailer signature changes in `equipment/vehicles/r3-revised-chassis-rail-trailer-signature-p203-204.yml` blob `59d3f6cc0aeb46453a72728d5f42d084986c1d90` remain corroborated by both editions.

The original Chassis Table has been inspected across all page breaks; full field-to-canon closure remains open pending resolution of the above erroneous records, comparison to accepted historical table records, and exact source/transaction gates. Manifest still contains 50 historical verified registrations at blob `c02aa1470425d2173a94493bd98d77e1744cc72a`; this is a receipt count, not a renewed assertion of 50 independently correct mechanics. No new records or global pages. Do not reopen accepted core. Next: materialize complete live manifest exactly, correct these source-specific errors through normal gates, then reconcile remaining original mechanical sections.

### Coordinator follow-up: three chassis corrections confirmed (2026-11-23)

The exact 51,300-byte live revised manifest was materialized locally and Git blob identity `c02aa1470425d2173a94493bd98d77e1744cc72a` independently matched. Fresh cataloged original FanPro10662 PDF was acquired from Drive; actual repository `preservation_method.py verify-source` returned `source_pdf_hash_verified`, SHA-256 `88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909`. All four local gate scripts matched live blobs and the preflight suite passed 29/29. The historical original mounted FASA7910 PDF independently hash-matched `0857d118371309c73e5393caa0849a94ec11e1c0009c2eda8fa56169e515e860`. Original images of p202, p204 and p205 revised and corresponding historical p202 and p204 re-examined; historical canonical `rules/vehicles/chassis-reference.yml` blob `6a41d3c5914376a1a47d4195d828bbe518f13fd9` read and compared.

All three source-specific corrections independently staged from original-reviewed baselines, prepared, ordinarily updated with fresh current SHA, exact commit-ref and live-path byte/blob readback, actual `ingestion_gate.py confirm` returning verified, recovery inspection, and per-record manifest update/readback. Prior verified registrations retained in `chassis_correction_history_2026_11_23` rather than overwritten as history.

| Corrected existing record | Semantic commit | Exact blob | Source index commit |
| --- | --- | --- | --- |
| `r3-revised-chassis-vehicle-capacity-p202` — APC seating 1b unchanged; two genuine CF differences remain | `261d0ae7b53fcb29e30d90dd94d4912553382495` | `538cbecd83cc3efc255be615abc9186d0ec8b9f0` | `79d3fc924018fdb352352a2f16c981f92883aef6` |
| `r3-revised-drone-chassis-corrections-p204` — two walker sensor pairs 0/— unchanged; three genuine crawler field differences remain | `c60d12884ba7c394e004c796a9dbda61ab3a1df7` | `5d1441a4ba7e933da198cff7a9a22b645b1b0d71` | `639dc8ae4c536207faba070e47a6780362d8ab79` |
| `r3-revised-added-submarine-chassis-p205` — three historical p204 rows reflowed to revised p205, reuse not novelty | `dcf6ffa6acac38563a4ad2fa85d851041e9b4d98` | `dc42685b941ce83f24f302ba968e7ad774acf027` | `9d894028cc432fea9eb6693006c9abc267045aa1` |

Final manifest exact blob `217dced5a64e25a5ff66e735b6a79af7e95c5ab7`, independently reconstructed and hash-checked locally. 50 current registrations, three corrected existing records, zero new distinct record IDs, zero newly certified full sections, zero contiguous pages. The preceding chassis discrepancy note is resolved for these three specific records, not the entire table. Historical Boomer EnviroSeal (water & engine) qualifier remains historical normalization debt; both originals print it, so not a revised difference. Full chassis field-to-canon reconciliation and maintenance p29 historical debt remain open. Historical FASA7910 and accepted SR3 source unchanged.

**Specialist live reconciliation (read-only, not duplicate acceptance):** MitS `1151a0a5ecfb35a154e2df51fd3ae7c6ef81e7f2` retains Centering/Cleansing field review and magical-group indexed transactions; M&M `c817fbc9496888d88786b6a1fd5bc83084bac304` lists nanoware classification/addiction resolved and installation receipt debt; Cannon Companion `5cccb8cdc22a66b8ec0b1729088806808ae06d86` indexes advanced combat options p85–86; SRComp `c27b942275c80f41efd70231a35cbbaf242bc55b` retains contact contest and scoped option closure; Matrix `991e11228bb26f27fb6955dbd7fd54d72a4cdce6` indexes team coordination and SOTA maintenance; SOTA2063 `389e7ea7625efb1b362d0073c9d9fcf3225b2dcf`, SOTA2064 `c33edd6c9396d5bb8b3afa975f76ec4cb6eb4d25` retain source-local evidence; ShadowBeat `9c83c5e6308bbeefa5aeb77171a3810546145b53` records 32 verified transactions and Simsense/equipment section closures with legacy lineage unresolved; Critters `72666d1f7cacf77ee3c0a45421c6bf817d4c88aa` indexes Awakened entry exceptions pp29–30 and pp18–20 statistic reference closure; Corporate Security Handbook `eb3cfae85d918d7f847835fd69c49a61f524e687` indexes verified magical security source corrections pp36–43. Secondary source manifests also inspected; none independently recertified by coordinator. Core manifest blob `b0ebffa4985ab544e64857b99e98b17d69ee3184` and global checkpoint blob `6c2fde9f34fef62d3c98b1f284212713dc81fa32` remain unchanged. Expanded milestone open.

### Coordinator follow-up: revised submarine vehicle-list mechanics (2026-11-23)

Freshly retrieved original FanPro10662 PDF (40,997,045 bytes) matched SHA-256 `88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909`; actual preservation_method verify-source returned source_pdf_hash_verified against exact manifest blob `217dced5a64e25a5ff66e735b6a79af7e95c5ab7`. All four unchanged verification scripts matched live Git blobs; preflight 29/29 passed. Historical FASA7910 mounted original independently hash-matched `0857d118371309c73e5393caa0849a94ec11e1c0009c2eda8fa56169e515e860`. Original page images of revised pp188–190/PDF190–192 and historical pp187–189/PDF187–189 compared by model rather than page number. Three distinct original revised differences accepted through separate actual stage/prepare, ordinary Contents create, exact commit-ref and live-path readbacks, confirm/inspect verified, individual source index and exact readback:

| New record under equipment/vehicles/ | Semantic commit | Blob | Index commit |
| --- | --- | --- | --- |
| r3-revised-anago-availability-p190.yml | a670aafc83e97f9a46dd957c25b59c8b1bf3f354 | e99cbf365db9e435625b0665d56e10eb1c500e9c | e0bb0cffd921e5c7031e1fbd974b23579663399e |
| r3-revised-delphin-patrol-launch-control-count-p189.yml | 4d920590aba5bc172914bf4fff00512b85e5d284 | c77e1ee560ee06c995e4d24a8cc734eee90b5131 | ba644fc5006af0e3a9aa39b754f05c56fee097f5 |
| r3-revised-new-hampshire-mount-count-p188.yml | e96d99bcbde8f4306ab26c182d7bd846d069cec5 | 79b1f60708d851cebf438d0a4bd223d5f10b8b0b | d5eab956f1e51faf3fe3c6c981ba66c5f9ea727e |

Final revised manifest blob `40f394f71804267446ddff7ccccffd58b7219cd0`: 53 verified registrations (3 new). Historical entity references checked: New Hampshire `63de385a3787e6e4cb8839175ae523efde82cae2`, Triton `ccf855f5688e1fa444ff74b336c7fb6541ea0ab6`, Locker `725b95fd4f5d3a0887765589844b735786a5cb0f`, Delphin `4c76bcdf94df1baf2fee5ee9f4f408c86525812e`, Electronaut `2b1092f9fccf8a0f43f918f8e85e4988cfe31adf`, Vaneyev `f7367767eb6c026310dad2f474c7bbfd2689f606`, Anago `8d95c0dc60961f82a4781e6f1921acd2a4daee69`. Distinct revised fields are accepted; no whole natural section certification. Historical normalization debt observed in both editions: Triton twelve-year overhaul interval; Delphin diesel-mode recharge 1 PF/hour and accommodation prose up to eight versus table seating four; Anago prose ability to tow up to six passengers versus two seats (six handholds already indexed); revised p189 table changes column label Sensor/Sonar to Sonar for minisubs but retains pairs, so do not invent a different numeric interpretation. Revised submarine chassis p205/PDF207 and historical p205/PDF205 also show the seven commercial/minisub/patrol rows beyond Boomer all specify water and engine EnviroSeal, omitted from historical chassis canonical feature text. These unchanged-source omissions are not revised-only differences; retain historical ownership and resolve with appropriate source authority before full mechanical acceptance. Chassis table and p29 maintenance debt remain open.

Read-only live specialist primary manifests checked: MitS `1151a0a5ecfb35a154e2df51fd3ae7c6ef81e7f2`, M&M `cba0ab958c070a123198915ae04cd9174cc407ec`, Cannon Companion `6df6a5eacda6c19afa0ddb9da2a78f1ce792cfe2`, SRComp `e477b2626fd7dd382ca6ff9ad7c13fbccf612669`, Matrix `d9c7a2edf1affb37c2ffc170771ef160f5ce13d2`, SOTA2063 `389e7ea7625efb1b362d0073c9d9fcf3225b2dcf`, SOTA2064 `c5ff206ffc030b1ec33cc68061a9ef3da11ec92a`, ShadowBeat `f19ea7d6e51671af5264db14814007ba5d9e430a`, Critters `d4a46599f7e7ee16ef373f29af15ef115e5a3ed3`, Corporate Security Handbook `526c0b13f8e5e9ffa164b9f594fdda6d2a7f3764`; Target Matrix, Sprawl Survival Guide, Year of the Comet, Dragons of the Sixth World and Target Wastelands also read. Changed manifests are evidence of progress, not automatically whole-book certification. No expanded-corpus acceptance. Core blob `b0ebffa4985ab544e64857b99e98b17d69ee3184` and checkpoint `6c2fde9f34fef62d3c98b1f284212713dc81fa32` unchanged; zero global pages.

### Coordinator follow-up: light aircraft original-table reconciliation (2026-11-23)

Fresh cataloged FanPro10662 original PDF 40,997,045 bytes, SHA-256 `88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909`; actual preservation_method verify-source returned source_pdf_hash_verified against exact live manifest blob `40f394f71804267446ddff7ccccffd58b7219cd0`. Four common scripts match current GitHub blobs; actual preflight 29/29. Mounted historical FASA7910 independently hash-matched `0857d118371309c73e5393caa0849a94ec11e1c0009c2eda8fa56169e515e860`. Original revised pp180–181/PDF182–183 and historical pp180–181/PDF180–181 images compared by model, not pagination. Three new distinct source-specific records independently staged/prepared, ordinarily created with matching exact bytes at commit and live path, actually confirmed and recovery-inspected, individually indexed and exactly read back:

| Record under equipment/vehicles/ | Semantic commit | Blob | Index commit |
| --- | --- | --- | --- |
| r3-revised-platinum-availability-p181.yml | 538c764239756d6d2baad03674783c0748f7372c | 6f272c09b3f3c1ec37da46d01f53a4a4a25aafaf | 184a99f1cec84cb880d8ab2cf27d6f1c6d130461 |
| r3-revised-nightglider-stats-p181.yml | 4ff9b0a362cd4fdbd0f7adde51952e86703144d4 | f7485ed3b7c7b07c022d5e3134944002e1b71196 | 7405c7a735eecd08f26207909d1c74088603a8d7 |
| r3-revised-light-aircraft-fuel-and-raven-index-p180-181.yml | 480a566d7359f72b5a9bf91f245953ef024a2002 | c63bfdf426373fe6f820f60b7a83b082ff58ddf6 | a53e2105751ca525b1e6e9e861bbb6bc43badb60 |

Final source manifest blob `23a0e91eabe568321e95c0fed60993114db6ddc7`, 56 verified registrations. Platinum I/II Availability changes, Nightglider Speed/Economy/Availability/Cost, Raven Street Index and multiple literal JP fuel label differences are confirmed. CASA J-229 heading versus J-239 table label preserved. Remaining light-aircraft issues: Mistral Jet (2,000 l) -> JP (2,000 l) original difference observed, historical canonical path unresolved (attempted exact path returned 404; no duplicate created). Nightglider description claims 200 kg capacity while table Load 190 in both editions, historical canonical omits prose; Platinum satellite navigation in both editions is descriptive feature omitted from historical entity; Cloud Nine prose six seats versus printed 2 + 2b in both editions, preserve distinction pending historical source authority. Ultralight/twin-engine natural section closure not certified. Previous Chassis Table and maintenance historical debt remains open. No global page advance.

Live specialist primary manifest reconciliation (read-only): MitS `39b5c135848e3f5e1cc2f54d8203b3edc3b8de31` adds Learning Metamagic pp69–70 with verified receipt; M&M `cba0ab958c070a123198915ae04cd9174cc407ec` retains scoped surgery options; Cannon Companion `3f0d34d620aa3f6953c9bec0e78f2a24934fdbbe` has scoped Using Skillsoft Systems and Dedicated Chipjack closure, programming pp60–64 outstanding; SRComp `01dfe599555ddd2f8b8d2eb5edc359b1cf0fa141` has five NPC-tier source-local reconciliation with printed ambiguity; Matrix `491a319839f83f8c41c9a6a7659e65ae38588d08` has Accessing the Matrix closure through p42, seven new records and one correction reported in indexed audit; SOTA2063 `389e7ea7625efb1b362d0073c9d9fcf3225b2dcf`, SOTA2064 `92f2b3ce7dbfbd2ca0da57b38be2b75fad163dc9` retains directed Games of State/sports review; ShadowBeat `7d33faa67ec1b5fee2d8e6daf40c1ce2711e9406` adds indexed p27–29 original legacy network conflict and p49–51 reporting records; Critters `28b59c37f9e5d8f42a69704de6b656ea7ace950f` retains power catalog closure and outstanding Awakened individual blocks; Corporate Security Handbook `526c0b13f8e5e9ffa164b9f594fdda6d2a7f3764` retains Matrix guidance corrections. Secondary Target Matrix, Sprawl Survival Guide, Year of the Comet, Dragons of the Sixth World, Target Wastelands and Lone Star manifests inspected. These are manifest-reported source-local findings, not independent full-book recertification. Core manifest `b0ebffa4985ab544e64857b99e98b17d69ee3184` and global checkpoint `6c2fde9f34fef62d3c98b1f284212713dc81fa32` read unchanged. Expanded-rules acceptance remains open.


### Coordinator follow-up: functional improvement missing fields and Mistral binding (2026-11-24)

Original FanPro10662 freshly retrieved (40,997,045 bytes), actual repository verify-source returned `source_pdf_hash_verified` against exact live manifest blob `23a0e91eabe568321e95c0fed60993114db6ddc7`, SHA-256 `88c3670ad4f39efebb1ee0545c222e4153bc4a5e1114e138e063e4f845a36909`. Four cached gate scripts matched live Git blobs; preflight self-test 29/29. Historical mounted FASA7910 SHA independently matched `0857d118371309c73e5393caa0849a94ec11e1c0009c2eda8fa56169e515e860`. Revised original pp114–116/PDF116–118 and historical pp114–116 original images, plus prior Mistral original p180 versus revised p181, directly reviewed. Two new records independently baseline/candidate reviewed, staged/prepared, ordinarily created, exact commit-ref and current path read back, actual confirmation and recovery inspection verified, individually indexed/read back:

| Record | Semantic commit | Blob | Source index commit |
| --- | --- | --- | --- |
| rules/vehicles/r3-revised-design-functional-improvements-p114-116.yml | a28f1a92699b25e26dce4f094c4995358686607a | cba3b9cd609e3e107314c888b7d76eec5ccf7c40 | 736b4c52c5e8415f934ec70fa0eca4b56af4c2e8 |
| equipment/vehicles/r3-revised-mistral-fuel-p181.yml | 53af2beae8a4923d51d8ca0a8e9ee1586537d4e5 | 0fda964927dc59d60e4c70723b1a743a8aa8ee08 | 2df5dc8d02449655c0a0a7d4093ed281797b9472 |

Final revised manifest blob `9fbd7e4fa98d0694b130ffe37c0c5cce93a9bc1e`, 58 verified registrations (+2). Functional Improvements: all nine headings and five fuel-table rows compared. Historical rule/vehicles/design-options.yml blob `7fcadc59bacfd4e002c89e46b20e2162c2da3211` contains acceleration, depth increment, entry point costs and limits, handling, economy, cargo, load, signature and speed values; missing Hull Factor, depth initialization/multipliers and exact Load reduction, entry rounding and feasibility, full fuel capacity rows, independent ground handling, economy increment and explicit CF/Load accounting now indexed as additive field-level normalization, not an edition delta. The printed prose saying fuel enlargement does not reduce Load and table's electric Load reductions remain a source interpretation ambiguity. Historical record lacks independently confirmed modern gate provenance; full natural-section certification therefore remains open despite complete original section image review and additive field registration. Design Enhancements p116 onward not certified. Mistral historical entity resolved at entities/vehicles/embraer-dessault-mistral.yml blob `6a6bf8c79965e8a6879b3cc835afd74577979721` (historical filename spelling differs from display name); Jet to JP designation, same 2,000 liters. Earlier aircraft prose/table distinctions and Chassis Table/maintenance debt still open.

Read-only specialist live primary manifest reconciliation: MitS `39b5c135848e3f5e1cc2f54d8203b3edc3b8de31` unchanged; M&M `987f0facfbf081c9556b294f53777355f20cc2ae` records seven scoped surgery subsections, Implant Detection and receipt reconciliation remain; CannonCompanion `d0bfb00ea877e4b81715955d8e7eded2a3d22e82` records four scoped BTL subsections, three verified additions, open Types of BTL Chips qualifications; SRComp `163a42d1835b6393778188f2e0766ffc6e2d3852` records gang leadership correction pp123–124, gang creation write HTTP409 remains; Matrix `6db5aafa0b30753b80f2592f4c66882ab6da155c` records UV Hosts pp48–49 source-local closure, topology/Paydata open; SOTA2063 `389e7ea7625efb1b362d0073c9d9fcf3225b2dcf` unchanged; SOTA2064 `1fa975f4138c7d2372657e816d8d245bec65cf88` records custody timing and directed review pp69–95, Culture Shock remains; ShadowBeat `c55405ce9edfabdbff3c0db44be2ccb59ccb0452` records instrument control pp8–10 and sasquatch band recruitment p17 with SR3 adaptation unverified; Critters `e01c4e6ebbb4f73d4ad86a3c177201e98d52d990` records Nomad p38 exception, whole-book closure unclaimed; Corporate Security Handbook `526c0b13f8e5e9ffa164b9f594fdda6d2a7f3764` unchanged. Secondary Target Matrix, Sprawl Survival Guide, Year of the Comet, Dragons of the Sixth World, Target Wastelands and Lone Star also fetched. Exact live record blobs matched indexed receipts for UV Hosts, Nomad, both new ShadowBeat musical records, BTL programming and its audit, and M&M surgical operation; no coordinator recredit or whole-book certification. Accepted SR3 blob `b0ebffa4985ab544e64857b99e98b17d69ee3184` and checkpoint `6c2fde9f34fef62d3c98b1f284212713dc81fa32` unchanged. Coordinator newly certified full sections: 0; new global pages: 0. Full expanded-rules acceptance remains open.

## Completed Bug City source

| Source | Status | Verified scope |
| --- | --- | --- |
| Bug City (FASA7117) | complete | Sequential coverage through printed p.160/PDF169; game information through p.151, illustration p.152, index pp.153-160. Historical Second Edition mechanics retain source provenance and explicit relationships without inferred SR3 supersession. Manifest and checkpoint agree, with no pending normalization. |

Completion verified on 2026-10-11: [manifest commit](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/34a6719befed317ba0c803ebf4d9334dad42d006), [checkpoint commit](https://github.com/DoofWizard/Shadowrun-3E-Preservation-Project/commit/3bc992688e9d64ffaa80f9e1e6df41e9425fe70c). The final recovery session advanced from printed p.137/PDF146 through p.160/PDF169 in five fully reconciled slices, adding 19 source-reviewed, gate-confirmed records. The former p.138 write rejection did not recur in this session; its historical root cause remains unconfirmed. Recovery sidecars were retained with retirement evidence.

## Corpus inventory

The current 104-entry Drive inventory is stored in `sources/catalog.yml`. Every item remains in the queue until it is marked complete here or in its source manifest.

## Completion rule

A source is not marked `complete` until:
- all mechanical additions have canonical records or explicit links to existing records,
- all explicit replacements/supersessions/conversions have lineage entries,
- optional rules are marked optional,
- world-only material has been routed to world records where appropriate,
- ambiguous conflicts are preserved rather than silently reconciled,
- source/page provenance is present.
