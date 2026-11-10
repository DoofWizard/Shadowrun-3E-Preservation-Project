"""Source-linked coverage expansion for SR3 core numerical engine adapters."""
import unittest
from rules_probe import UnresolvedRule
from core_extensions import starting_character_budget, initiative_tie_winner, ranged_outcome


class SR3CoreCoverageExpansion(unittest.TestCase):
    """Source-reviewed p54/PDF55, p102/PDF103, p113/PDF114."""

    def test_priorities_allocate_exact_numeric_budgets(self):
        p = dict(Race="C", Magic="A", Attributes="B", Skills="D", Resources="E")
        self.assertEqual(starting_character_budget(p, "troll", "full_magician"),
                         {"attribute_points": 27, "skill_points": 30, "nuyen": 5000})

    def test_priority_budget_A_values(self):
        p = dict(Race="E", Magic="D", Attributes="A", Skills="B", Resources="C")
        self.assertEqual(starting_character_budget(p, "human", "mundane"),
                         {"attribute_points": 30, "skill_points": 40, "nuyen": 90000})

    def test_priority_adept_requires_B(self):
        p = dict(Race="E", Magic="A", Attributes="B", Skills="C", Resources="D")
        with self.assertRaises(ValueError): starting_character_budget(p,"human","adept")

    def test_race_priority_exact(self):
        p = dict(Race="B", Magic="A", Attributes="C", Skills="D", Resources="E")
        with self.assertRaises(ValueError): starting_character_budget(p,"elf","full_magician")

    def test_duplicate_priority_refused(self):
        p = dict(Race="E", Magic="D", Attributes="A", Skills="A", Resources="C")
        with self.assertRaises(ValueError): starting_character_budget(p,"human","mundane")

    def test_first_pass_initiative_breaks_tie(self):
        self.assertEqual(initiative_tie_winner((23,17),(4,8),(3,7)),"A")

    def test_adjusted_reaction_breaks_tie(self):
        self.assertEqual(initiative_tie_winner((23,23),(4,8),(3,7)),"B")

    def test_natural_reaction_breaks_tie(self):
        self.assertEqual(initiative_tie_winner((23,23),(4,4),(6,3)),"A")

    def test_repeated_dice_break_tie(self):
        self.assertEqual(initiative_tie_winner((10,10),(4,4),(3,3),([2,6],[2,1])),"A")

    def test_unresolved_dice_tie_fails_closed(self):
        with self.assertRaises(UnresolvedRule):
            initiative_tie_winner((10,10),(4,4),(3,3),([2],[2]))

    def test_attack_zero_successes_misses(self):
        self.assertEqual(ranged_outcome(0,0,0,"M").result,"miss")

    def test_dodge_more_successes_avoids(self):
        self.assertEqual(ranged_outcome(2,3,0,"M").result,"dodged")

    def test_equal_dodge_not_automatic_avoidance(self):
        result = ranged_outcome(2,2,0,"M")
        self.assertEqual((result.result,result.damage_level),("hit","M"))

    def test_partial_dodge_adds_resistance_successes(self):
        result = ranged_outcome(2,1,3,"M")
        self.assertEqual((result.total_defender_successes,result.damage_level),(4,"L"))

    def test_defender_stages_below_light(self):
        result = ranged_outcome(1,1,4,"L")
        self.assertEqual((result.result,result.damage_level),("hit-no-damage","none"))

    def test_attacker_stages_deadly_cap(self):
        result = ranged_outcome(6,0,0,"D")
        self.assertEqual((result.result,result.damage_level),("hit","D"))

    def test_invalid_ranged_input_refused(self):
        with self.assertRaises(ValueError): ranged_outcome(-1,1,2,"L")
