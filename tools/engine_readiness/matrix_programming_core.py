"""Bounded executable rules for the fictional Shadowrun Third Edition tabletop game.

Source: FASA Corporation, Matrix (FASA7909), original printed pp76,
78-80 / original physical PDF pp77,79-81, scanned SHA-256
b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe.
Canonical records: rules/matrix/matrix-programming-rating-constraints-p76.yml
and rules/matrix/matrix-programming-size-plan-suite-team-p78-80.yml.
These pure functions are a consumer prototype: no dice rolls, no fictional
cyber-intrusion implementation, no archival ingestion or source authorization.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import ceil


class UnresolvedProgrammingRule(ValueError):
    """Input is insufficient or mechanics outside reviewed published pages."""


def _integer(value: int, label: str, minimum: int, maximum: int | None = None) -> int:
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{label} must be an integer in the sourced range")
    return value


def program_size_mp(rating: int, multiplier: int) -> int:
    """FASA7909 p78/PDF79 original size table: rating² × multiplier.

    Bounded to the table's published rating 1–14 and multipliers 1–10.
    Caller must source the correct multiplier from the selected utility.
    """
    return _integer(rating, "rating", 1, 14) ** 2 * _integer(multiplier, "multiplier", 1, 10)


def programming_suite_size_mp(rating: int) -> int:
    """FASA7909 p79/PDF80: 15 × suite rating squared, table 1–10."""
    return 15 * _integer(rating, "suite rating", 1, 10) ** 2


@dataclass(frozen=True)
class Plan:
    design_tn_before_global_minimum: int
    preparation_hours: int
    preparation_memory_mp: int
    test_tn_reduction_per_success: int = 1


def programming_plan(program_rating: int, option_count: int, multiplier: int,
                     final_program_size_mp: int) -> Plan:
    """FASA7909 pp78-79/PDF79-80: planning table, hours, memory.

    Memory is floor(program size / 10), using the option-adjusted size input.
    Options' size effects must be sourced separately; no automatic guesses.
    """
    rating = _integer(program_rating, "rating", 1, 14)
    opts = _integer(option_count, "options", 0)
    mul = _integer(multiplier, "multiplier", 1, 10)
    size = _integer(final_program_size_mp, "program size", 1)
    bracket = -1 if rating <= 4 else (0 if rating <= 9 else 1)
    return Plan(4 + bracket + opts, (rating + opts) * mul, size // 10)


def required_programming_memory_mp(final_program_size_mp: int) -> tuple[int, int]:
    """p78/PDF79: need at least program size in BOTH active and storage Mp."""
    size = _integer(final_program_size_mp, "program size", 1)
    return size, size


def programming_test_tn(program_rating: int, plan_successes: int | None = None,
                        double_memory: bool = False,
                        mainframe_color: str | None = None) -> int:
    """p79/PDF80 Computer (Programming) TN from the printed modifier table.

    None means no plan (+2); an integer means a created plan with that many
    source-rule successes (each -1). Caller proves memory/host eligibility.
    Target-number minimum 2 applies. Options do not raise base *test* TN.
    """
    rating = _integer(program_rating, "rating", 1, 14)
    if type(double_memory) is not bool:
        raise ValueError("double_memory must be a boolean")
    if plan_successes is not None:
        _integer(plan_successes, "plan successes", 0)
    color_mod = {None: 0, "blue": -1, "green": -2, "orange": -3, "red": -4}
    if mainframe_color not in color_mod:
        raise ValueError("unknown mainframe color")
    raw = rating + (2 if plan_successes is None else -plan_successes)
    raw += -2 if double_memory else 0
    raw += color_mod[mainframe_color]
    return max(2, raw)


def programming_days(final_program_size_mp: int, test_successes: int) -> int:
    """p79/PDF80: ceil(Mp / Computer (Programming) successes), 8h/day.

    Zero successes is a *different* failed-program case and requires a 2D6
    gamemaster roll; do not silently convert failure into successful code.
    """
    size = _integer(final_program_size_mp, "program size", 1)
    successes = _integer(test_successes, "test successes", 0)
    if successes == 0:
        raise UnresolvedProgrammingRule("zero success requires the separate GM 2D6 failure result")
    return (size + successes - 1) // successes


def failed_program_days(final_program_size_mp: int, gm_2d6_sum: int) -> int:
    """p79/PDF80 zero-success failed code: ceil(base Mp-days / 2D6)."""
    size = _integer(final_program_size_mp, "program size", 1)
    die_sum = _integer(gm_2d6_sum, "2D6 total", 2, 12)
    return (size + die_sum - 1) // die_sum


def plan_team(program_rating: int, member_skills: tuple[int, ...],
              single_programmer_task_days: int) -> dict[str, int]:
    """p80/PDF81 source example: highest skill determines team max/rating.

    One team Computer (Programming) test rolls floor(mean member skills);
    Task Pools alter the mean in source-specific ways NOT implemented here.
    Task period uses ceil(solo days / (team count+1)). A caller must separately
    validate each member's program memory and suitable programming-suite rating.
    """
    rating = _integer(program_rating, "rating", 1, 14)
    days = _integer(single_programmer_task_days, "single programmer days", 1)
    if not isinstance(member_skills, tuple) or not member_skills:
        raise ValueError("supply at least one member skill in a tuple")
    for skill in member_skills:
        _integer(skill, "team member Computer (Programming) skill", 1)
    top = max(member_skills)
    max_team = top // 2
    if len(member_skills) > max_team:
        raise ValueError("team exceeds maximum size based on highest skill")
    if rating > top:
        raise ValueError("program rating exceeds highest team member skill")
    return {"maximum_members": max_team,
            "maximum_program_rating": top,
            "test_skill_dice_before_task_pool": sum(member_skills) // len(member_skills),
            "minimum_days_each_member": (days + len(member_skills)) // (len(member_skills) + 1)}
