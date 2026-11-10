"""Boundary and integration tests of original SR3 FASA7001 p111/PDF112."""
import unittest
from rules_probe import UnresolvedRule, success_test
from core_extensions import ranged_outcome
from condition_core import ConditionMonitor
from weapon_range_core import resolve_weapon_range, RANGE_LIMITS_M


class OriginalSR3WeaponRangeTests(unittest.TestCase):
    def test_all_included_rows_have_monotonic_four_ranges(self):
        self.assertEqual(len(RANGE_LIMITS_M),13)
        for name, limits in RANGE_LIMITS_M.items():
            with self.subTest(name=name):
                self.assertEqual(len(limits),4)
                self.assertEqual(tuple(sorted(set(limits))),limits)
                self.assertTrue(all(type(x) is int and x>=0 for x in limits))
    def test_light_pistol_exact_tn_cutoffs(self):
        self.assertEqual([(resolve_weapon_range("light_pistol",d).category,resolve_weapon_range("light_pistol",d).base_target_number)
                          for d in (5,6,15,16,30,31,50)],
                         [("short",4),("medium",5),("medium",5),("long",6),("long",6),("extreme",9),("extreme",9)])
    def test_light_pistol_beyond_extreme_is_not_a_roll(self):
        x=resolve_weapon_range("light_pistol",51)
        self.assertEqual((x.in_range,x.category,x.base_target_number),(False,"beyond_extreme",None))
    def test_zero_distance_in_short_band(self):
        self.assertEqual(resolve_weapon_range("hold_out_pistol",0).base_target_number,4)
    def test_smg_short_medium_cutoff(self):
        self.assertEqual(resolve_weapon_range("smg",10).category,"short")
        self.assertEqual(resolve_weapon_range("smg",11).category,"medium")
    def test_heavy_pistol_end_of_long(self):
        self.assertEqual(resolve_weapon_range("heavy_pistol",40).base_target_number,6)
        self.assertEqual(resolve_weapon_range("heavy_pistol",41).base_target_number,9)
    def test_taser_extreme_short_max(self):
        self.assertEqual(resolve_weapon_range("taser",15).base_target_number,9)
        self.assertFalse(resolve_weapon_range("taser",16).in_range)
    def test_shotgun_rifle_not_used_as_source_range_class(self):
        with self.assertRaises(UnresolvedRule):resolve_weapon_range("shotgun_pistol",10)
    def test_sniper_rifle_max_1000(self):
        self.assertEqual(resolve_weapon_range("sniper_rifle",1000).category,"extreme")
        self.assertFalse(resolve_weapon_range("sniper_rifle",1001).in_range)
    def test_assault_cannon_extreme_limit(self):
        self.assertEqual(resolve_weapon_range("assault_cannon",2400).base_target_number,9)
    def test_grenade_launcher_requires_minimum_range_logic(self):
        with self.assertRaises(UnresolvedRule):resolve_weapon_range("grenade_launcher",10)
    def test_unknown_generic_rifle_not_inferred(self):
        with self.assertRaises(UnresolvedRule):resolve_weapon_range("rifle",30)
    def test_noninteger_distance_fails_closed(self):
        with self.assertRaises(ValueError):resolve_weapon_range("smg",10.5)
        with self.assertRaises(ValueError):resolve_weapon_range("smg",True)
        with self.assertRaises(ValueError):resolve_weapon_range("smg",-1)
    def test_cross_system_attack_to_condition_monitor(self):
        """Source-linked test, NOT full attack: caller supplies dice, Body TN."""
        x=resolve_weapon_range("light_pistol",10)  # p111 medium => TN5
        attack=success_test([[5],[5],[1]],x.base_target_number).successes
        dodge=success_test([[4],[1]],4).successes
        resist=success_test([[2],[1]],5).successes
        result=ranged_outcome(attack,dodge,resist,"M")
        self.assertEqual((attack,dodge,resist,result.damage_level),(2,1,0,"M"))
        self.assertEqual(ConditionMonitor(body=4).apply(result.damage_level,"Physical").physical,3)
