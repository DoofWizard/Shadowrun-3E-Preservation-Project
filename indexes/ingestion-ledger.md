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

## Queue

The Google Drive corpus will be entered here source-by-source as it is processed.
