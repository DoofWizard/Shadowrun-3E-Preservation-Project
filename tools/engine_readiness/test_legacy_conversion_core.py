"""Source-bounded historical FASA7001 printed pp323-325 test vectors."""
import unittest

try:
    from .legacy_conversion_core import (
        UnresolvedConversion, sr2_metahuman_karma, available_knowledge_points,
        language_read_write_rating, converted_astral_initiative,
        spell_lock_disposition, sustaining_focus_upgrade_cost,
        passenger_combat_pool_cap, vr2_ripper_mpcp_loss, vr2_alert_reset_minutes,
    )
except ImportError:
    from legacy_conversion_core import (
        UnresolvedConversion, sr2_metahuman_karma, available_knowledge_points,
        language_read_write_rating, converted_astral_initiative,
        spell_lock_disposition, sustaining_focus_upgrade_cost,
        passenger_combat_pool_cap, vr2_ripper_mpcp_loss, vr2_alert_reset_minutes,
    )


class LegacyConversionCoreTests(unittest.TestCase):
    def test_metahuman_karma(self):
        for race in ("elf", "dwarf", "ork", "troll"):
            self.assertEqual(sr2_metahuman_karma(race, 7, 10), (3, 14))
            self.assertEqual(sr2_metahuman_karma(race, 1, 0), (1, 0))

    def test_metahuman_fail_closed(self):
        for args in (("human", 7, 2), ("elf", 0, 0), ("elf", True, 3), ("elf", 2, -1)):
            with self.subTest(args=args), self.assertRaises(UnresolvedConversion):
                sr2_metahuman_karma(*args)

    def test_knowledge_point_budget(self):
        self.assertEqual(available_knowledge_points(6, [4, 3]), 23)
        self.assertEqual(available_knowledge_points(3, []), 15)
        self.assertEqual(available_knowledge_points(2, [10]), 0)
        for args in ((1, [6]), (2, [True]), (-1, []), (2, None)):
            with self.subTest(args=args), self.assertRaises(UnresolvedConversion):
                available_knowledge_points(*args)

    def test_language_read_write(self):
        for rating, expected in ((0, 0), (1, 0), (5, 2), (6, 3)):
            with self.subTest(rating=rating):
                self.assertEqual(language_read_write_rating(rating), expected)
        for rating in (-1, 2.0, True):
            with self.assertRaises(UnresolvedConversion):
                language_read_write_rating(rating)

    def test_converted_astral_initiative(self):
        self.assertEqual(converted_astral_initiative(5, 1), 26)
        self.assertEqual(converted_astral_initiative(5, 6), 31)
        for d6 in (0, 7, True, 2.5):
            with self.assertRaises(UnresolvedConversion):
                converted_astral_initiative(5, d6)

    def test_spell_locks(self):
        self.assertEqual(spell_lock_disposition(2, "force_3_focus"), {"focus_count": 2, "focus_force": 3, "nuyen": 0})
        self.assertEqual(spell_lock_disposition(2, "sell"), {"focus_count": 0, "focus_force": None, "nuyen": 90000})
        with self.assertRaises(UnresolvedConversion):
            spell_lock_disposition(1, "keep_old_lock")
        self.assertEqual(sustaining_focus_upgrade_cost(3, True), 0)
        self.assertEqual(sustaining_focus_upgrade_cost(5, True), 30000)
        self.assertEqual(sustaining_focus_upgrade_cost(6, True), 45000)
        for args in ((2, True), (7, True), (5, False)):
            with self.subTest(args=args), self.assertRaises(UnresolvedConversion):
                sustaining_focus_upgrade_cost(*args)

    def test_passenger_and_ripper(self):
        self.assertEqual(passenger_combat_pool_cap(7), 3)
        self.assertEqual(passenger_combat_pool_cap(8), 4)
        self.assertEqual(vr2_ripper_mpcp_loss(5), 2)
        self.assertEqual(vr2_ripper_mpcp_loss(6), 3)
        for fn in (passenger_combat_pool_cap, vr2_ripper_mpcp_loss):
            with self.assertRaises(UnresolvedConversion):
                fn(-1)

    def test_vr2_alert_reset(self):
        self.assertEqual(vr2_alert_reset_minutes([1, 2, 3], False), 6)
        self.assertEqual(vr2_alert_reset_minutes([6, 6, 6], False), 18)
        for args in (([1, 2], False), ([0, 2, 3], False), ([1, 2, 3], True), ([True, 2, 3], False)):
            with self.subTest(args=args), self.assertRaises(UnresolvedConversion):
                vr2_alert_reset_minutes(*args)


if __name__ == "__main__":
    unittest.main()
