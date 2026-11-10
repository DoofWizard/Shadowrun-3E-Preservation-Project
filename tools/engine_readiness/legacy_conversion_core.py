"""Bounded consumer of source-verified SR3 FASA7001 historical conversion rules.

Source: FASA Corporation, Shadowrun Third Edition (FASA7001), printed
pp323-325 / physical PDF pp331-333. These are Second Edition conversion
only, not operative rules for newly created Third Edition characters.
Canonical anchors: rules/compatibility/sr2-to-sr3-numeric-character-conversion-p323.yml;
 sr2-to-sr3-magic-conversion-p324.yml; rigger2-to-sr3-vehicle-mechanics-p324.yml;
 vr2-to-sr3-matrix-mechanics-p325.yml.
No source-ingestion transaction or full rules-engine certification is implied.
"""

class UnresolvedConversion(ValueError):
    """Source does not authorize the requested extrapolation."""


def _nonnegative(value, field):
    if type(value) is not int or value < 0:
        raise UnresolvedConversion(f"{field} must be a nonnegative integer")
    return value


def sr2_metahuman_karma(race, old_pool, old_good_karma):
    """FASA7001 p323: elf/dwarf/ork/troll pool halves down, at least one."""
    if race not in {"elf", "dwarf", "ork", "troll"}:
        raise UnresolvedConversion("This conversion formula is only for listed SR2 metahumans")
    _nonnegative(old_pool, "old_pool")
    _nonnegative(old_good_karma, "old_good_karma")
    if old_pool < 1:
        raise UnresolvedConversion("A zero previous pool is not resolved by this paragraph")
    new_pool = max(1, old_pool // 2)
    return new_pool, old_good_karma + old_pool - new_pool


def available_knowledge_points(intelligence, existing_knowledge_ratings):
    """FASA7001 p323: 5*Intelligence less existing knowledge ratings."""
    _nonnegative(intelligence, "intelligence")
    if not isinstance(existing_knowledge_ratings, (tuple, list)):
        raise UnresolvedConversion("existing ratings must be a sequence")
    used = sum(_nonnegative(r, "existing rating") for r in existing_knowledge_ratings)
    remainder = intelligence * 5 - used
    if remainder < 0:
        raise UnresolvedConversion("Source provides no rule for overspent knowledge points")
    return remainder


def language_read_write_rating(language_skill_rating):
    """FASA7001 p323: read/write skill is floor(language skill / 2)."""
    return _nonnegative(language_skill_rating, "language_skill_rating") // 2


def converted_astral_initiative(intelligence, d6_roll):
    """FASA7001 p324: Intelligence + 20 + 1D6, rolled die 1..6."""
    _nonnegative(intelligence, "intelligence")
    if type(d6_roll) is not int or not 1 <= d6_roll <= 6:
        raise UnresolvedConversion("d6_roll must be a single 1..6 result")
    return intelligence + 20 + d6_roll


def spell_lock_disposition(lock_count, choice):
    """FASA7001 p324: each SR2 spell lock => Force-3 focus OR 45,000 nuyen."""
    _nonnegative(lock_count, "lock_count")
    if choice == "force_3_focus":
        return {"focus_count": lock_count, "focus_force": 3, "nuyen": 0}
    if choice == "sell":
        return {"focus_count": 0, "focus_force": None, "nuyen": lock_count * 45000}
    raise UnresolvedConversion("Unlisted spell-lock disposition")


def sustaining_focus_upgrade_cost(desired_force, gm_approved):
    """FASA7001 p324: GM-approved +15,000 nuyen per Force over 3, max 6."""
    if type(desired_force) is not int or not 3 <= desired_force <= 6:
        raise UnresolvedConversion("Upgrades are only described from Force 3 to at most Force 6")
    if gm_approved is not True:
        raise UnresolvedConversion("The source requires gamemaster discretion")
    return (desired_force - 3) * 15000


def passenger_combat_pool_cap(pool):
    """FASA7001 p324: attacked vehicle passenger may use floor(pool/2)."""
    return _nonnegative(pool, "pool") // 2


def vr2_ripper_mpcp_loss(test_successes):
    """FASA7001 p325: one MPCP rating lost per two Ripper test successes."""
    return _nonnegative(test_successes, "test_successes") // 2


def vr2_alert_reset_minutes(dice, alert_triggered):
    """FASA7001 p325: 3D6 only if neither passive nor active alert fired."""
    if alert_triggered is not False:
        raise UnresolvedConversion("No 3D6 reset rule is granted after an alert")
    if not isinstance(dice, (tuple, list)) or len(dice) != 3:
        raise UnresolvedConversion("3D6 needs exactly three die results")
    if any(type(d) is not int or not 1 <= d <= 6 for d in dice):
        raise UnresolvedConversion("Each die must be in 1..6")
    return sum(dice)
