# Schema conventions

## 1. Sourcebooks are provenance, not hierarchy

Canonical game knowledge is organized by concept. Publications live under `sources/` and are referenced by records.

## 2. Stable identity

A record's `id` is permanent. Moving a file must not change its ID.

## 3. Keep kinds of knowledge separate

Do not turn every paragraph into an entity.

- **Entity**: what something is.
- **Rule**: how something behaves.
- **Procedure**: how a multi-step task is performed.
- **Option**: a selectable variation.
- **Modifier**: a conditional change.
- **Subsystem**: a stateful mechanical domain.
- **World record**: setting information.

## 4. Provenance is additive

A record may cite many sources. Each source contribution declares its relationship to the record: `defines`, `extends`, `clarifies`, `adds_option`, `adds_modifier`, `exception`, `replaces`, `supersedes`, `conversion`, `example`, `references`, or `errata`.

## 5. Effective/current rule state is explicit

Every canonical mechanical record may carry an `effective` block:

```yaml
effective:
  status: current
  source: source.sr3-core
  page: 38
  basis: defines
```

When a later source truly changes the rule, append a source contribution and update `effective` rather than deleting history.

Allowed effective statuses:
- `current` — this is the operative SR3 version represented by the record.
- `superseded` — retained for historical/source tracking but no longer operative.
- `optional` — only operative when that optional rule is enabled.
- `ambiguous` — sources conflict and the corpus does not clearly establish precedence.
- `conversion_only` — applies only when converting older-edition/source material.

"Latest" does **not** mean "newest publication automatically wins." Precedence is:
1. explicit errata/correction;
2. explicit replacement/supersession language;
3. explicit SR3 conversion/update instruction;
4. otherwise later material is treated as an extension, clarification, option, modifier, or exception rather than silently overwriting the earlier rule.

If two sources conflict without clear precedence, preserve both contributions and mark the record `ambiguous`.

## 6. Avoid monster schemas

Do not place every interaction on an entity itself. For example, a weapon's intrinsic statistics belong on the weapon entity; recoil, movement, ammunition interactions, smartlink interactions, vehicle firing, and wound effects belong in linked rules/options/modifiers.

## 7. Separate source statement from normalized interpretation

During ingestion, preserve:
- source provenance and page,
- concise normalized mechanical meaning,
- cross-record links,
- whether the contribution is current, superseded, optional, or unresolved,
- unresolved ambiguity.

Do not silently reconcile contradictions.

## 8. Optional rules remain optional

Optional systems and variants must be explicitly tagged and must never silently overwrite baseline SR3 behavior.

## 9. Cross-book compatibility is first-class

Edition conversions, sourcebook updates, and errata belong in `compatibility/` and may link to the canonical records they affect.

## 10. Source contributions are append-only in meaning

When a later source affects an existing record, preserve the earlier source entry. Never replace provenance merely because a newer source becomes effective.
