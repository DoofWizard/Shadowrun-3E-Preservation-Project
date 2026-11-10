"""Small deterministic probes for *Shadowrun Companion* SR3 game rules.

Historical fictional tabletop publication: FASA Corporation FASA7905a,
original printed pp32-34/PDF33-35 and pp44-48/PDF45-49. Implementations
below intentionally omit GM discretion and any unconfirmed rounding cases.
Not a complete gameplay engine, and not real-world health guidance.
"""
from fractions import Fraction

RULE_IDS = {
    "ghoul_creation": "option.character-creation.srcomp-ghoul-player-characters",
    "ghoul_infection": "rule.character-creation.srcomp-ghoul-krieger-infection",
    "climbing": "rule.skills.srcomp-athletics-climbing-falling-escape",
    "motion": "rule.skills.srcomp-athletics-motion-fatigue-water",
}


class UnresolvedRule(ValueError):
    """The source provides no unique outcome without further authoritative input."""


def _nonnegative_integer(x: int) -> int:
    if type(x) is not int or x < 0:
        raise ValueError("expected nonnegative integer")
    return x


def ghoul_exposure_outcome(successes: int) -> str:
    """FASA7905a printed p33: fictional initial Body infection success table."""
    _nonnegative_integer(successes)
    return ("infected", "permanent-effect-at-gm-discretion", "temporary-sickness", "no-effect-carrier-possible")[min(successes, 3)]


def ghoul_stage3_modifiers(successes: int) -> dict[str, int]:
    """FASA7905a printed p33: optional transformation Willpower (6) table.

    These are ONLY stage-three modifiers; the p34 Ghoul Characteristics Table
    is cumulative and is intentionally not folded into this result.
    """
    _nonnegative_integer(successes)
    if successes == 0:
        return {"intelligence": -2, "charisma": -2}
    if successes == 1:
        return {"intelligence": -1, "charisma": -1}
    if successes == 2:
        return {"charisma": -1}
    if successes == 3:
        return {}
    return {"willpower": 1}


def ghoul_starting_build_point_surcharge() -> int:
    """FASA7905a printed p34: +10 above base race cost; points, not nuyen."""
    return 10


def climbing_target_number(surface: str, height_band: str, condition: str = "ordinary") -> int:
    """FASA7905a p46/PDF47: explicit base, height and ONE surface condition.

    Caller chooses the printed height band and a single condition rather than
    speculating about treatment precedence or fractional boundary handling.
    """
    surface_map = {"easy": 3, "broken": 5, "flat": 8, "sheer": 14}
    height_map = {"under_2m": 0, "2_to_4m": 2, "above_4m": 4}
    condition_map = {"ordinary": 0, "wet": 2, "greased": 4}
    if surface not in surface_map or height_band not in height_map or condition not in condition_map:
        raise ValueError("unknown table category")
    return surface_map[surface] + height_map[height_band] + condition_map[condition]


def escape_artist_timing(restraint: str, successes: int) -> tuple[Fraction | None, int]:
    """FASA7905a p46/PDF47: (elapsed minutes on success, retry wait on fail).

    No unsupported rounding: Fraction retains exact source division.
    """
    tn = {"ropes": 4, "handcuffs": 6, "straitjacket": 8, "manacles": 10}.get(restraint)
    if tn is None:
        raise ValueError("unknown restraint table value")
    _nonnegative_integer(successes)
    return (Fraction(5 * tn, successes) if successes else None, 5 * tn)


def fall_profile_for_even_meters(meters: int, impact_armor: int, athletics_successes: int = 0) -> tuple[int, str]:
    """FASA7905a p46/PDF47: deterministic fall Power/Level for even distances.

    Refuse odd-meter power: source specifies flooring impact armor half but
    does not separately resolve integer rounding of distance / 2.
    """
    if type(meters) is not int or meters < 1:
        raise ValueError("positive whole meters required")
    _nonnegative_integer(impact_armor)
    _nonnegative_integer(athletics_successes)
    if meters % 2:
        raise UnresolvedRule("half-distance Power at odd meter count: authoritative rounding needed")
    level = "L" if meters <= 2 else "M" if meters <= 6 else "S" if meters <= 20 else "D"
    return meters // 2 - impact_armor // 2 - athletics_successes, level


def fatigue_period_turns(body: int) -> int:
    """FASA7905a p47/PDF48: sprint period, ceiling Body/2."""
    if type(body) is not int or body < 1:
        raise ValueError("positive Body needed")
    return (body + 1) // 2


def fatigue_power_for_period(period: int) -> int:
    """FASA7905a p47/PDF48: repeated 4L Stun Power doubling."""
    if type(period) is not int or period < 1:
        raise ValueError("period must be >=1")
    return 4 * 2 ** (period - 1)


def effective_running_quickness(quickness: int, athletics_successes: int) -> int:
    """FASA7905a p47/PDF48: effective Quickness for this Combat Phase only."""
    if type(quickness) is not int or quickness < 1:
        raise ValueError("positive Quickness needed")
    _nonnegative_integer(athletics_successes)
    return quickness + athletics_successes


def normal_swimming_distance(running_distance: int) -> Fraction:
    """FASA7905a p47/PDF48: ordinary distance is one fifth of running."""
    _nonnegative_integer(running_distance)
    return Fraction(running_distance, 5)


def breath_hold_turns(athletics_successes: int) -> int:
    """FASA7905a pp47-48/PDF48-49: 15 turns plus 3 per success."""
    _nonnegative_integer(athletics_successes)
    return 15 + 3 * athletics_successes
