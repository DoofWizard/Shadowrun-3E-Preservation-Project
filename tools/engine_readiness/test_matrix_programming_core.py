"""Independent bounded numeric vectors from FASA Matrix FASA7909 SR3 pp76,78-80.

Source p77/PDF78 is artwork, not a missing programming-rule page. Existing
canonical records are archival authorities; these tests are consumer checks.
"""
import unittest
from matrix_programming_core import (
    program_size_mp, programming_suite_size_mp, programming_plan,
    required_programming_memory_mp, programming_test_tn,
    programming_days, failed_program_days, plan_team,
    UnresolvedProgrammingRule,
)


class MatrixProgrammingNumericTests(unittest.TestCase):
    def test_program_size_source_example_6_by_4(self):
        self.assertEqual(program_size_mp(6, 4), 144)

    def test_program_size_printed_table_limits(self):
        self.assertEqual(program_size_mp(14, 10), 1960)
        self.assertEqual(program_size_mp(1, 1), 1)

    def test_program_size_refuses_outside_table(self):
        for value in [0, 15, True, 1.2]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                program_size_mp(value, 4)

    def test_suite_sizes_source_examples(self):
        self.assertEqual(programming_suite_size_mp(1), 15)
        self.assertEqual(programming_suite_size_mp(5), 375)
        self.assertEqual(programming_suite_size_mp(10), 1500)

    def test_suite_outside_table_fails(self):
        with self.assertRaises(ValueError): programming_suite_size_mp(11)

    def test_source_plan_hours_and_mp(self):
        plan = programming_plan(6, 1, 4, 256)
        self.assertEqual((plan.design_tn_before_global_minimum,
                          plan.preparation_hours, plan.preparation_memory_mp),
                         (5, 28, 25))

    def test_plan_rating_bands_and_option_modifiers(self):
        self.assertEqual(programming_plan(4, 0, 3, 48).design_tn_before_global_minimum, 3)
        self.assertEqual(programming_plan(9, 0, 3, 243).design_tn_before_global_minimum, 4)
        self.assertEqual(programming_plan(10, 2, 3, 300).design_tn_before_global_minimum, 7)

    def test_plan_minute_memory_floor(self):
        self.assertEqual(programming_plan(1, 0, 1, 9).preparation_memory_mp, 0)

    def test_plan_negative_options_refused(self):
        with self.assertRaises(ValueError): programming_plan(6, -1, 4, 256)

    def test_memory_two_independent_requirements(self):
        self.assertEqual(required_programming_memory_mp(256), (256, 256))

    def test_no_plan_penalty(self):
        self.assertEqual(programming_test_tn(6), 8)

    def test_source_example_rating6_plan3_double_memory(self):
        self.assertEqual(programming_test_tn(6, plan_successes=3, double_memory=True), 2)

    def test_plan_zero_success_does_not_mean_absent_plan(self):
        self.assertEqual(programming_test_tn(6, plan_successes=0), 6)
        self.assertEqual(programming_test_tn(6, plan_successes=None), 8)

    def test_security_color_modifiers(self):
        self.assertEqual(programming_test_tn(12, plan_successes=1, mainframe_color="blue"), 10)
        self.assertEqual(programming_test_tn(12, plan_successes=1, mainframe_color="green"), 9)
        self.assertEqual(programming_test_tn(12, plan_successes=1, mainframe_color="orange"), 8)
        self.assertEqual(programming_test_tn(12, plan_successes=1, mainframe_color="red"), 7)

    def test_tn_minimum_two(self):
        self.assertEqual(programming_test_tn(1, plan_successes=10, double_memory=True), 2)

    def test_unknown_color_fails(self):
        with self.assertRaises(ValueError): programming_test_tn(6, mainframe_color="magenta")

    def test_source_task_period(self):
        self.assertEqual(programming_days(256, 8), 32)
        self.assertEqual(programming_days(256, 7), 37)

    def test_failed_program_requires_gm_roll(self):
        with self.assertRaises(UnresolvedProgrammingRule): programming_days(256, 0)

    def test_gm_failed_days_2d6(self):
        self.assertEqual(failed_program_days(256, 7), 37)
        with self.assertRaises(ValueError): failed_program_days(256, 13)

    def test_original_four_member_team(self):
        result = plan_team(8, (5, 2, 8, 7), 32)
        self.assertEqual(result, {"maximum_members": 4, "maximum_program_rating": 8,
                                  "test_skill_dice_before_task_pool": 5,
                                  "minimum_days_each_member": 7})

    def test_team_size_over_limit_fails(self):
        with self.assertRaises(ValueError): plan_team(8, (5, 2, 8, 7, 2), 32)

    def test_team_max_rating_fails(self):
        with self.assertRaises(ValueError): plan_team(9, (5, 2, 8, 7), 32)

    def test_non_integer_members_refused(self):
        with self.assertRaises(ValueError): plan_team(8, (5, 2, 8, True), 32)

    def test_outside_sourced_mechanics_not_implemented(self):
        self.assertFalse(hasattr(__import__('matrix_programming_core'), 'run_intrusion'))


if __name__ == '__main__':
    unittest.main()
