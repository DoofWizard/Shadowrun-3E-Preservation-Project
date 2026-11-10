"""Executed original FASA7001 p279/PDF288 + p111/PDF112 vectors."""
import unittest
from rules_probe import UnresolvedRule
from firearms_ammo_core import ammunition_classes_compatible, source_range_class


class SourceReviewedSR3AmmunitionClasses(unittest.TestCase):
    def test_same_light_pistol_class(self):
        self.assertTrue(ammunition_classes_compatible("light_pistol", "light_pistol"))
    def test_hold_out_is_not_light_pistol(self):
        self.assertFalse(ammunition_classes_compatible("hold_out_pistol", "light_pistol"))
    def test_light_and_heavy_pistol_separate_classes(self):
        self.assertFalse(ammunition_classes_compatible("light_pistol", "heavy_pistol"))
    def test_shotgun_pistol_and_shotgun_rifle_share_explicit_exception(self):
        self.assertTrue(ammunition_classes_compatible("shotgun_pistol", "shotgun_rifle"))
    def test_shotgun_pistol_matches_shotgun_base_category(self):
        self.assertTrue(ammunition_classes_compatible("shotgun_pistol", "shotgun"))
    def test_shotgun_does_not_share_sporting_rifle_ammo(self):
        self.assertFalse(ammunition_classes_compatible("shotgun_rifle", "sporting_rifle"))
    def test_medium_and_heavy_machine_guns_separate_classes(self):
        self.assertFalse(ammunition_classes_compatible("medium_machine_gun", "heavy_machine_gun"))
    def test_unknown_rifle_umbrella_fails_closed(self):
        with self.assertRaises(UnresolvedRule):ammunition_classes_compatible("rifle", "rifle")
    def test_user_supplied_weapon_model_not_valid_class(self):
        with self.assertRaises(UnresolvedRule):source_range_class("Enfield AS-7")
    def test_shotgun_exception_is_normalization_not_wholesale_conversion(self):
        self.assertEqual(source_range_class("shotgun_rifle"),"shotgun")
    def test_non_string_class_rejected(self):
        with self.assertRaises(ValueError):ammunition_classes_compatible(None,"shotgun")
