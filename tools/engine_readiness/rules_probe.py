"""SR3 source-provenance mechanics probe, NOT a complete game engine.

This is a deterministic executable-check layer for already-accepted Shadowrun,
Third Edition canonical records. It never fills missing source rules by guessing.
The original published material is fictional tabletop-RPG content.
"""
from __future__ import annotations
from dataclasses import dataclass

RULE_IDS = {
    "tests": "rule.tests.making-tests",       # FASA7001 p38
    "six": "rule.tests.rule-of-six",         # FASA7001 p38
    "one": "rule.tests.rule-of-one",         # FASA7001 p38
    "target": "rule.tests.target-numbers",    # FASA7001 p38
    "initiative": "rule.initiative.initiative-passes",  # FASA7001 p102
    "melee": "procedure.combat.melee-attack",      # FASA7001 pp122-123
    "staging": "rule.combat.damage-staging",       # FASA7001 pp113-114
    "reloading": "procedure.firearms.sr3-core-ammunition-reloading",  # FASA7001 p280
}


class UnresolvedRule(ValueError):
    """The archived rule needs an explicit additional input or table decision."""


def _d6(value: int) -> int:
    if type(value) is not int or not 1 <= value <= 6:
        raise ValueError("die must be an integer from 1 to 6")
    return value


@dataclass(frozen=True)
class TestResult:
    successes: int
    all_ones: bool
    die_totals: tuple[int, ...]
    target: int


def success_test(dice_chains: list[list[int]], target: int) -> TestResult:
    """Count per-die SR3 successes; explode each 6 only when needed to reach TN.

    Input includes explicit per-die sequences, making this function deterministic.
    Each die counts at most one success. A chain missing a required follow-up
    roll raises UnresolvedRule rather than fabricating RNG output.
    """
    if type(target) is not int:
        raise ValueError("target must be an integer")
    if not dice_chains:
        raise ValueError("cannot resolve an empty dice pool")
    tn = max(2, target)
    totals, first_rolls = [], []
    for chain in dice_chains:
        if not chain:
            raise ValueError("each die needs at least one roll")
        first = _d6(chain[0]); first_rolls.append(first)
        total = first
        if first == 6 and tn > 6:
            for extra in chain[1:]:
                if total >= tn or total % 6 != 0:
                    raise ValueError("unneeded extra exploding roll")
                total += _d6(extra)
            if total < tn and chain[-1] == 6:
                raise UnresolvedRule("missing follow-up roll after a six")
        elif len(chain) != 1:
            raise ValueError("unexpected extra rolls")
        totals.append(total)
    return TestResult(
        successes=sum(1 for x in totals if x >= tn),
        all_ones=all(x == 1 for x in first_rolls),
        die_totals=tuple(totals), target=tn,
    )


def initiative_total(reaction: int, initiative_dice: list[int]) -> int:
    """Initiative adds ordinary d6 totals to Reaction; sixes do not explode."""
    if type(reaction) is not int or reaction < 0 or not initiative_dice:
        raise ValueError("invalid initiative inputs")
    return reaction + sum(_d6(x) for x in initiative_dice)


def initiative_passes(scores: dict[str, int]) -> list[list[str]]:
    """Return ordered passes, subtracting ten after each pass.

    Initiative ties are not silently resolved here: a separate canonical
    tie-break rule is required before implementing tie handling.
    """
    if any(type(v) is not int for v in scores.values()):
        raise ValueError("initiative scores must be integer")
    current = dict(scores); passes = []
    while any(v > 0 for v in current.values()):
        live = [(k, v) for k, v in current.items() if v > 0]
        vals = [v for _, v in live]
        if len(vals) != len(set(vals)):
            raise UnresolvedRule("tie: consult rule.initiative.initiative-ties")
        passes.append([k for k, _ in sorted(live, key=lambda item: -item[1])])
        current = {k: v - 10 for k, v in current.items()}
    return passes


def opposed_result(successes_a: int, successes_b: int, melee: bool = False) -> str:
    if min(successes_a, successes_b) < 0:
        raise ValueError("negative successes")
    if successes_a == successes_b:
        return "attacker" if melee else "tie-no-result"
    return "attacker" if successes_a > successes_b else "defender"


def staged_damage(base: str, attack_successes: int, resistance_successes: int) -> str:
    """The canonical two-net-success staging step, not full combat resolution."""
    levels = ("L", "M", "S", "D")
    if base not in levels or min(attack_successes, resistance_successes) < 0:
        raise ValueError("invalid staging input")
    net = attack_successes - resistance_successes
    delta = abs(net) // 2 * (1 if net >= 0 else -1)
    index = levels.index(base) + delta
    if not 0 <= index < len(levels):
        raise UnresolvedRule("damage boundary: consult complete condition-monitor rules")
    return levels[index]


def reloading_options(code: str, quickness: int | None = None) -> list[tuple[str, int | str]]:
    """FASA7001 p280 confirmed reload table; no inferred rounding on odd Quickness."""
    codes = {"c", "b", "m", "cy", "belt"}
    if code not in codes:
        raise ValueError("unknown ammunition-feed code")
    if quickness is not None and (type(quickness) is not int or quickness < 1):
        raise ValueError("Quickness must be positive")
    if code == "c":
        return [("Simple", "clip insert/remove"), ("Complex", quickness if quickness is not None else "Quickness")]
    if code == "b":
        return [("Complex", 2)]
    if code == "m":
        return [("Complex", quickness if quickness is not None else "Quickness")]
    if code == "cy":
        return [("Complex", quickness if quickness is not None else "Quickness"), ("Complex", "speed loader")]
    if quickness is not None and quickness % 2:
        raise UnresolvedRule("p280 belt rounds Quickness/2: rounding unspecified in this table")
    return [("Complex", "insert belt"), ("Complex", quickness // 2 if quickness is not None else "Quickness/2")]
