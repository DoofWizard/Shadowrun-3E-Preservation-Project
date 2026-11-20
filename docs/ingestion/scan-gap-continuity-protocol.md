# Scan-gap continuity review — source preservation

Applies to Shadowrun Pass B and subsequent preservation passes. This is a source-fidelity protocol, not a substitute for the existing ingestion, exact-byte transaction, or source-completion gates. One existing hourly worker remains authoritative.

## Editorial rule
An absent **printed** page in a scanned PDF is a **warning requiring contextual review**, not automatic proof that textual content is missing. Scans commonly omit intentionally blank leaves. Start with the benign-omission hypothesis, but test it against visible evidence rather than converting a probability into a fact.

Review and record:
1. The exact preceding and following **physical PDF page images**, printed headers/page numbers, and the absent printed page(s). Describe the true mapping; do not assign a nonexistent PDF image to a missing printed page.
2. Both "hang points": whether sentences, headings, footnotes, tables, figures, lists, running page headers and chapter structure join naturally, including any continuations across columns.
3. The printed table of contents, index and in-book cross-references for an expected heading or substantive item on the omitted page.
4. Whether the same purported page is absent from another **independent source scan** (not just a byte-distinct re-encoding or derived copy); record the source identity/hash when known.
5. Distinguish facts observed from images, editorial inference, user-supplied publishing knowledge, and independently authenticated replacement images.

## Dispositions
- `likely_intentionally_blank`: both sides connect and no positive source evidence points to substantive material. Preserve uncertainty and the evidence; do not manufacture a blank page or content.
- `suspected_missing_content`: a specific interrupted sequence, table, heading, table-of-contents target, or similar positive evidence suggests omitted material.
- `confirmed_missing_content`: an authenticated independent page/source shows material absent from the cataloged PDF.
- `resolved_by_verified_page`: an original or otherwise sufficiently authenticated replacement page was independently reviewed with provenance and source-integrity controls.
- `project_level_exception`: only an explicit, documented project decision made with the contradictory evidence visible, subject to **all** existing authorization and completion gates; it never asserts that unobserved facts were extracted.

Neither a likely blank nor an exception on its own creates a source-reviewed semantic record, an ordinary GitHub semantic commit, or an `ingestion_gate.py authorize-advance` receipt. No silent pagination remapping, synthetic source pages, frozen-data changes, or weakening of gate constraints. Until an authorized resolution can be represented lawfully, keep the manifest's contiguous boundary unchanged; distinct verified forward records remain separate.

## FASA7115 worked continuity finding (2026-10-26)
Publication: Nigel D. Findley and Stephen Atkins, *Lone Star Sourcebook*, FASA Corporation (1994), Shadowrun original/Second Edition source context, catalog FASA7115, `source.fasa-7115`.

The original Drive-cataloged 145-page PDF has SHA-256 `c24e67bec3b2e2659236f96cfa334f06cde95ad4f76958e09943379060e69c28`. In it, physical PDF p4 is printed p3 (continuation of contents/credits); physical PDF p5 is printed p5 (`INTRODUCTION`). Printed p4 is absent. The table of contents on printed p2 / PDF p3 **explicitly assigns "WELCOME TO SHADOWLAND" to printed p4**, while separately listing the `INTRODUCTION` at printed p5.

These adjacent pages have no mid-sentence break, but that alone does not prove p4 blank: the independently listed named section is positive evidence of potentially omitted content. Classification: `suspected_missing_content`, **not** `confirmed_blank` and **not** `confirmed_missing_content`. The user's general observation that unscanned printed pages are usually blank is retained as a valuable triage prior, not as independent page imagery. The precise target for further evidence is the single printed p4 section; do not repeat a wholesale rescan of p5–136.

The manifest currently documents completed-through printed p3/PDF4 and 161 verified, separately indexed forward records (printed pp5–136 plus unnumbered plates/back cover). This statement is a dated snapshot, not authority to advance boundaries on later runs. Recover the actual page or obtain an explicit project-level disposition with adequate source evidence and gate authorization before claiming contiguous progress.

## Recording requirement
Preserve a compact receipt with source ID, actual PDF hash, physical PDF positions, observed hang-point texts/headings, TOC/index evidence, confidence/disposition, unresolved uncertainty, reviewed image locations, and optional authenticated replacement provenance. Review new candidates before the baseline freeze under the fictional-source/newsroom-neutral playbook. Never claim the continuity receipt proves full source fidelity or a successful semantic write.

## User-authorized FASA7115 p4 deferral (2026-10-27)

The project owner explicitly directed: "Skip that one page. I will manually verify the page later." This is an affirmative **project-level deferral** of the missing **printed p4** of FASA Corporation's *Lone Star Sourcebook* (FASA7115; `source.fasa-7115`, 1994 original/Second Edition), **not** an assertion that p4 was blank or source-reviewed. The cataloged 145-page PDF (SHA-256 `c24e67bec3b2e2659236f96cfa334f06cde95ad4f76958e09943379060e69c28`) has physical PDF4 displaying printed p3 and physical PDF5 displaying printed p5; there is **no physical PDF image for printed p4**. Printed p2/PDF3's contents explicitly identifies `WELCOME TO SHADOWLAND` at printed p4. The owner has reserved manual verification of this one page.

Practical sequence: **do not repeatedly investigate p4 as if the user had not decided**. Continue genuine independent review, correction and gate-authorized indexing of distinct available source pages starting with printed p5, using previously verified forward records without resubmission. Keep the absent p4 identified as a deferred, unverified source-copy gap. This documented decision alone is NOT a semantic record, `ingestion_gate.py authorize-advance` receipt, permission to fabricate a p4 image/range, or permission to silently change `done`/`next`. If the existing gate cannot represent the one-page exception while preserving source-integrity invariants, report that **narrow technical gate incompatibility**, keep true authoritative boundaries intact, and continue independently authorized forward work. Only a separately reviewed, strictly scoped lawful exception mechanism (or authenticated p4) may enable later boundary movement; general gate weakening is prohibited.

## Permanent owner policy — nonblocking scan omissions (2026-11-20)

This project-owner direction **supersedes earlier missing-page stop conditions for ongoing work**. An absent page in a cataloged scanned copy is a documented, deferred source-integrity limitation, **not an automatic blocker** to consolidating authentic available-source mechanics, processing eligible subsequent material, engine development, or issuing a *properly scoped* completion verdict. The original page is not silently credited or reconstructed. An omitted page may still be investigated later when independent evidence is newly available or the owner requests it.

**Required omission ledger fields:** source ID, publication/edition, catalog identifier, exact original cataloged scan SHA-256, absent printed folio(s), neighboring observed printed-to-physical-PDF page mapping, text/table/heading continuity where actually examined, historical observations, date and attribution of the owner's disposition, any positively evidenced unresolved mechanical dependency, and status `owner_accepted_nonblocking_deferred_later_audit`. Preserve earlier contrary or unresolved observations as *history*, not current global project blockers. Do not claim that an unseen page was inspected, proved blank/artwork, transcribed or deliberately skipped by the original scanner. The owner's continuity conclusion is attributed **owner evidence** rather than source authentication.

**FASA7001 case (original Shadowrun, Third Edition, FASA Corporation):** the scanned PDF SHA-256 is `7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914`. The existing page-image receipt records printed p307 at physical PDF316 and printed p309 at physical PDF317, with no image of printed p308. On 2026-11-20 the owner independently reviewed the continuity and judged that the missing folio did not interrupt the mechanics-bearing article and should not block core consolidation. **Disposition: owner-accepted, nonblocking for FASA7001 available-source core mechanics; audit later if new original evidence appears.** Do not repeat unchanged p308 replacement searches. It is still an unknown original folio, *not* an authenticated blank or credited printed page.

**Denver FASA7212:** printed pp46–47 are historical archived source losses and noncore. Preserve the real active boundary through printed p45 / PDF46 and all pending and forward index history. Never turn the owner disposition into an unauthorized page advance or source transition.

**Gate separation:** The existing `ingestion_gate.py authorize-advance` controls active-source global contiguous page advancement, not a source-specific postscan *available-source* gameplay-mechanics coverage verdict. An omission disposition is no semantic ingestion receipt, new verified record, readback, mechanical field value, or permission to falsify a manifest status. Preserve first-pass editorial and provenance review, independently sourced baseline/candidate, transaction stage/prepare, ordinary GitHub Contents write, fresh exact-byte readback, confirmation and legitimate source indexing for genuine available-page semantic work. If a concrete missing mechanic is positively demonstrated later, record *that exact narrow unknown*, continue independent work and avoid invented values. Full original-book archival certification and executable engine readiness are separately reported.

This section is an owner-authorized administrative policy update. The original scan-gap continuity protocol, FASA7115 named TOC discrepancy and older observations above remain historically intact. In a conflict over **whether work must stop solely for a scan omission**, this later owner policy controls; in a conflict over **whether an unseen page was source-verified or may be awarded contiguous credit**, the original source-evidence and transaction gate restrictions still control.
