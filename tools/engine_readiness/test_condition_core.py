"""SR3 FASA7001 printed pp125-126 original-page condition vectors."""
import unittest
from condition_core import ConditionMonitor, DAMAGE_BOXES, condition_level


class ConditionMonitorSourceVectors(unittest.TestCase):
    def test_original_damage_level_boxes(self):
        self.assertEqual(DAMAGE_BOXES, {"L":1,"M":3,"S":6,"D":10})

    def test_cumulative_severity_boundaries(self):
        self.assertEqual([condition_level(n) for n in (0,1,2,3,5,6,9,10)],
                         ["uninjured","L","L","M","M","S","S","D"])

    def test_moderate_plus_serious_is_nine_boxes(self):
        m = ConditionMonitor(body=5).apply("M","Physical").apply("S","Physical")
        self.assertEqual((m.physical,m.physical_level), (9,"S"))

    def test_two_different_track_penalties_add(self):
        m = ConditionMonitor(body=5).apply("M","Stun").apply("L","Physical")
        self.assertEqual(m.modifiers(), (3,-3))

    def test_serious_stun_penalty(self):
        self.assertEqual(ConditionMonitor(body=4,stun=6).modifiers(), (3,-3))

    def test_stun_overflow_to_physical(self):
        m = ConditionMonitor(body=5,stun=9).apply("M","Stun")
        self.assertEqual((m.stun,m.physical), (10,2))
        self.assertTrue(m.unconscious)

    def test_overflow_with_preexisting_physical_damage(self):
        m = ConditionMonitor(body=7,physical=3,stun=10).apply("L","Stun")
        self.assertEqual((m.physical,m.stun),(4,10))

    def test_physical_overflow_at_body_not_instantly_dead(self):
        m = ConditionMonitor(body=5,physical=15)
        self.assertEqual(m.physical_overflow,5)
        self.assertFalse(m.dead)
        self.assertTrue(m.incapacitated)

    def test_physical_overflow_past_body_is_dead(self):
        m = ConditionMonitor(body=5,physical=16)
        self.assertTrue(m.dead)

    def test_deadly_stun_precludes_action(self):
        m = ConditionMonitor(body=5).apply("D","Stun")
        self.assertIsNone(m.modifiers())

    def test_deadly_physical_precludes_action(self):
        self.assertIsNone(ConditionMonitor(body=5,physical=10).modifiers())

    def test_default_uninjured(self):
        m = ConditionMonitor(body=4)
        self.assertEqual((m.modifiers(),m.physical_level,m.stun_level),
                         ((0,0),"uninjured","uninjured"))

    def test_reject_invalid_track(self):
        with self.assertRaises(ValueError):
            ConditionMonitor(body=4).apply("M","Mental")

    def test_stun_overflow_pre_normalization_refused(self):
        with self.assertRaises(ValueError): ConditionMonitor(body=5,stun=11)
