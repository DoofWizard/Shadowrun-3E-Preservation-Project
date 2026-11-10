"""Original FASA7001 Third Edition printed p126/PDF127 optional-rule vectors."""
import unittest
from overdamage_core import optional_overdamage


def result(**override):
    d = dict(enabled=True, body=4, attack_power=7, staged_damage_level="D",
             damage_type="Physical", excess_successes_after_deadly=4)
    d.update(override)
    return optional_overdamage(**d)


class OriginalSR3DeadlierOverdamage(unittest.TestCase):
    def test_primary_threshold_strict_greater(self):
        self.assertFalse(result(attack_power=6).activated)

    def test_primary_above_threshold(self):
        x = result()
        self.assertTrue(x.activated)
        self.assertEqual((x.extra_body_overflow_points, x.extra_physical_monitor_boxes), (2, 0))

    def test_stun_goes_to_physical_monitor(self):
        x = result(damage_type="Stun")
        self.assertEqual((x.extra_body_overflow_points, x.extra_physical_monitor_boxes), (0, 2))

    def test_disabled_is_not_baseline_mechanics(self):
        self.assertFalse(result(enabled=False).activated)
        self.assertEqual(result(enabled=False).extra_body_overflow_points, 0)

    def test_only_deadly_stage_qualifies(self):
        for level in ("L", "M", "S"):
            with self.subTest(level=level):
                self.assertFalse(result(staged_damage_level=level).activated)

    def test_even_deadlier_alternative_body_threshold(self):
        self.assertTrue(result(attack_power=5, deadlier_variant=True).activated)
        self.assertFalse(result(attack_power=4, deadlier_variant=True).activated)

    def test_primary_option_does_not_use_alternative_threshold(self):
        self.assertFalse(result(attack_power=5, deadlier_variant=False).activated)

    def test_threshold_odd_body_uses_exact_integer_arithmetic(self):
        # Body 5 -> 1.5*Body=7.5, so Power=7 fails and Power=8 succeeds.
        self.assertFalse(result(body=5, attack_power=7).activated)
        self.assertTrue(result(body=5, attack_power=8).activated)

    def test_one_unpaired_extra_success_not_invented_as_damage(self):
        x = result(excess_successes_after_deadly=5)
        self.assertEqual((x.extra_body_overflow_points, x.unused_unpaired_successes), (2, 1))

    def test_no_extra_successes_no_overdamage_points(self):
        x = result(excess_successes_after_deadly=0)
        self.assertTrue(x.activated)
        self.assertEqual(x.extra_body_overflow_points, 0)

    def test_single_success_explicit_remainder(self):
        x = result(excess_successes_after_deadly=1)
        self.assertEqual((x.extra_body_overflow_points, x.unused_unpaired_successes), (0, 1))

    def test_reject_nonboolean_selectors(self):
        with self.assertRaises(ValueError): result(enabled=1)
        with self.assertRaises(ValueError): result(deadlier_variant="yes")

    def test_reject_bad_numeric_inputs(self):
        for field, val in (("body", 0), ("body", True), ("attack_power", -1),
                           ("excess_successes_after_deadly", -1),
                           ("excess_successes_after_deadly", 1.5)):
            with self.subTest(field=field, val=val), self.assertRaises(ValueError):
                result(**{field: val})

    def test_reject_unknown_damage_type_or_level(self):
        with self.assertRaises(ValueError): result(damage_type="Magic")
        with self.assertRaises(ValueError): result(staged_damage_level="deadly")


if __name__ == '__main__':
    unittest.main()
