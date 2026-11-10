"""Deterministic source-linked regression probes; no publication text reproduced."""
import unittest
from rules_probe import (
    RULE_IDS, UnresolvedRule, success_test, initiative_total,
    initiative_passes, opposed_result, staged_damage, reloading_options,
)


class SR3SourceVectors(unittest.TestCase):
    def test_stable_canonical_ids(self):
        self.assertIn("rule.tests", RULE_IDS["tests"])
        self.assertEqual(RULE_IDS["reloading"], "procedure.firearms.sr3-core-ammunition-reloading")

    def test_successes_are_per_die(self):
        self.assertEqual(success_test([[4], [5], [1]], 4).successes, 2)

    def test_target_floor(self):
        self.assertEqual(success_test([[2], [1]], 0).target, 2)

    def test_rule_of_one(self):
        r = success_test([[1], [1], [1]], 4)
        self.assertEqual(r.successes, 0)
        self.assertTrue(r.all_ones)

    def test_no_rule_of_one_when_not_all_ones(self):
        self.assertFalse(success_test([[1], [2]], 4).all_ones)

    def test_exploding_six_succeeds(self):
        self.assertEqual(success_test([[6, 2]], 8).successes, 1)

    def test_exploding_six_fail(self):
        self.assertEqual(success_test([[6, 1]], 8).successes, 0)

    def test_exploding_multiple_sixes(self):
        self.assertEqual(success_test([[6, 6]], 12).successes, 1)

    def test_missing_explosion_refused(self):
        with self.assertRaises(UnresolvedRule):
            success_test([[6]], 7)

    def test_initiative_no_explosion(self):
        self.assertEqual(initiative_total(5, [6, 3]), 14)

    def test_initiative_passes(self):
        self.assertEqual(initiative_passes({"A":22,"B":14,"C":6}),
                         [["A","B","C"],["A","B"],["A"]])

    def test_tied_initiative_is_not_guessed(self):
        with self.assertRaises(UnresolvedRule):
            initiative_passes({"A":14,"B":14})

    def test_standard_opposed_tie(self):
        self.assertEqual(opposed_result(2,2), "tie-no-result")

    def test_melee_tie_exception(self):
        self.assertEqual(opposed_result(2,2,melee=True), "attacker")

    def test_two_successes_stage_up(self):
        self.assertEqual(staged_damage("M",3,1), "S")

    def test_two_successes_stage_down(self):
        self.assertEqual(staged_damage("S",1,3), "M")

    def test_one_net_success_no_stage(self):
        self.assertEqual(staged_damage("M",2,1), "M")

    def test_staging_caps_at_deadly(self):
        self.assertEqual(staged_damage("D",5,1), "D")

    def test_staging_below_light_zero_damage(self):
        self.assertEqual(staged_damage("L",1,5), "none")

    def test_clip_reload(self):
        self.assertEqual(reloading_options("c",4),[("Simple","clip insert/remove"),("Complex",4)])

    def test_break_reload(self):
        self.assertEqual(reloading_options("b",4),[("Complex",2)])

    def test_belt_even_quickness(self):
        self.assertEqual(reloading_options("belt",4)[1],("Complex",2))

    def test_belt_odd_quickness_unresolved(self):
        with self.assertRaises(UnresolvedRule):
            reloading_options("belt",5)


if __name__ == "__main__":
    unittest.main()
