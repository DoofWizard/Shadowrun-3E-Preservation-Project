"""Original FASA7001 p111/PDF112 firearm range bands and base target numbers.

FASA Corporation, fictional tabletop RPG Shadowrun, Third Edition (SR3).
Canonical: rules/combat/range-target-number.yml, source.sr3-core.
Only the thirteen ordinary numeric firearm/heavy-weapon rows of the original
Weapon Range Table are included. Original grenade/missile launcher minimum
ranges, bows/STR scaling, and later Cannon Companion extensions are NOT
silently guessed. Consumer adapter, not source-review/transaction receipt.
"""
from __future__ import annotations
from dataclasses import dataclass
from rules_probe import UnresolvedRule

# Original p111/PDF112 end-of-range upper limits in meters, inclusive.
# In order: Short, Medium, Long, Extreme. The next range begins at previous+1.
# NO universal aliases: e.g. p279 Defiance T-250 short-barrel shotgun explicitly
# uses heavy-pistol ranges despite its shotgun ammunition classification.
RANGE_LIMITS_M = {
    "hold_out_pistol": (5, 15, 30, 50),
    "light_pistol": (5, 15, 30, 50),
    "heavy_pistol": (5, 20, 40, 60),
    "smg": (10, 40, 80, 150),
    "taser": (5, 10, 12, 15),
    "shotgun": (10, 20, 50, 100),
    "sporting_rifle": (100, 250, 500, 750),
    "sniper_rifle": (150, 300, 700, 1000),
    "assault_rifle": (50, 150, 350, 550),
    "light_machine_gun": (75, 200, 400, 800),
    "medium_machine_gun": (80, 250, 750, 1200),
    "heavy_machine_gun": (80, 250, 800, 1500),
    "assault_cannon": (100, 300, 900, 2400),
}
RANGE_CATEGORIES = ("short", "medium", "long", "extreme")
BASE_TARGET_NUMBERS = (4, 5, 6, 9)


@dataclass(frozen=True)
class RangeResolution:
    source_class: str
    distance_m: int
    category: str
    base_target_number: int | None
    in_range: bool


def resolve_weapon_range(source_class: str, distance_m: int) -> RangeResolution:
    """Lookup published base TN only; no cover, vision, recoil or model fixes.

    Input class must be a p111 named table row. Distance is integer meters
    (published bands are integral). Non-integral distances need an explicit
    measurement/rounding rule not supplied by this consumer adapter.
    """
    if source_class not in RANGE_LIMITS_M:
        raise UnresolvedRule(f"no unambiguous p111 firearm range for {source_class!r}")
    if type(distance_m) is not int or distance_m < 0:
        raise ValueError("distance must be a nonnegative integer number of meters")
    for index, upper in enumerate(RANGE_LIMITS_M[source_class]):
        if distance_m <= upper:
            return RangeResolution(source_class,distance_m,RANGE_CATEGORIES[index],BASE_TARGET_NUMBERS[index],True)
    return RangeResolution(source_class,distance_m,"beyond_extreme",None,False)
