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

## 5. Avoid monster schemas

Do not place every interaction on an entity itself. For example, a weapon's intrinsic statistics belong on the weapon entity; recoil, movement, ammunition interactions, smartlink interactions, vehicle firing, and wound effects belong in linked rules/options/modifiers.

## 6. Separate source statement from normalized interpretation

During later ingestion, preserve:
- source provenance and page,
- concise normalized mechanical meaning,
- cross-record links,
- unresolved ambiguity.

Do not silently reconcile contradictions.

## 7. Optional rules remain optional

Optional systems and variants must be explicitly tagged and must never silently overwrite baseline SR3 behavior.

## 8. Cross-book compatibility is first-class

Edition conversions, sourcebook updates, and errata belong in `compatibility/` and may link to the canonical records they affect.
