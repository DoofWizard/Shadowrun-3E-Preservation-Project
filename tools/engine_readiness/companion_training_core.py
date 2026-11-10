"""Bounded optional SR3 training mechanics. FASA Corporation Shadowrun Companion,
FASA7905a, Shadowrun Third Edition, printed pp48-51/PDF49-52.
Source SHA256: 8c52409108459a130ff6292722d98dc1f7a65cf870e63e363c34dc1dc299afd5.
Canonical: rules/skills/srcomp-optional-training-exact-p48-51.yml.
Consumer prototype ONLY; skill tests, instructor qualification and GM choices are external.
"""
from fractions import Fraction


class UnresolvedTrainingRule(ValueError):
    """Source does not uniquely specify this requested combination."""


def _int(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("integer outside source-defined input bounds")
    return value


def _ceil(a, b):
    return (a + b - 1) // b


def skill_base_days(karma, kind):
    """FASA7905a p49: Active x7; Knowledge/Language x15."""
    factor = {"active": 7, "knowledge": 15, "language": 15}.get(kind)
    if factor is None:
        raise ValueError("unknown skill category")
    return _int(karma, 1) * factor


def training_days(base_days, test_successes, teacher_successes=0):
    """pp49-50: ceil(base / (skill successes + floor(instruction successes/2)));
    with no combined successes multiply the base days by 1.5 and round up."""
    base = _int(base_days, 1)
    hits = _int(test_successes) + _int(teacher_successes) // 2
    return _ceil(base, hits) if hits else _ceil(base * 3, 2)


def attribute_training_days(karma, attribute_hits, teacher_hits=0):
    """p51: 7 days per required Good Karma; attribute test TN6 externally."""
    return training_days(7 * _int(karma, 1), attribute_hits, teacher_hits)


def interruption_remaining_days(remaining, intelligence, new_rating, absent):
    """p49 worked example: a qualifying interruption doubles remainder 5 -> 10.
    Printed text calls this 'extra training'; do NOT add it again to remaining."""
    remaining = _int(remaining)
    threshold = _int(intelligence, 1) + _int(new_rating, 1)
    return 2 * remaining if _int(absent) >= threshold else remaining


def baseline_daily_hours(willpower):
    """p50: ceil(Willpower/2)+4, subject to physical 24h ceiling."""
    return min(24, (_int(willpower, 1) + 1) // 2 + 4)


def effective_daily_hours(willpower, extra_declared, willpower_tn10_hits):
    """pp50-51: each Willpower(10) hit makes one declared extra hour effective."""
    limit = baseline_daily_hours(willpower)
    extra = _int(extra_declared)
    hits = _int(willpower_tn10_hits)
    if limit + extra > 24:
        raise ValueError("cannot declare more than 24 clock hours")
    return limit + min(extra, hits)


def calendar_days(training_day_units, effective_daily_hours_value):
    """p51: a training-day unit = 4 hours of effective practice."""
    days, hours = _int(training_day_units, 1), _int(effective_daily_hours_value, 1)
    if hours > 24:
        raise ValueError("invalid daily hours")
    return _ceil(days * 4, hours)


def instructor_base_fee(instruction_rating):
    """p50 suggested nuyen/day, GM-overridable."""
    n = _int(instruction_rating, 1)
    return {1:40, 2:50, 3:75, 4:100, 5:200, 6:400}.get(n,400+100*(n-6))


def subject_rating_fee_factor(subject_rating):
    """p50 table: 2-3: -25%; 4-5: zero; 6-7: +25%; 8+: +50%."""
    n = _int(subject_rating, 2)
    return Fraction(3,4) if n<=3 else Fraction(1) if n<=5 else Fraction(5,4) if n<=7 else Fraction(3,2)


def instructor_daily_fee(instruction_rating, subject_rating, *, specialization=False,
                         classroom=False, longer_than_four_hours=False):
    """Exact fraction, one additional adjustment; stacked percentage ordering
    isn't specified in the source, so combination needs a GM decision."""
    flags = (specialization, classroom, longer_than_four_hours)
    if not all(type(flag) is bool for flag in flags):
        raise ValueError("fee options must be booleans")
    if sum(flags)>1:
        raise UnresolvedTrainingRule("combining multiple fee adjustments requires GM ruling")
    factor = subject_rating_fee_factor(subject_rating)
    if specialization or longer_than_four_hours:
        factor *= Fraction(3,2)
    if classroom:
        factor *= Fraction(1,2)
    return instructor_base_fee(instruction_rating) * factor
