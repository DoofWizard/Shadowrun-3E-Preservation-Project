# Transcription batch pipeline — qualification stage

## Objective

Reduce repeated repository discovery and canonical lookup. This is an
optional deterministic accelerator for the existing ten hourly workers, not
a new worker, source authority, write path, or acceptance process.

## Public/private boundary

The preservation repository is public. The GitHub Actions job reads only
Git-tracked public YAML at an explicitly pinned commit and generates
short-lived candidate metadata artifacts. It uses no Drive credentials,
original PDFs, original page images, private review notes, or journal archives.
No actual original source material should be added to this repository or its
workflow artifacts. Keep private inputs and evidence in authorized storage.
A separate private temporary processing repository is a possible later
deployment, not a prerequisite, and deleting one cannot guarantee deletion
of previously copied data.

## Qualification

The draft branch adds review_index.py, regression fixtures, and the
sr3-transcription-batch workflow. The workflow uses synthetic Git snapshots
and builds a candidate index from the pull request's exact base commit.
No changes to canonical records, manifests, worker ownership, or existing gates.

Run locally with Python 3.12, Git and PyYAML 6.0.2:

    python -m unittest discover -s tools/transcription_batch -p 'test_*.py' -v
    python tools/transcription_batch/review_index.py build --repo . --ref HEAD --out /tmp/sr3-index.json --packets /tmp/sr3-packets

The MSI is optional. No Codex, Work, or API key is required for these commands.

## Worker consumption (after qualification)

Use the index only as a locator: source manifest candidates, registered
record paths/blob hashes, explicit printed/PDF locators, duplicate IDs,
typed field fingerprints, and historical registration pointers. To select
a source and heading, use:

    python tools/transcription_batch/review_index.py packet --index /tmp/sr3-index.json --source source.fasa-7907 --query 'ally spirit' --printed 113-116 --out /tmp/packet.json

A page range or query match is not coverage; unknown page formats and
unindexed fields are not missing rules. Compare source and live blob pins;
refresh changed records by existing authorized means. If the artifact is
unavailable or stale, keep working with the original workflow. A typed
comparison establishes only equality/difference of a scalar at an exact
record/blob/pointer, never semantic equivalence or source completeness.

Continue authentic original acquisition, independent original pixel review,
editorial gates, individual stage/prepare/write/readback/confirm/index,
receipt retention, edition lineage and acceptance under the existing
contract. No source-wide or global page credit from an index or packet.

## Next stage

After CI passes, verify an actual worker can retrieve the artifact and
consume one source packet without local machine access. Compare elapsed
lookup/setup and end-to-end verified scope throughput against comparable
existing work. Add automated private-source preparation and historical
journal matching only after authorization, authenticated input availability
and separate verification. Do not modify worker prompts until the artifact
retrieval path is proven or retain an explicit fallback.
