"""Standard-library regression vectors for the reference resolver.

Run: python -m unittest discover -s game-adapters/scumm-vga256/tests -v
"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from reference_resolver import (
    compare_successes, initiative, initiative_passes,
    open_test, opposed_test, success_test,
)


class CoreSR3Vectors(unittest.TestCase):
    def test_each_die_counts_separately(self):
        result = success_test([[6, 1], [4], [1]], 7)
        self.assertEqual(result["die_totals"], [7, 4, 1])
        self.assertEqual(result["successes"], 1)

    def test_six_succeeds_at_six_without_explosion(self):
        self.assertEqual(success_test([[6], [1]], 6)["successes"], 1)

    def test_six_plus_one_succeeds_at_seven(self):
        self.assertEqual(success_test([[6, 1]], 7)["successes"], 1)

    def test_consecutive_explosions(self):
        self.assertEqual(success_test([[6, 6, 3]], 15)["die_totals"], [15])
        self.assertEqual(success_test([[6, 6, 3]], 15)["successes"], 1)

    def test_rule_of_one_all_base_ones(self):
        result = success_test([[1], [1], [1]], 4)
        self.assertTrue(result["rule_of_one"])
        self.assertEqual(result["successes"], 0)

    def test_rule_of_one_not_just_one_one(self):
        self.assertFalse(success_test([[1], [2]], 5)["rule_of_one"])

    def test_target_number_floor_after_modifiers(self):
        result = success_test([[2], [5]], 4, modifiers=[-5])
        self.assertEqual(result["target"], 2)
        self.assertEqual(result["successes"], 2)

    def test_open_test_takes_highest_individual_die(self):
        result = open_test([[6, 6, 3], [5], [2]])
        self.assertEqual(result["result"], 15)

    def test_contest_tie_is_unresolved(self):
        result = compare_successes({"successes": 2}, {"successes": 2})
        self.assertTrue(result["tie"])
        self.assertIsNone(result["winner"])

    def test_opposed_uses_other_participants_rating_as_target(self):
        result = opposed_test(2, [[4], [5]], 3, [[1], [1], [1]])
        self.assertEqual((result["a"]["target"], result["b"]["target"]), (3, 2))
        self.assertEqual(result["winner"], "A")

    def test_initiative_sixes_do_not_explode(self):
        result = initiative(4, [6, 6])
        self.assertEqual(result["score"], 16)
        self.assertFalse(result["exploding_sixes"])

    def test_initiative_passes_subtract_ten(self):
        result = initiative_passes({"runner": 23, "guard": 12})
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]["order_groups"][0], {"score": 13, "actors": ["runner"]})
        self.assertEqual(result[2]["order_groups"], [{"score": 3, "actors": ["runner"]}])

    def test_initiative_tie_not_arbitrarily_decided(self):
        result = initiative_passes({"zen": 14, "ace": 14})
        self.assertEqual(result[0]["order_groups"][0]["actors"], ["ace", "zen"])
        self.assertTrue(result[0]["tie_breaks_unresolved"])

    def test_missing_followup_roll_rejected(self):
        with self.assertRaises(ValueError):
            success_test([[6]], 7)
        with self.assertRaises(ValueError):
            open_test([[6]])

    def test_illegal_extra_roll_rejected(self):
        with self.assertRaises(ValueError):
            success_test([[5, 4]], 5)

    def test_zero_dice_not_silently_resolved(self):
        with self.assertRaises(ValueError):
            success_test([], 4)


if __name__ == "__main__":
    unittest.main()
