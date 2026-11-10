"""FASA7001 original SR3 p306/PDF315 source-reviewed numerical vectors.

Only the published fictional tabletop pricing, prerequisites and table columns
are tested. No game-combat integration or archival transaction is implied.
"""
import unittest
from rigging_gear_core import (
    datajack_port, remote_control_gear, vehicle_control_gear,
    remote_control_deck, remote_control_eccm, hitcher_jacks,
    screen_display, intercom_speaker,
)


class SourceReviewedOriginalSR3RiggingMarket(unittest.TestCase):
    def test_datajack_regular_vehicle(self):
        item = datajack_port()
        self.assertEqual((item.cost_nuyen, item.cargo_factor, item.load_kg), (2500, 1, 15))
        self.assertEqual((item.availability, item.street_index, item.legality),
                         ("3/72 hrs", 1.5, "Legal"))

    def test_motorcycle_port_has_separate_source_price(self):
        self.assertEqual(datajack_port(motorcycle=True).cost_nuyen, 5000)

    def test_datajack_not_an_arbitrary_truthy_flag(self):
        with self.assertRaises(ValueError): datajack_port(motorcycle=1)

    def test_remote_control_body_four_costs_10000(self):
        item = remote_control_gear(vehicle_body=4, sensor_rating=1)
        self.assertEqual((item.cost_nuyen, item.cargo_factor, item.granted_pilot_rating),
                         (10000, 0, 1))
        self.assertEqual((item.availability, item.street_index), ("4/72 hrs", 2))

    def test_remote_control_requires_sensor_rating_one(self):
        with self.assertRaises(ValueError):
            remote_control_gear(vehicle_body=4, sensor_rating=0)

    def test_remote_control_requires_positive_integer_body(self):
        for body in (0, -2, 3.5, True):
            with self.subTest(body=body), self.assertRaises(ValueError):
                remote_control_gear(vehicle_body=body, sensor_rating=1)

    def test_vcr_adapter_requires_an_installed_interface(self):
        with self.assertRaises(ValueError):
            vehicle_control_gear(sensor_rating=1, datajack_port_installed=False,
                                 remote_control_gear_installed=False)

    def test_vcr_adapter_datajack_only(self):
        item = vehicle_control_gear(sensor_rating=1, datajack_port_installed=True,
                                    remote_control_gear_installed=False)
        self.assertEqual((item.cost_nuyen, item.cargo_factor, item.load_kg), (2500, 1, 10))
        self.assertEqual(item.availability, "4/7 days")

    def test_vcr_adapter_remote_gear_only(self):
        item = vehicle_control_gear(sensor_rating=2, datajack_port_installed=False,
                                    remote_control_gear_installed=True)
        self.assertEqual((item.cost_nuyen, item.cargo_factor), (2500, 1))

    def test_vcr_adapter_both_interfaces_not_required(self):
        item = vehicle_control_gear(sensor_rating=1, datajack_port_installed=True,
                                    remote_control_gear_installed=True)
        self.assertEqual(item.cost_nuyen, 2500)

    def test_vcr_adapter_rejects_zero_sensor(self):
        with self.assertRaises(ValueError):
            vehicle_control_gear(sensor_rating=0, datajack_port_installed=True,
                                 remote_control_gear_installed=False)

    def test_vcr_adapter_rejects_truthy_nonbooleans(self):
        with self.assertRaises(ValueError):
            vehicle_control_gear(sensor_rating=1, datajack_port_installed="yes",
                                 remote_control_gear_installed=False)

    def test_remote_control_deck_rating_three(self):
        item = remote_control_deck(3)
        self.assertEqual((item.cost_nuyen, item.weight_kg), (15000, 3.0))

    def test_remote_control_deck_rating_not_zero(self):
        with self.assertRaises(ValueError): remote_control_deck(0)

    def test_eccm_rating_1_lower_tier(self):
        item = remote_control_eccm(1)
        self.assertEqual((item.cost_nuyen, item.legality, item.weight_kg), (7500, "Legal", 1.5))

    def test_eccm_rating_3_top_of_first_tier(self):
        self.assertEqual(remote_control_eccm(3).cost_nuyen, 22500)

    def test_eccm_rating_4_start_middle_tier(self):
        item = remote_control_eccm(4)
        self.assertEqual((item.cost_nuyen, item.availability, item.legality),
                         (60000, "6/14 days", "6P–V"))

    def test_eccm_rating_5_middle_tier(self):
        self.assertEqual(remote_control_eccm(5).cost_nuyen, 75000)

    def test_eccm_rating_6_end_middle_tier(self):
        self.assertEqual(remote_control_eccm(6).cost_nuyen, 90000)

    def test_eccm_rating_7_start_upper_tier(self):
        item = remote_control_eccm(7)
        self.assertEqual((item.cost_nuyen, item.street_index, item.legality),
                         (245000, 4.0, "5P–W"))

    def test_eccm_rating_9_end_upper_tier(self):
        self.assertEqual(remote_control_eccm(9).cost_nuyen, 315000)

    def test_eccm_rating_10_exception_not_extrapolated(self):
        item = remote_control_eccm(10)
        self.assertEqual((item.cost_nuyen, item.street_index, item.legality, item.weight_kg),
                         (500000, None, "4P–W", 2.5))
        self.assertEqual(item.availability, "18/45 days")

    def test_eccm_unknown_rating_no_inferred_value(self):
        for rating in (-1, 0, 11, 3.5, True):
            with self.subTest(rating=rating), self.assertRaises(ValueError):
                remote_control_eccm(rating)

    def test_hitcher_jacks_are_per_jack(self):
        item = hitcher_jacks(rating=3, jack_count=2)
        self.assertEqual((item.cost_nuyen, item.weight_kg, item.availability),
                         (600, 0.0, "2/48 hours"))

    def test_hitcher_jack_count_positive(self):
        with self.assertRaises(ValueError): hitcher_jacks(rating=3, jack_count=0)

    def test_display_market_row(self):
        item = screen_display()
        self.assertEqual((item.cost_nuyen, item.weight_kg, item.legality),
                         (100, 0.5, "Legal"))

    def test_intercom_market_row(self):
        item = intercom_speaker()
        self.assertEqual((item.cost_nuyen, item.weight_kg), (25, 0.0))

    def test_gear_is_not_equivalent_to_included_interface(self):
        # One base datajack plus VCR adapter consumes 2 CF, 25 kg *combined*,
        # and costs 5,000 nuyen; the adapter alone does not include the jack.
        port = datajack_port()
        adapter = vehicle_control_gear(sensor_rating=1, datajack_port_installed=True,
                                       remote_control_gear_installed=False)
        self.assertEqual((port.cargo_factor + adapter.cargo_factor,
                          port.load_kg + adapter.load_kg,
                          port.cost_nuyen + adapter.cost_nuyen), (2, 25, 5000))


if __name__ == '__main__':
    unittest.main()
