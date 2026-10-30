# Provisional Lone Star to Smuggler Havens transition

The owner authorized this specific transition on 2026-10-30 while reserving Lone
Star printed p4 for later manual review. Extraction reached printed p136/PDF144;
this is not full verification. The existing completion checklist remains binding.
There is no generic skip-source flag and no automatic exception for other gaps.

The missing page is **unverified**, not blank, irrecoverable, or complete. Its TOC
heading is *Welcome to Shadowland* and no physical PDF page exists in this copy.
The transition never emits a semantic receipt or credits any numbered page.

## Durable state

- `sources/manifests/LoneStar.yml` stays byte-for-byte unchanged, including all
  163 verified-forward entries, records, p136/PDF144 boundary and p4 evidence.
  Its legacy `status: ingesting` is deliberately retained. The separate transition
  receipt records `extraction_finished_manual_review_deferred`; do not reinterpret
  that state as `complete` or rewrite the legacy source to satisfy completion.
- `sources/transitions/FASA7115-to-FASA7215.checkpoint-before.yml` is the exact
  outgoing checkpoint, with its original `last_commit` and queue preserved.
- `sources/transitions/FASA7115-to-FASA7215.yml` binds the authorization, outgoing
  blobs and successor seed. `source_complete` and `source_completion_allowed`
  are false; p4 remains a required manual-review obligation.
- `sources/manifests/TargetSmugglerHavens.yml` starts with no credited pages or
  promoted forward records. `done: {p: 0, pdf: 0}` is an empty-ledger sentinel;
  resume p2/PDF3 is the first numbered page. PDF1-2 are unnumbered cover/title.
- `WORKER_CHECKPOINT.yml` switches to FASA7215 only after committed prerequisite
  readbacks. It carries the p4 obligation and immutable transition references.
  `WORKER_CHECKPOINT_NEXT.yml` is historical and is not changed or activated.

The catalog is a Drive inventory, not the active execution pointer. Existing
FASA7215 semantic files stay in place and retain their IDs and commit history.
They require actual staged/confirmed receipts and authoritative indexing before
page credit. Do not manufacture receipts from file presence, a tree, or a hash.

## One-time deployment and recovery

Run regression tests before any authoritative checkpoint change. The offline tool
`tools/ingestion/source_transition.py authorize` requires the exact outgoing
manifest/checkpoint and a freshly acquired cataloged successor PDF. It produces
the receipt without changing the source or checkpoint. It rejects any changed
outgoing state: re-read and reconcile a concurrent worker update instead of
overriding the expected SHA.

Publish code/tests, archive, successor manifest, receipt and handoff using normal
GitHub `create_file`/`update_file` actions. Read each prerequisite back at its real
commit. Record `commit_sha`, `blob_sha`, and SHA-256 of the exact readback content,
keyed by repository path. Include the unchanged outgoing manifest in this map.
Then run `activate` with these readbacks; it creates a checkpoint proposal.
Re-read current main and its checkpoint before the final normal `update_file`.
Use the current expected blob SHA. Verify the checkpoint bytes after commit and
run `audit`. Write responses alone are not verification.

If interrupted before checkpoint activation, the outgoing checkpoint remains
authoritative. Reuse identical committed prerequisites after fresh readback;
never reset a checkpoint already on FASA7215 or erase forward work. If checkpoint
activation has an unknown outcome, read it back before retrying. Exact matching
active state is audited, not reactivated. Divergent state requires reconciliation.

## Existing hourly worker startup

Use the existing single hourly worker; do not create a task or alter its schedule.
Read the live checkpoint first. When `provisional_source_transition` is present,
run this audit with fresh GitHub files (paths shown from repository root):

```sh
python tools/ingestion/source_transition.py audit \
  sources/manifests/LoneStar.yml \
  sources/transitions/FASA7115-to-FASA7215.checkpoint-before.yml \
  sources/manifests/TargetSmugglerHavens.yml \
  sources/transitions/FASA7115-to-FASA7215.yml \
  --checkpoint WORKER_CHECKPOINT.yml
```

The audit accepts ordinary successor progress but rejects loss of the p4 debt,
changed outgoing evidence, or manifest/checkpoint disagreement. Reacquire and hash
the cataloged active PDF each run. Continue ordinary source review, independent
baseline, preflight, stage/prepare, normal write, exact readback, confirm,
authorize-advance, manifest then checkpoint. Neither this audit nor CI proves
source fidelity. All original gates remain mandatory and unmodified.

Start by reconciling p2-3/PDF3-4. The existing opening record has a mixed
unnumbered/numeric citation that the numeric page-advance gate cannot consume.
Preserve that record. Recover its authentic receipts where available, and prepare
a source-reviewed numeric page record through normal gates when required; never
truncate or relabel a receipt. TOC routes are seeded; deep-review every mechanical
subsection and reconcile end matter before deciding FASA7215 completion. Continue
the fixed queue with FASA7214 afterwards, carrying unresolved manual-review debt.

Do not repeatedly reopen Lone Star p4 without a new copy or the owner's manual
review. Closing that obligation requires new source evidence, ordinary semantic
gates where applicable, and a separate audited state change. Do not edit this
receipt or archival checkpoint to make historical p4 verification appear true.
