"""Deterministic SR3 tabletop test reference for the VGA/SCUMM adapter.

Inputs are *recorded dice*, one list per base die. No RNG, graphics or lore.
Implemented only where the existing canonical SR3 records support behavior.

Sources (archive paths, not original-page re-verification):
  rules/tests/{making-tests,success-test,target-numbers,rule-of-one,rule-of-six,
               open-test,opposed-test,success-contest}.yml
  rules/initiative/{initiative,initiative-passes}.yml

Unimplemented intentionally: combat damage, magic, Matrix, rigging, NPC AI,
defaulting, special-case ties, and any rules not explicitly mapped above.
"""

from collections.abc import Mapping, Sequence


def _integer(value: int, name: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _faces(dice: Sequence[Sequence[int]]) -> list[list[int]]:
    if not dice:
        raise ValueError("At least one die is required; zero-dice/defaulting is not implemented")
    checked: list[list[int]] = []
    for index, chain in enumerate(dice):
        if not chain:
            raise ValueError(f"Die {index} has no recorded face")
        result = [_integer(face, f"die {index} face", 1) for face in chain]
        if any(face > 6 for face in result):
            raise ValueError(f"Die {index} has a face outside 1..6")
        checked.append(result)
    return checked


def _resolve_chain(chain: Sequence[int], *, target: int | None) -> int:
    """Resolve *one* die. For a fixed TN, stop once success is secured."""
    total = 0
    for pos, face in enumerate(chain):
        if pos > 0 and chain[pos - 1] != 6:
            raise ValueError("Continuation may only follow a rolled 6")
        if target is not None and pos > 0 and total >= target:
            raise ValueError("Extra continuation after target was already met")
        total += face
        explode = face == 6 and (target is None or total < target)
        if explode and pos == len(chain) - 1:
            raise ValueError("Missing required follow-up face after a 6")
        if not explode and pos < len(chain) - 1:
            raise ValueError("Extra faces after a completed die")
    return total


def success_test(
    dice: Sequence[Sequence[int]],
    base_target: int,
    modifiers: Sequence[int] = (),
) -> dict:
    """Count separate dice meeting SR3 target number; Rule of One is all base 1s.

    Example: success_test([[6, 1], [3], [1]], 7) has one success.
    For TN <= 6, a 6 succeeds without a continuation.
    """
    _integer(base_target, "base_target") if base_target >= 0 else _integer(base_target, "base_target", -1000000)
    mods = tuple(modifiers)
    for mod in mods:
        if isinstance(mod, bool) or not isinstance(mod, int):
            raise ValueError("Modifiers must be integers")
    target = max(2, base_target + sum(mods))
    chains = _faces(dice)
    totals = [_resolve_chain(chain, target=target) for chain in chains]
    return {
        "rule_id": "rule.tests.success-test",
        "target": target,
        "rolls": chains,
        "die_totals": totals,
        "successes": sum(total >= target for total in totals),
        "rule_of_one": all(chain[0] == 1 for chain in chains),
    }


def open_test(dice: Sequence[Sequence[int]]) -> dict:
    """Return highest individually exploded die, not sum of different dice."""
    chains = _faces(dice)
    totals = [_resolve_chain(chain, target=None) for chain in chains]
    return {
        "rule_id": "rule.tests.open-test",
        "rolls": chains,
        "die_totals": totals,
        "result": max(totals),
        "rule_of_one": all(chain[0] == 1 for chain in chains),
    }


def compare_successes(a: Mapping, b: Mapping) -> dict:
    """Tie remains unresolved. Never apply melee's attacker-tie exception here."""
    a_successes = _integer(a["successes"], "a.successes")
    b_successes = _integer(b["successes"], "b.successes")
    return {
        "rule_id": "rule.tests.success-contest",
        "a_successes": a_successes,
        "b_successes": b_successes,
        "net_a": a_successes - b_successes,
        "winner": "A" if a_successes > b_successes else ("B" if b_successes > a_successes else None),
        "tie": a_successes == b_successes,
    }


def opposed_test(
    a_rating: int,
    a_dice: Sequence[Sequence[int]],
    b_rating: int,
    b_dice: Sequence[Sequence[int]],
) -> dict:
    """Simplest opposed-rating test; other situational modifiers not yet modeled."""
    _integer(a_rating, "a_rating", 1)
    _integer(b_rating, "b_rating", 1)
    if len(a_dice) != a_rating or len(b_dice) != b_rating:
        raise ValueError("Opposed-test dice must equal provided ratings in v0")
    a = success_test(a_dice, b_rating)
    b = success_test(b_dice, a_rating)
    outcome = compare_successes(a, b)
    outcome["rule_id"] = "rule.tests.opposed-test"
    outcome["a"] = a
    outcome["b"] = b
    return outcome


def initiative(reaction: int, dice: Sequence[int]) -> dict:
    """SR3 initiative dice are added normally; the Rule of Six is excluded."""
    _integer(reaction, "reaction")
    if not dice:
        raise ValueError("At least one Initiative die is required")
    for index, face in enumerate(dice):
        _integer(face, f"initiative die {index}", 1)
        if face > 6:
            raise ValueError("Initiative faces must be in 1..6")
    return {
        "rule_id": "rule.initiative.initiative",
        "reaction": reaction,
        "rolls": list(dice),
        "score": reaction + sum(dice),
        "exploding_sixes": False,
    }


def initiative_passes(scores: Mapping[str, int]) -> list[dict]:
    """Group tied scores; canonical tie-break rules are not modeled in v0.

    The first pass uses original scores. Subtract ten each subsequent pass.
    """
    if not scores:
        return []
    for name, score in scores.items():
        if not isinstance(name, str) or not name:
            raise ValueError("Actor identifiers must be nonempty strings")
        _integer(score, f"initiative score for {name}")
    result: list[dict] = []
    round_index = 0
    while True:
        eligible = [(name, score - 10 * round_index) for name, score in scores.items()
                    if score - 10 * round_index > 0]
        if not eligible:
            break
        groups: dict[int, list[str]] = {}
        for name, current in eligible:
            groups.setdefault(current, []).append(name)
        result.append({
            "pass": round_index + 1,
            "order_groups": [
                {"score": score, "actors": sorted(groups[score])}
                for score in sorted(groups, reverse=True)
            ],
            "tie_breaks_unresolved": any(len(names) > 1 for names in groups.values()),
        })
        round_index += 1
    return result
