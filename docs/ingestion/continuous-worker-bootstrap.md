# Continuous SR3 source-review preparation (draft stage only)

This tool is a RUNNABLE, FAIL-CLOSED draft preparation system, not a replacement for the existing verified source publication workflow. It creates no additional ChatGPT tasks, makes no changes to their hourly schedules, and never submits or indexes canonical rule records.

The supervisor supplies sourcebook tasks and original PDF page images to locally authenticated Codex CLI. It moves on to another queued task immediately once one completes, limited by machine capacity. A draft prepared by this utility is NOT accepted canon and counts as zero source-verified committed records until the established source-owner transaction pipeline succeeds.

## Run on the MSI or another computer that stays online

Prerequisites:

- Python 3.12+ and dependencies: PyYAML==6.0.2 and pymupdf.
- An authenticated official Codex CLI, supporting codex exec.
- A separate, up-to-date clean clone of DoofWizard/Shadowrun-3E-Preservation-Project.
- A locally synchronized, trusted mirror of the original registered Google Drive PDFs, with the source catalog number in each original PDF filename (for example FASA7907-original.pdf).
- A persistent output directory OUTSIDE the source repository.

PowerShell example, replacing example paths with actual existing paths:

    cd C:\Projects\Shadowrun-3E-Preservation-Project
    py -3 -m pip install PyYAML==6.0.2 pymupdf
    py -3 tools/continuous_sprint/runner.py --repo . --source-dir 'D:\SR3-Original-PDFs' --results-dir 'D:\SR3-Drafts' --once --dry-run
    py -3 tools/continuous_sprint/runner.py --repo . --source-dir 'D:\SR3-Original-PDFs' --results-dir 'D:\SR3-Drafts' --max-parallel 2

The second command polls continuously while running. Stop using Ctrl+C. Default concurrency is two so the MSI is not overcommitted. Up to ten source owners are configured; a task is never reassigned across shards. Set --shard matrix, for example, to process only one owner. Set --once for a bounded pass.

For startup persistence, the computer owner must configure Task Scheduler or an OS service on the real host, running under a non-administrator account with access to the PDF mirror and authenticated Codex CLI. The computer must remain online. A self-hosted Linux/cloud server can use the same runner.

## Source integrity and safety

1. The source-to-worker allowlist is fixed in the runner. ShadowBeat/legacy does not own FASA7118; Corporate Security Handbook is exclusively owned by Sourcebook Mechanics. No unassigned mixed sources are automatically claimed.
2. Original physical PDF page indices must have an independently authenticated printed-to-PDF mapping before a job runs. Entries with an empty original_pdf_pages array are intentionally blocked, not guessed.
3. The runner compares original local PDF bytes to the live source-specific manifest SHA-256 and actually executes the repository preservation_method.py verify-source command. It renders the declared original physical page images with PyMuPDF and passes them directly as image attachments to Codex.
4. The model works in a temporary Git-metadata-free copy of the repository under workspace-write, not the canonical Git repository. GitHub tokens and Google Drive credential locations are omitted. Proposed YAML and a field-level report are copied to the results directory, never into the canonical repo.
5. Proposed records must later be independently source-authenticated against a fresh original Drive download, editorially reviewed with immutable BASELINE and same-substance CANDIDATE, transaction-staged and prepared, written through ordinary GitHub Contents API, read back and confirmed by the genuine ingestion gate, and source-specifically indexed with strict readback by the owning existing worker. This tool cannot waive any of those gates.
6. The accepted FASA7001 core (451 records), the global ledger, and the Denver printed p45/PDF46 boundary remain untouched. A proposed or no-op status is not a page advancement or source-closure certification.
7. A blocked job does not automatically re-run. Correct the problem and deliberately delete only its local status.json to retry; add distinct new source-owned natural-section jobs to the queue to continue processing.
8. Local source-image SHA verification is not proof of a fresh Drive acquisition or of a finished human-level source audit. The actual final source owner must independently validate before accepting.

## Tests

    python -m unittest discover -s tools/continuous_sprint -p 'test_*.py' -v

Tests cover ten ownership shards, illegal cross-shard jobs, path traversal, exact original SHA checks, missing physical page mappings, and refusal to accept a failed verify-source command. Tests do not claim Codex CLI, Google Drive access or a persistent cloud machine is configured.

## Deployment status

The code and queue exist in GitHub on a feature branch. NO persistent service is yet running on the MSI or a cloud machine, because that requires execution-machine access plus the source mirror and Codex credentials. Keep all ten existing hourly writers enabled until an actual continuously running host and safe handoff are verified. Never run a second autonomous publishing pipeline over their files.
