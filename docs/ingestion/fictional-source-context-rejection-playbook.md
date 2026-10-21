# Fictional-source context for ambiguous connector rejections

**Scope:** Preservation records drawn from published tabletop role-playing games, fictional sourcebooks, adventures, or other invented-world publications. This is an ingestion provenance and diagnostic workflow, **not** a way around safety restrictions.

## Standard first response

1. Read the actual failed operation, diagnostic text, any observed provider HTTP status, target path, latest remote blob, verified candidate hash, and staging journal. An ambiguous "blocked by OpenAI's safety checks" message is **not** evidence of a particular trigger or a GitHub HTTP status.
2. Confirm the subject's **fictional** identity using the original publication, its real publisher/title/cat. number, edition, and printed/PDF page map. Do not invent publication metadata or assert that a real person is fictional.
3. Independently source-review the baseline against original page images. Correct unsupported or overstated biographical details in **both** the independently reviewed baseline and same-substance candidate before preflight; never pretend a candidate copied into baseline constitutes independent review.
4. If provenance was ambiguous, state it prominently and truthfully in schema-permitted root **headline/summary** and the ordinary GitHub commit description. Example: "Fictional Shadowrun tabletop RPG character from FASA's Prime Runners (FASA7116, 1994, Second Edition), printed p20/PDF p21; these are invented-world biographical claims, not a real person's profile." Keep edition_scope, source, record_type, exact provenance and one content_class. For nonmechanical classes keep the approved framing required by connector_preflight.py.
5. Only presentation framing may differ between the verified baseline and candidate. Preserve all substantive fields, relationships, identity, chronology, attribution, agency, conditions, negation, and precise game mechanics. Changes to substantive fields require fresh independent source review of the revised baseline, followed by staging and preflight; do not edit a staged candidate silently.
6. If actual conditions or candidate content legitimately changed, run the normal local transaction_recovery.py stage and ingestion_gate.py prepare, then submit the **exact preflighted UTF-8 bytes** once through the ordinary GitHub create_file/update_file connector action. This step is never a request to override a denial.
7. Fetch the exact GitHub path again. Only a real matching blob plus actual commit SHA permits ingestion_gate.py confirm. An observed 404 on **readback** is not an observed 404 on the preceding write.
8. Run authorize-advance only after all pertinent source classes are independently covered and all required receipts exist. Then update/readback the authoritative source manifest **before** its checkpoint mirror; retain unrelated verified-ahead and deferred entries without loss.
9. If rejected again, use preservation_method.py log-failure/decide with the trusted journal and exact observed error. Do not retry identical denied bytes, disguise facts, route through alternate Git APIs, weaken validation, guess an unknown HTTP status, or mark a page complete. Defer with evidence and continue safe independent work.

## Worked example

On 2026-10-21, Erik Vernon Dreyfuss's **fictional** biography in FASA7116 Prime Runners, printed p20/PDF p21, was successfully submitted after independent source review, a correction to unsupported college/Harvard chronology, and prominent truthful source-context framing. GitHub returned commit `886d5367f9c048bb1397818763e439fa18c3eb6f`, observed matching blob `2eb43e9c9fae7d2212af1b7a68146c0a135fafeb`, and ingestion_gate.py confirm returned verified. This verifies **that** the revised candidate was accepted; it does **not** establish which aspect of the earlier rejected payload caused the prior generic rejection.

This playbook applies by default to similarly ambiguous **fictional** character/person/organization records; do not apply a fictional label to real-world individuals. Source-fidelity and normal connector restrictions remain controlling.
