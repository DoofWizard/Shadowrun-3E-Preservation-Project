# Schema validation fixtures

These are structural tests only. They are not ingested SR3 records.

## Fixture A — a weapon affected by several books

Expected representation:
- weapon itself -> **entity**
- base firing behavior -> **rule**
- ammunition behavior -> **entity + modifier/rule**
- accessory -> **entity or option**
- martial-arts interaction -> **option/rule**
- later source contribution -> additional provenance relation, not a duplicate weapon record

**Pass condition:** no need to add sourcebook-specific weapon folders or inflate the weapon entity with every combat interaction.

## Fixture B — cyberterminal construction

Expected representation:
- cyberterminal and components -> **entities**
- component choices -> **options**
- design/software/cook/installation flow -> **procedure**
- construction tests and constraints -> **rules/modifiers**
- cyberlimb or cranial installation -> linked **subsystem/procedure** interactions

**Pass condition:** construction can be expanded without changing the base entity schema.

## Fixture C — Matrix program options

Expected representation:
- utility/program -> **entity**
- programming -> **procedure**
- program option -> **option**
- option effect on rating/size/behavior -> **modifier/rule**
- incompatible options -> explicit links

**Pass condition:** options compose without duplicating program records.

## Fixture D — initiation/metamagic

Expected representation:
- initiation -> **subsystem + procedure**
- grade/state -> subsystem state
- metamagic technique -> **option**
- group/geas interactions -> linked options/modifiers/rules

**Pass condition:** magic expansion does not require a special ad-hoc schema.

## Fixture E — vehicle customization

Expected representation:
- vehicle -> **entity**
- modification -> **option/entity**
- construction/customization -> **procedure**
- changed statistics -> **modifiers**
- sensors/EW/remote networks -> linked **subsystems**

**Pass condition:** Rigger material can extend vehicles without replacing vehicle identity.

## Fixture F — optional campaign rules

Expected representation:
- optional rule package -> **option**
- contained mechanical changes -> linked **rules/modifiers/procedures**
- baseline remains untouched unless the option is enabled

**Pass condition:** optional material never silently becomes canonical baseline.

## Result

All six fixtures are representable with the current eight record types without adding a ninth type. The schema is therefore suitable for repository initialization and the next phase: controlled ingestion of the core rulebook.
