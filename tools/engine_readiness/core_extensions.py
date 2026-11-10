"""Source-reviewed SR3 core numeric adapters; not canonical archival records.

FASA Corporation, Shadowrun Third Edition, FASA7001. Creation table:
printed p54/PDF55. Initiative tie-break: p102/PDF103. Ranged outcome:
p113/PDF114. All functions consume pre-resolved counts, not random rolls.
"""
from __future__ import annotations
from dataclasses import dataclass
from rules_probe import UnresolvedRule, _d6, staged_damage


# Numerical source from FASA Corporation, Shadowrun Third Edition,
# FASA7001 printed p54/PDF55; associated magic descriptions p54-55/PDF55-56.
# An adapter for testable code, NOT a canonical ingestion record.
PRIORITY_BUDGETS = {
    "A": {"Attributes": 30, "Skills": 50, "Resources": 1_000_000},
    "B": {"Attributes": 27, "Skills": 40, "Resources": 400_000},
    "C": {"Attributes": 24, "Skills": 34, "Resources": 90_000},
    "D": {"Attributes": 21, "Skills": 30, "Resources": 20_000},
    "E": {"Attributes": 18, "Skills": 27, "Resources": 5_000},
}
RACE_PRIORITY = {"human": "E", "dwarf": "D", "ork": "D", "elf": "C", "troll": "C"}
MAGIC_PRIORITY = {"full_magician": "A", "aspected_magician": "B", "adept": "B"}


def starting_character_budget(priorities: dict[str, str], race: str,
                              magic: str) -> dict[str, int]:
    """Validate exact SR3 priority assignments and report starting numeric budgets.

    Does not replace the full creation procedure, racial modifiers, Essence,
    skill selection, additional magic restrictions, or shopping rules.
    """
    categories = {"Race", "Magic", "Attributes", "Skills", "Resources"}
    if set(priorities) != categories or set(priorities.values()) != set("ABCDE"):
        raise ValueError("assign A-E exactly once to the five categories")
    if race not in RACE_PRIORITY:
        raise ValueError("unknown baseline metatype")
    if priorities["Race"] != RACE_PRIORITY[race]:
        raise ValueError("race-priority restriction from Master Creation Table")
    if magic != "mundane":
        if magic not in MAGIC_PRIORITY or priorities["Magic"] != MAGIC_PRIORITY[magic]:
            raise ValueError("magical-character priority restriction")
    return {
        "attribute_points": PRIORITY_BUDGETS[priorities["Attributes"]]["Attributes"],
        "skill_points": PRIORITY_BUDGETS[priorities["Skills"]]["Skills"],
        "nuyen": PRIORITY_BUDGETS[priorities["Resources"]]["Resources"],
    }


def initiative_tie_winner(first_pass: tuple[int, int],
                          adjusted_reaction: tuple[int, int],
                          natural_reaction: tuple[int, int],
                          dice_rolls: tuple[list[int], list[int]] = ([], [])) -> str:
    """Resolve a *two-actor* initiative tie from FASA7001 p102/PDF103.

    Use first-pass Initiative, adjusted Reaction, natural Reaction, then a
    repeated 1D6 tie-break. Caller handles voluntary action delay separately.
    """
    for pair in (first_pass, adjusted_reaction, natural_reaction):
        if len(pair) != 2 or any(type(x) is not int for x in pair):
            raise ValueError("two integer score values required at every stage")
        if pair[0] != pair[1]:
            return "A" if pair[0] > pair[1] else "B"
    if len(dice_rolls) != 2:
        raise ValueError("supply two die streams")
    for a, b in zip(*dice_rolls):
        a, b = _d6(a), _d6(b)
        if a != b:
            return "A" if a > b else "B"
    raise UnresolvedRule("initiative dice tie persists or missing next reroll")


@dataclass(frozen=True)
class RangedOutcome:
    result: str
    damage_level: str
    total_defender_successes: int


def ranged_outcome(attack_successes: int, dodge_successes: int,
                   damage_resistance_successes: int, base_damage: str) -> RangedOutcome:
    """FASA7001 p113/PDF114 after all attack/dodge/resistance dice are rolled.

    Distinguishes an attack miss, Dodge > attack (complete dodge), and partial
    dodge successes that *also* count toward resistance. This does NOT roll
    Body, calculate armor/Power, manage dice pools, or apply Condition Monitor.
    """
    values = (attack_successes, dodge_successes, damage_resistance_successes)
    if any(type(x) is not int or x < 0 for x in values):
        raise ValueError("nonnegative integer success counts required")
    if base_damage not in ("L", "M", "S", "D"):
        raise ValueError("invalid SR3 damage level")
    combined = dodge_successes + damage_resistance_successes
    if attack_successes == 0:
        return RangedOutcome("miss", "none", combined)
    if dodge_successes > attack_successes:
        return RangedOutcome("dodged", "none", combined)
    final = staged_damage(base_damage, attack_successes, combined)
    return RangedOutcome("hit-no-damage" if final == "none" else "hit", final, combined)
