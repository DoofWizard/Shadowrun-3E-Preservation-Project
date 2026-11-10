"""Source-grounded Companion vectors; narrow code-tested portion only."""
import unittest
from fractions import Fraction
from companion_probe import (
    RULE_IDS, UnresolvedRule, ghoul_exposure_outcome, ghoul_stage3_modifiers,
    ghoul_starting_build_point_surcharge, climbing_target_number,
    escape_artist_timing, fall_profile_for_even_meters, fatigue_period_turns,
    fatigue_power_for_period, effective_running_quickness,
    normal_swimming_distance, breath_hold_turns,
)


class CompanionVectors(unittest.TestCase):
    def test_provenance_ids(self):
        self.assertEqual(RULE_IDS["ghoul_infection"], "rule.character-creation.srcomp-ghoul-krieger-infection")

    def test_infection_zero(self):
        self.assertEqual(ghoul_exposure_outcome(0), "infected")

    def test_infection_one_gm(self):
        self.assertEqual(ghoul_exposure_outcome(1), "permanent-effect-at-gm-discretion")

    def test_infection_three_plus_carrier_possible(self):
        self.assertEqual(ghoul_exposure_outcome(8), "no-effect-carrier-possible")

    def test_stage_three_zero(self):
        self.assertEqual(ghoul_stage3_modifiers(0), {"intelligence": -2, "charisma": -2})

    def test_stage_three_one_two(self):
        self.assertEqual(ghoul_stage3_modifiers(1), {"intelligence": -1, "charisma": -1})
        self.assertEqual(ghoul_stage3_modifiers(2), {"charisma": -1})

    def test_stage_three_three_and_four(self):
        self.assertEqual(ghoul_stage3_modifiers(3), {})
        self.assertEqual(ghoul_stage3_modifiers(4), {"willpower": 1})

    def test_build_points_not_race_cost(self):
        self.assertEqual(ghoul_starting_build_point_surcharge(), 10)

    def test_climbing_surface_height_wet(self):
        self.assertEqual(climbing_target_number("flat", "2_to_4m", "wet"), 12)

    def test_climbing_sheer_greased(self):
        self.assertEqual(climbing_target_number("sheer", "above_4m", "greased"), 22)

    def test_escape_handcuffs_time(self):
        self.assertEqual(escape_artist_timing("handcuffs", 2), (Fraction(15), 30))

    def test_escape_fraction_no_invented_rounding(self):
        self.assertEqual(escape_artist_timing("ropes", 3)[0], Fraction(20, 3))

    def test_escape_failure_wait(self):
        self.assertEqual(escape_artist_timing("ropes", 0), (None, 20))

    def test_fall_even_no_armor(self):
        self.assertEqual(fall_profile_for_even_meters(4, 0), (2, "M"))

    def test_fall_even_armor_successes(self):
        self.assertEqual(fall_profile_for_even_meters(20, 3, 1), (8, "S"))

    def test_odd_meter_power_refused(self):
        with self.assertRaises(UnresolvedRule):
            fall_profile_for_even_meters(3, 2)

    def test_sprint_fatigue(self):
        self.assertEqual(fatigue_period_turns(5), 3)
        self.assertEqual(fatigue_power_for_period(1), 4)
        self.assertEqual(fatigue_power_for_period(2), 8)

    def test_phase_running_and_swim(self):
        self.assertEqual(effective_running_quickness(4, 3), 7)
        self.assertEqual(normal_swimming_distance(30), Fraction(6))

    def test_swim_fraction_no_invented_rounding(self):
        self.assertEqual(normal_swimming_distance(27), Fraction(27, 5))

    def test_hold_breath(self):
        self.assertEqual(breath_hold_turns(2), 21)

    def test_wrong_inputs_rejected(self):
        with self.assertRaises(ValueError):
            ghoul_exposure_outcome(-1)
        with self.assertRaises(ValueError):
            climbing_target_number("missing", "under_2m")
        with self.assertRaises(ValueError):
            fatigue_period_turns(0)


if __name__ == "__main__":
    unittest.main()
