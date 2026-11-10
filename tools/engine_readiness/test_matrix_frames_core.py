"""FASA Corporation Matrix FASA7909 SR3 source tests pp89-90/PDF90-91."""
import unittest
from matrix_frames_core import design_frame, maximum_frame_core, utility_reload_cost, UndefinedFrameRule

class FrameDesignRules(unittest.TestCase):
    def test_original_skill8_limits(self):
        self.assertEqual([maximum_frame_core(8, kind) for kind in ("dumb_frame", "smart_frame", "agent")], [16, 12, 8])
    def test_original_agent8_budget(self):
        b = design_frame(8, "agent", 8, persona_bod=4, persona_evasion=4,
                         persona_masking=5, persona_sensor=3, pilot=8,
                         extra_initiative_dice=4, utility_payload=20)
        self.assertEqual((b.core_size_mp, b.persona_points_available, b.frame_points_available,
                          b.spent_frame_points, b.unspent_frame_points_lost, b.hacking_pool,
                          b.total_initiative_dice), (640, 16, 48, 48, 0, 8, 5))
    def test_frame_core_size_multipliers(self):
        self.assertEqual(design_frame(4, "dumb_frame", 4).core_size_mp, 48)
        self.assertEqual(design_frame(4, "smart_frame", 4, pilot=1).core_size_mp, 96)
        self.assertEqual(design_frame(4, "agent", 4, pilot=1).core_size_mp, 160)
    def test_smart_initiative_cap(self):
        self.assertEqual(design_frame(8, "smart_frame", 8, pilot=1, extra_initiative_dice=3).total_initiative_dice, 4)
        with self.assertRaises(UndefinedFrameRule): design_frame(8, "smart_frame", 8, pilot=1, extra_initiative_dice=4)
    def test_dumb_reuses_controller_initiative(self):
        b=design_frame(4,"dumb_frame",4)
        self.assertIsNone(b.total_initiative_dice)
        self.assertEqual(b.hacking_pool,0)
    def test_dumb_rejects_pilot(self):
        with self.assertRaises(UndefinedFrameRule): design_frame(4,"dumb_frame",4,pilot=1)
    def test_smart_requires_pilot(self):
        with self.assertRaises(UndefinedFrameRule): design_frame(8,"smart_frame",8)
    def test_agent_cannot_exceed_skill(self):
        with self.assertRaises(UndefinedFrameRule): design_frame(8,"agent",9,pilot=1)
    def test_programmer_limits_pilot(self):
        with self.assertRaises(UndefinedFrameRule): design_frame(4,"smart_frame",6,pilot=5)
    def test_persona_max_attribute_and_budget(self):
        with self.assertRaises(UndefinedFrameRule): design_frame(8,"agent",8,pilot=1,persona_bod=9)
        with self.assertRaises(UndefinedFrameRule): design_frame(8,"smart_frame",8,pilot=1,persona_bod=8,persona_sensor=8)
    def test_frame_points_not_infinite(self):
        with self.assertRaises(UndefinedFrameRule): design_frame(4,"agent",4,pilot=4,extra_initiative_dice=4,utility_payload=5)
    def test_unused_points_expire(self):
        self.assertEqual(design_frame(4,"smart_frame",4,pilot=1).unspent_frame_points_lost,14)
    def test_reload_source_example(self):
        self.assertEqual(utility_reload_cost([5,5,5]),{"computer_programming_test_tn":5,"base_time_days":50})
    def test_reload_round_up_tn_and_time(self):
        self.assertEqual(utility_reload_cost([5,6]),{"computer_programming_test_tn":6,"base_time_days":72})
    def test_reload_reject_unknown(self):
        with self.assertRaises(UndefinedFrameRule): utility_reload_cost([])
    def test_frame_unknown_kind(self):
        with self.assertRaises(UndefinedFrameRule): design_frame(4,"AI",4)

if __name__ == "__main__": unittest.main()
