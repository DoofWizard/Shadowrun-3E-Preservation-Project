"""Fictional tabletop Matrix frame/agent builder, FASA7909 Shadowrun Third Edition.

FASA Corporation *Matrix* printed pp89-90/PDF90-91, original scan SHA-256
b5be5f7d6b51823ea51545b7816f3813ddc9f3bf4b674e4aa261030edbdb02fe.
Canonical rule: rules/matrix/matrix-frames-agents-design-operation-p88-91.yml.
Only deterministic design budgets/limits; no IC, Matrix intrusion or autonomous AI.
Consumer code, not source-transaction authorization or a new semantic record.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import ceil


class UndefinedFrameRule(ValueError):
    """Inputs violate source limits or invoke an unsupported frame mechanic."""


MULTIPLIER = {"dumb_frame": 3, "smart_frame": 6, "agent": 10}
FRAME_POINT_FACTOR = {"dumb_frame": 2, "smart_frame": 4, "agent": 6}


def _int(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise UndefinedFrameRule("noninteger or out-of-bounds game rating")
    return value


def maximum_frame_core(programming_skill, kind):
    skill = _int(programming_skill, 1)
    if kind == "dumb_frame": return 2 * skill
    if kind == "smart_frame": return 3 * skill // 2
    if kind == "agent": return skill
    raise UndefinedFrameRule("unknown original frame category")


@dataclass(frozen=True)
class FrameBudget:
    type: str
    core_rating: int
    core_size_mp: int
    persona_points_available: int
    frame_points_available: int
    spent_frame_points: int
    unspent_frame_points_lost: int
    hacking_pool: int
    total_initiative_dice: int | None


def design_frame(programming_skill, kind, core_rating,
                 persona_bod=0, persona_evasion=0, persona_masking=0, persona_sensor=0,
                 pilot=0, extra_initiative_dice=0, utility_payload=0):
    """Compute exact bounded point budget; caller validates loaded utility choices.

    Dumb frames inherit controller Reaction/Initiative (represented by None).
    Smart/agent Pilot minimum 1, capped by both core and programmer skill.
    Frame Points unspent after design vanish, not carried to future designs.
    """
    skill = _int(programming_skill, 1)
    rating = _int(core_rating, 1)
    if kind not in MULTIPLIER or rating > maximum_frame_core(skill, kind):
        raise UndefinedFrameRule("frame core exceeds type/programmer limit")
    attributes = [persona_bod, persona_evasion, persona_masking, persona_sensor]
    for a in attributes:
        if _int(a) > rating: raise UndefinedFrameRule("persona attribute exceeds core")
    persona = rating * (2 if kind == "agent" else 1)
    if sum(attributes) > persona: raise UndefinedFrameRule("too many Persona Points")
    _int(pilot); _int(extra_initiative_dice); _int(utility_payload)
    if kind == "dumb_frame":
        if pilot or extra_initiative_dice: raise UndefinedFrameRule("dumb frames have no independent Pilot/Initiative")
        dice = None
    else:
        if not 1 <= pilot <= min(skill, rating):
            raise UndefinedFrameRule("Pilot minimum and source maximum not met")
        if extra_initiative_dice > (3 if kind == "smart_frame" else 4):
            raise UndefinedFrameRule("total Initiative dice exceed 4D6/5D6 source cap")
        dice = 1 + extra_initiative_dice
    points = rating * FRAME_POINT_FACTOR[kind]
    spent = pilot * 2 + extra_initiative_dice * 3 + utility_payload
    if spent > points: raise UndefinedFrameRule("Frame Points exhausted")
    # The p78 published program-size table, not a rating × multiplier shortcut.
    return FrameBudget(kind, rating, rating * rating * MULTIPLIER[kind], persona,
                       points, spent, points - spent, rating if kind == "agent" else 0, dice)


def utility_reload_cost(utility_ratings):
    """p90: average Rating rounded up for test TN; rating squared ×2 days."""
    if type(utility_ratings) not in (list, tuple) or not utility_ratings:
        raise UndefinedFrameRule("complete utilities and rating list required")
    for rating in utility_ratings: _int(rating, 1)
    avg = ceil(sum(utility_ratings) / len(utility_ratings))
    return {"computer_programming_test_tn": avg, "base_time_days": avg * avg * 2}
