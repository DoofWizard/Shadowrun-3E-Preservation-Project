"""Source-limited optional Deadlier Over-Damage consumer for SR3.

FASA Corporation, *Shadowrun, Third Edition*, FASA7001 (fictional tabletop
RPG), original printed p126/physical PDF127. Existing gated canonical record:
``rules/combat/sr3-core-optional-deadlier-overdamage-p126.yml``.
Original PDF SHA-256: 7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914.

This is NOT a default damage rule. It receives an already-staged damage level
and remaining excess attack successes, not dice, recoil or damage resistance.
The outcome returns *additional* boxes only; caller updates the appropriate
track after resolving the baseline Deadly damage. It keeps an unmatched extra
success explicit rather than inventing an extra-damage rounding rule.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class OptionalOverdamage:
    activated: bool
    extra_physical_monitor_boxes: int
    extra_body_overflow_points: int
    unused_unpaired_successes: int


def optional_overdamage(*, enabled: bool, body: int, attack_power: int,
                        staged_damage_level: str, damage_type: str,
                        excess_successes_after_deadly: int,
                        deadlier_variant: bool = False) -> OptionalOverdamage:
    """Resolve only the optional p126 overdamage add-on, with strict '>' test.

    With default option, Power > Body*1.5. With the source's even-deadlier
    alternative, Power > Body. Eligibility additionally requires Deadly stage;
    every pair of excess successes adds one point. Extra Deadly Stun affects
    the Physical track; extra Deadly Physical affects Body Overflow.
    """
    if type(enabled) is not bool or type(deadlier_variant) is not bool:
        raise ValueError("optional rule and variant selectors must be booleans")
    if type(body) is not int or body < 1:
        raise ValueError("Body must be a positive integer")
    if type(attack_power) is not int or attack_power < 0:
        raise ValueError("Attack Power must be a nonnegative integer")
    if type(excess_successes_after_deadly) is not int or excess_successes_after_deadly < 0:
        raise ValueError("excess successes must be a nonnegative integer")
    if staged_damage_level not in ("L", "M", "S", "D"):
        raise ValueError("staged damage level must be L/M/S/D")
    if damage_type not in ("Physical", "Stun"):
        raise ValueError("damage type must be Physical or Stun")

    eligible = enabled and staged_damage_level == "D" and (
        attack_power > body if deadlier_variant else 2 * attack_power > 3 * body
    )
    if not eligible:
        return OptionalOverdamage(False, 0, 0, 0)
    extra, remainder = divmod(excess_successes_after_deadly, 2)
    if damage_type == "Physical":
        return OptionalOverdamage(True, 0, extra, remainder)
    return OptionalOverdamage(True, extra, 0, remainder)
