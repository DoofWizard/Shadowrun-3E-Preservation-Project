"""Consumer tests from FanPro Sprawl Survival Guide, SR3, pp122-123/PDF123-124.

Tests load accepted canonical YAML, not a manually reconstructed data fixture.
"""
import unittest
from pathlib import Path
import yaml
from ssg_market_core import (UnresolvedSSGRule, household_drone_market,
    household_fleet_cost_nuyen, electronic_paper_sheet_nuyen,
    colorchange_paint_quote_nuyen, paint_market_availability)

ROOT = Path(__file__).resolve().parents[2]

def source_record(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))

class SSGMarketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.drones = source_record("equipment/ssg-household-drone-market-p122.yml")
        cls.paper = source_record("equipment/ssg-electronic-paper-colorchange-p123.yml")
        cls.market = household_drone_market(cls.drones)

    def test_eleven_distinct_source_models(self):
        self.assertEqual(len(self.market), 11)
    def test_synthcat_price(self):
        self.assertEqual(self.market["Ares Felix the SynthCat"]["market"]["price_nuyen"], 9500)
    def test_butlerbot_pilot_notation_not_rounded(self):
        self.assertEqual(self.market["Mitsuhama Butlerbot"]["stats"]["pilot"], "2 (4)")
    def test_distinct_mr_bright_variants(self):
        self.assertEqual(self.market["IFMU Mr. Bright 3000"]["market"]["price_nuyen"], 6500)
        self.assertEqual(self.market["Household model"]["market"]["price_nuyen"], 6000)
    def test_availability_keeps_hours(self):
        self.assertEqual(self.market["Renraku Barback"]["market"]["availability"], "3/72 hrs")
    def test_em_dash_not_assumed_zero(self):
        self.assertEqual(self.market["Ares Felix the SynthCat"]["stats"]["acceleration"], "—")
    def test_fleet_price(self):
        self.assertEqual(household_fleet_cost_nuyen(self.drones, ["V.R. House Helper", "Ares Felix the SynthCat"]), 11000)
    def test_unknown_variant_refused(self):
        with self.assertRaises(UnresolvedSSGRule): household_fleet_cost_nuyen(self.drones, ["imaginary variant"])
    def test_misaligned_row_refused(self):
        from copy import deepcopy
        bad = deepcopy(self.drones)
        bad["data"]["vehicle_rows"][0][0] = "other model"
        with self.assertRaises(UnresolvedSSGRule): household_drone_market(bad)
    def test_wrong_source_id_refused(self):
        from copy import deepcopy
        bad = deepcopy(self.drones)
        bad["source"] = "source.fasa-7910"
        with self.assertRaises(UnresolvedSSGRule): household_drone_market(bad)
    def test_paper_form_prices(self):
        self.assertEqual(electronic_paper_sheet_nuyen(self.paper, "standard"), 2)
        self.assertEqual(electronic_paper_sheet_nuyen(self.paper, "tabloid"), 5)
    def test_paper_unlisted_form_refused(self):
        with self.assertRaises(UnresolvedSSGRule): electronic_paper_sheet_nuyen(self.paper, "custom")
    def test_paint_price_controller_separately(self):
        self.assertEqual(colorchange_paint_quote_nuyen(self.paper, 3), 225)
        self.assertEqual(colorchange_paint_quote_nuyen(self.paper, 3, True), 2225)
    def test_paint_fraction_rounding_unspecified(self):
        for area in [1.5, 0, True, -1]:
            with self.subTest(area=area), self.assertRaises(UnresolvedSSGRule): colorchange_paint_quote_nuyen(self.paper, area)
    def test_source_paint_columns_unresolved(self):
        with self.assertRaises(UnresolvedSSGRule): paint_market_availability(self.paper)

if __name__ == "__main__": unittest.main()
