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
