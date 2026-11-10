"""Executed consumer vectors for published FASA7001 p307/PDF316 (not R3)."""
import unittest
from rules_probe import UnresolvedRule
from vehicle_mounts_core import (
    mount_capacity, mounting_allowed, mount_installation, fixed_mount_sidefire,
    halved_fixed_mount_recoil, mount_signature_delta, turret_cargo_change,
    aircraft_external_missile_mounts,
)


class SourceReviewedOriginalSR3VehicleMounts(unittest.TestCase):
    def test_body_four_two_hardpoints(self):
        x=mount_capacity(4,["fixed_hardpoint","fixed_hardpoint"])
        self.assertEqual((x.used,x.remaining,x.legal),(4,0,True))
    def test_body_four_one_hard_two_firm(self):
        self.assertTrue(mount_capacity(4,["fixed_hardpoint","pintle","fixed_firmpoint"]).legal)
    def test_body_four_four_firm(self):
        self.assertTrue(mount_capacity(4,["pintle"]*4).legal)
    def test_excess_capacity_is_explicit_not_silently_clipped(self):
        x=mount_capacity(4,["fixed_hardpoint","fixed_hardpoint","pintle"])
        self.assertEqual((x.used,x.remaining,x.legal),(5,-1,False))
    def test_turret_uses_two_hardpoints(self):
        self.assertEqual(mount_capacity(4,["turret"]).used,4)
    def test_mini_turret_uses_one_hardpoint(self):
        self.assertEqual(mount_capacity(2,["mini_turret"]).used,2)
    def test_negative_body_and_bool_rejected(self):
        for val in [-1,True,3.5]:
            with self.subTest(val=val),self.assertRaises(ValueError):mount_capacity(val,[])
    def test_unknown_mount_and_string_sequence_fail_closed(self):
        with self.assertRaises(UnresolvedRule):mount_capacity(4,["ring_mount"])
        with self.assertRaises(ValueError):mount_capacity(4,"turret")
    def test_small_weapon_firmpoint_vs_heavy(self):
        self.assertTrue(mounting_allowed("fixed_firmpoint","small"))
        self.assertFalse(mounting_allowed("fixed_firmpoint","mmg"))
    def test_mini_turret_mmg_limit(self):
        self.assertTrue(mounting_allowed("mini_turret","mmg"))
        self.assertFalse(mounting_allowed("mini_turret","larger_than_mmg"))
    def test_full_hardpoint_carries_mmg_or_larger(self):
        self.assertTrue(mounting_allowed("fixed_hardpoint","larger_than_mmg"))
    def test_unresolved_weapon_size_must_be_source_classified(self):
        with self.assertRaises(UnresolvedRule):mounting_allowed("turret","heavy rifle")
    def test_fixed_mount_installation(self):
        x=mount_installation("fixed_hardpoint")
        self.assertEqual((x.test,x.target_number,x.base_hours),("Vehicle B/R",4,24))
    def test_pintle_installation(self):
        self.assertEqual((mount_installation("pintle").target_number,mount_installation("pintle").base_hours),(2,12))
    def test_turret_installation(self):
        self.assertEqual((mount_installation("turret").target_number,mount_installation("turret").base_hours),(4,72))
    def test_side_firing_fixed_mount_forces_crash_test(self):
        self.assertEqual(fixed_mount_sidefire(3,2).updated_handling,5)
        self.assertTrue(fixed_mount_sidefire(3,2).requires_crash_test)
    def test_half_recoil_even_is_exact(self):
        self.assertEqual(halved_fixed_mount_recoil(6),3)
    def test_half_recoil_odd_fails_closed(self):
        with self.assertRaises(UnresolvedRule):halved_fixed_mount_recoil(5)
    def test_turret_signature_and_cargo_change(self):
        self.assertEqual(mount_signature_delta("turret"),-1)
        self.assertEqual(turret_cargo_change("turret"),2)
        self.assertEqual(turret_cargo_change("mini_turret"),1)
    def test_fixed_external_signature_only_when_explicitly_outside(self):
        self.assertEqual(mount_signature_delta("fixed_hardpoint",external=True),-1)
        with self.assertRaises(UnresolvedRule):mount_signature_delta("fixed_hardpoint")
        with self.assertRaises(UnresolvedRule):mount_signature_delta("fixed_firmpoint",external=False)
    def test_pintle_signature_not_specified_fails_closed(self):
        with self.assertRaises(UnresolvedRule):mount_signature_delta("pintle")
    def test_aircraft_body_three_three_300kg_mounts(self):
        x=aircraft_external_missile_mounts(3,[300,300,300])
        self.assertEqual((x.legal,x.total_weight_kg,x.counts_against_body_mount_points),(True,900,False))
    def test_aircraft_too_many_mounts_is_illegal(self):
        self.assertFalse(aircraft_external_missile_mounts(2,[50,50,50]).legal)
    def test_aircraft_over_300kg_one_mount_illegal(self):
        self.assertFalse(aircraft_external_missile_mounts(3,[301]).legal)
    def test_aircraft_invalid_weights_rejected(self):
        with self.assertRaises(ValueError):aircraft_external_missile_mounts(2,[False,300])
