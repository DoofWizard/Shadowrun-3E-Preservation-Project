"""Small source-grounded SR3 kernel integration traces; not a complete encounter."""
import unittest
from rules_probe import success_test, initiative_total
from core_extensions import starting_character_budget, ranged_outcome
from condition_core import ConditionMonitor


class CoreKernelIntegration(unittest.TestCase):
    def test_character_to_hit_to_condition_state(self):
        priorities = dict(Race="E", Magic="D", Attributes="A", Skills="B", Resources="C")
        budget = starting_character_budget(priorities, "human", "mundane")
        self.assertEqual((budget["attribute_points"],budget["skill_points"],budget["nuyen"]),
                         (30,40,90000))  # FASA7001 p54
        attack = success_test([[5],[1],[6]],4).successes  # p38 / p113
        dodge = success_test([[4],[1]],4).successes    # p113
        resist = success_test([[5],[2],[1],[1]],5).successes  # chosen fixture TN5
        result = ranged_outcome(attack,dodge,resist,"M")
        self.assertEqual((result.result,result.damage_level),("hit","M"))
        wound = ConditionMonitor(body=5).apply(result.damage_level,"Physical")
        self.assertEqual((wound.physical,wound.modifiers()),(3,(2,-2))) # pp125-126
        self.assertEqual(initiative_total(6,[5]),11)  # baseline no wound p42

    def test_complete_dodge_never_updates_condition_monitor(self):
        old = ConditionMonitor(body=4,physical=1)
        result = ranged_outcome(1,2,0,"S")
        self.assertEqual(result.result,"dodged")
        new = old if result.damage_level=="none" else old.apply(result.damage_level,"Physical")
        self.assertEqual(new,old)

    def test_stun_overflow_adds_physical_before_body_death_check(self):
        old = ConditionMonitor(body=2,physical=9,stun=9)
        new = old.apply("S","Stun")
        self.assertEqual((new.physical,new.stun,new.physical_overflow),(14,10,4))
        self.assertTrue(new.dead)

    def test_baseline_damage_and_advanced_extensions_stay_separate(self):
        old = ConditionMonitor(body=3)
        self.assertEqual(old.apply("D","Physical").physical,10)
        # FASA7001 default incapacitation; optional M&M p131 rescue not simulated.
        self.assertTrue(old.apply("D","Physical").incapacitated)
