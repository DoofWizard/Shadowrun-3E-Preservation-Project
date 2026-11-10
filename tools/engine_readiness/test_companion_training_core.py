"""FASA7905a printed pp49-51/PDF50-52 numerical regression vectors."""
import unittest
from fractions import Fraction
from companion_training_core import (UnresolvedTrainingRule, skill_base_days,
    training_days, attribute_training_days, interruption_remaining_days,
    baseline_daily_hours, effective_daily_hours, calendar_days,
    instructor_base_fee, subject_rating_fee_factor, instructor_daily_fee)

class SourceTrainingVectors(unittest.TestCase):
    def test_active_time(self): self.assertEqual(skill_base_days(6,"active"),42)
    def test_attribute_example(self): self.assertEqual(attribute_training_days(21,2,2),49)
    def test_calendar_days(self): self.assertEqual(calendar_days(14,8),7)
    def test_effective_hours(self): self.assertEqual(effective_daily_hours(6,3,1),8)
    def test_effective_hours_zero(self): self.assertEqual(effective_daily_hours(6,3,0),7)
    def test_fail_closed_stacking(self):
        with self.assertRaises(UnresolvedTrainingRule):
            instructor_daily_fee(4,4,classroom=True,specialization=True)
    def test_fee_options(self):
        self.assertEqual(instructor_daily_fee(4,4),100)
        self.assertEqual(instructor_daily_fee(4,4,specialization=True),150)
        self.assertEqual(instructor_daily_fee(4,4,classroom=True),50)
        self.assertEqual(instructor_daily_fee(4,4,longer_than_four_hours=True),150)
    def test_fee_table(self):
        self.assertEqual([instructor_base_fee(i) for i in range(1,9)], [40,50,75,100,200,400,500,600])
    def test_half_wp_ceiling(self): self.assertEqual(baseline_daily_hours(6),7)
    def test_invalid(self):
        for action in (lambda: skill_base_days(3,'magic'),lambda: training_days(5,-1),
                       lambda: calendar_days(5,25),lambda: instructor_base_fee(0),
                       lambda: effective_daily_hours(6,18,10),lambda: skill_base_days(True,'active')):
            with self.assertRaises(ValueError): action()
    def test_knowledge_time(self): self.assertEqual(skill_base_days(3,"knowledge"),45)
    def test_language_time(self): self.assertEqual(skill_base_days(2,"language"),30)
    def test_no_interruption(self): self.assertEqual(interruption_remaining_days(5,5,3,7),5)
    def test_odd_teacher_hits(self): self.assertEqual(training_days(42,2,1),21)
    def test_source_interruption(self): self.assertEqual(interruption_remaining_days(5,5,3,8),10)
    def test_source_knowledge_example(self): self.assertEqual(training_days(45,2),23)
    def test_source_teacher_example(self): self.assertEqual(training_days(42,2,2),14)
    def test_subject_factors(self):
        self.assertEqual([subject_rating_fee_factor(i) for i in (2,4,6,8)],
                         [Fraction(3,4),Fraction(1),Fraction(5,4),Fraction(3,2)])
    def test_zero_successes(self): self.assertEqual(training_days(7,0),11)

if __name__=='__main__': unittest.main()
