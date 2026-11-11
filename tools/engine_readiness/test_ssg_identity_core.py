"""Canonical-data-driven source-linked *consumer* tests: FanPro10667 pp125-127.

These verify a bounded mechanical adapter, not semantic ingestion or a working
Matrix system. The accepted canonical YAML must be present at repository root.
"""
import unittest
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import yaml
from ssg_identity_core import (UnresolvedSSGIdentity, id_creation_game_test,
    id_random_edge_or_flaw, id_price_with_optional_traits, home_turf_rating,
    limitation_rating, id_expiration_months, deterioration_interval)

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "rules/identity/ssg-fictional-id-creation-options-p125-127.yml"

class SSGIdentityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = yaml.safe_load(PATH.read_text(encoding="utf-8"))

    def test_original_source_example(self):
        x = id_creation_game_test(self.record,4,3,2)
        self.assertEqual(x, {"target_number":9,"adjusted_base_days":50,"nuyen_cost":1600,
            "contact_deficit":1,"test_succeeded":True,"elapsed_days":Fraction(25)})

    def test_no_contact_deficit(self):
        x = id_creation_game_test(self.record,3,3)
        self.assertEqual((x["target_number"],x["adjusted_base_days"],x["nuyen_cost"]),(6,30,900))

    def test_surplus_contacts_do_not_reduce_base_target(self):
        self.assertEqual(id_creation_game_test(self.record,2,9)["target_number"],4)

    def test_zero_success_consumes_half_adjusted_time(self):
        x=id_creation_game_test(self.record,4,3,0)
        self.assertFalse(x["test_succeeded"])
        self.assertEqual(x["elapsed_days"],25)

    def test_nondivisible_time_retained_exactly(self):
        self.assertEqual(id_creation_game_test(self.record,2,2,3)["elapsed_days"],Fraction(20,3))

    def test_rating_and_contacts_validation(self):
        for args in [(0,0),(True,0),(-1,2),(2,-1),(2,False)]:
            with self.subTest(args=args),self.assertRaises(UnresolvedSSGIdentity):
                id_creation_game_test(self.record,*args)

    def test_success_count_validation(self):
        for count in [1.5,True,-1]:
            with self.subTest(count=count),self.assertRaises(UnresolvedSSGIdentity):
                id_creation_game_test(self.record,4,3,count)

    def test_optional_d6_traits(self):
        self.assertEqual(id_random_edge_or_flaw(self.record,1),"flaw")
        self.assertEqual(id_random_edge_or_flaw(self.record,6),"edge")
        for i in range(2,6): self.assertIsNone(id_random_edge_or_flaw(self.record,i))

    def test_d6_validation(self):
        for bad in [0,7,True,1.5]:
            with self.subTest(bad=bad),self.assertRaises(UnresolvedSSGIdentity):
                id_random_edge_or_flaw(self.record,bad)

    def test_price_adjustments_additive(self):
        x=id_price_with_optional_traits(self.record,1000,edges=2,flaws=1)
        self.assertEqual(x["nuyen"],1200)
        self.assertFalse(x["recommended_trait_count_exceeded"])

    def test_price_fraction_not_inferred_rounding(self):
        self.assertEqual(id_price_with_optional_traits(self.record,101,edges=1)["nuyen"],Fraction(606,5))

    def test_three_trait_limit_is_recommendation(self):
        self.assertTrue(id_price_with_optional_traits(self.record,1000,edges=4)["recommended_trait_count_exceeded"])

    def test_disallow_negative_cost_not_defined_by_source(self):
        with self.assertRaises(UnresolvedSSGIdentity):
            id_price_with_optional_traits(self.record,1000,flaws=6)

    def test_home_turf_round_up_only_in_selected_area(self):
        self.assertEqual(home_turf_rating(self.record,3,True),5)
        self.assertEqual(home_turf_rating(self.record,3,False),3)

    def test_limitation_round_down_and_rating_one_failure(self):
        self.assertEqual(limitation_rating(self.record,3,True),{"automatic_failure":False,"effective_rating":1})
        self.assertEqual(limitation_rating(self.record,1,True),{"automatic_failure":True,"effective_rating":None})
        self.assertEqual(limitation_rating(self.record,1,False),{"automatic_failure":False,"effective_rating":1})

    def test_jurisdiction_type_not_guessed(self):
        for x in [0,1,None,"yes"]:
            with self.subTest(x=x),self.assertRaises(UnresolvedSSGIdentity):
                home_turf_rating(self.record,2,x)

    def test_expiration_game_die(self):
        self.assertEqual(id_expiration_months(self.record,3,4),12)
        self.assertEqual(id_expiration_months(self.record,3,6),18)

    def test_unclear_deterioration_interval_untouched(self):
        with self.assertRaises(UnresolvedSSGIdentity): deterioration_interval(self.record)

    def test_reject_wrong_canonical_id(self):
        r=deepcopy(self.record);r["id"]="fabricated"
        with self.assertRaises(UnresolvedSSGIdentity): id_creation_game_test(r,4,3)

    def test_reject_wrong_publisher_edition(self):
        r=deepcopy(self.record);r["data"]["publication"]["catalog_number"]="FASA7001"
        with self.assertRaises(UnresolvedSSGIdentity): id_creation_game_test(r,4,3)

    def test_refuse_modified_canonical_formula(self):
        r=deepcopy(self.record)
        r["data"]["optional_id_rating_creation_game_test"]["base_time_days_formula"]="made up"
        with self.assertRaises(UnresolvedSSGIdentity): id_creation_game_test(r,4,3)

if __name__=='__main__': unittest.main()
