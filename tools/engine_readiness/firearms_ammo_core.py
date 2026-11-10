"""Conservative Shadowrun Third Edition ammunition *class* adapter.

FASA Corporation, Shadowrun Third Edition FASA7001 original fictional RPG.
Source printed p279/PDF288 (ammunition-sharing rule) AND printed p111/PDF112
(Weapon Range Table category authority); original scan SHA256 begins 7661ba95.
Canonical original rule: rules/firearms/sr3-core-ammunition-class-compatibility-p279.yml.

No projectile engineering, calibers, ammo availability, specialized rounds,
weapon assembly, or Rigger 3 revisions. Consumer code, not archival ingestion.
"""
from rules_probe import UnresolvedRule


# Source p111 table's named firearm/weapon categories. No 'rifle' umbrella.
# Specialized taser/cannon/launcher projectiles have source-specific rules
# not resolved here, and must be checked separately.
# For a pistol-format shotgun, the p279 explicit exception points to the
# single Shotgun category in that table, despite different physical form.
FIREARM_RANGE_CLASSES = frozenset({
    "hold_out_pistol", "light_pistol", "heavy_pistol", "smg",
    "shotgun", "sporting_rifle", "sniper_rifle", "assault_rifle",
    "light_machine_gun", "medium_machine_gun", "heavy_machine_gun",
})
SHOTGUN_FORMS = {"shotgun_pistol": "shotgun", "shotgun_rifle": "shotgun"}


def source_range_class(class_from_p111: str) -> str:
    """Normalize only known class labels and the explicit shotgun exception.

    This is not a weapon-model classifier; callers must obtain actual source
    classification from the original p111 table or other verified mapping.
    """
    if type(class_from_p111) is not str:
        raise ValueError("source Weapon Range Table category must be text")
    value = SHOTGUN_FORMS.get(class_from_p111, class_from_p111)
    if value not in FIREARM_RANGE_CLASSES:
        raise UnresolvedRule(f"not a source-verified firearms category: {class_from_p111!r}")
    return value


def ammunition_classes_compatible(from_class: str, to_class: str) -> bool:
    """Class-based transfer per FASA7001 p279 and p111; no model guessing.

    Preserves the shotgun pistol/rifle cross-configuration allowance. The
    result only answers class matching; it does not identify compatible
    ammunition TYPES within a class or infer firearm caliber/round sizes.
    """
    return source_range_class(from_class) == source_range_class(to_class)
