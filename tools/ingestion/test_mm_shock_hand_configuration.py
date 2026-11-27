"""Original FASA7126 Shock Hand source-delta invariants; no book acceptance.

The legacy entity ID collision is *not* silently retired by this rule.
Only missing source p42 and p156 qualifiers are bound to the canonical item.
"""
import copy
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
RULE = 'rules/cyberware/mm-shock-hand-configuration-p42-156.yml'
CANON = 'entities/cyberware/shock-hand.yml'
TABLE = 'entities/cyberware/shock-hand-table.yml'


def verify(rule, canonical, legacy_table):
    def need(ok, name):
        if not ok:
            raise ValueError(name)

    need(rule.get('id') == 'rule.cyberware.mm-shock-hand-configuration-p42-156' and
         rule.get('source') == 'source.mm' and
         rule.get('printed_pages') == '42-43,156' and
         rule.get('pdf_pages') == '42-43,157' and
         rule.get('content_class') == ['rule_procedure'], 'original_source_identity')
    d = rule['data']
    need(d['original_printed_pages'] == [42, 43, 156] and
         d['original_physical_pdf_pages'] == [42, 43, 157], 'original_page_alignment')
    need(d['canonical_entity_id'] == canonical['id'] == 'entity.cyberware.shock-hand' and
         d['canonical_entity_path'] == CANON, 'canonical_shock_hand_binding')
    i = d['implantation']
    need(i.get('normal_hand_locations') == ['knuckles', 'palm'] and
         i.get('intended_for_cyberlimbs') is True and
         i.get('natural_hand_insulation') == 'ceramic ridges and insulation protect the user' and
         i.get('other_permitted_extremities') == ['foot', 'elbow', 'other extremities'],
         'original_mounting_and_insulation')
    act = d['activation']
    need(act.get('requires_contact_with_target') is True and
         act.get('must_be_activated') is True and
         type(act.get('uses_before_recharge')) is int and
         act['uses_before_recharge'] == 12, 'source_contact_and_charge_rule')
    t = d['original_equipment_table']
    need(t.get('printed_page') == 156 and t.get('physical_pdf_page') == 157 and
         type(t.get('ammunition')) is int and t['ammunition'] == 12 and
         t.get('mode') == '—' and t.get('mode_is_firearm_action_category') is False,
         'source_ammo_and_mode')
    nd = d['nonduplication']
    need(nd.get('existing_entity_contains_damage_cost_essence') is True and
         nd.get('existing_entity_is_reused_not_replaced') is True and
         nd.get('source_table_row_reference') == TABLE and
         nd.get('original_duplicate_entity_id_not_retired_by_this_record') is True,
         'no_duplicate_mechanics_or_fictional_retirement')
    c = canonical['intrinsic']; old = legacy_table['intrinsic']
    need(c['damage'] == '8S Stun' and c['essence_cost'] == old['essence'] == 0.25 and
         c['cost_nuyen'] == old['cost_nuyen'] == 1300 and
         c['concealability'] == old['concealability'] == 5 and
         c['availability'] == old['availability'] == '6/4 days' and
         c['street_index'] == old['street_index'] == 2 and
         c['legality'] == old['legality'] == '4P-Q',
         'original_shock_hand_equipment_identity_disagreement')
    need(legacy_table['id'] == canonical['id'], 'legacy_id_collision_state_changed_reaudit')
    return True


class ShockHandSourceDeltaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rule = yaml.safe_load((ROOT / RULE).read_bytes())
        cls.canon = yaml.safe_load((ROOT / CANON).read_bytes())
        cls.table = yaml.safe_load((ROOT / TABLE).read_bytes())

    def rejects(self, rule=None, canon=None, table=None):
        with self.assertRaises(ValueError):
            verify(rule if rule is not None else self.rule,
                   canon if canon is not None else self.canon,
                   table if table is not None else self.table)

    def test_source_delta_binding_current_canon(self):
        self.assertTrue(verify(self.rule, self.canon, self.table))

    def test_bad_original_page_number_rejected(self):
        x = copy.deepcopy(self.rule); x['pdf_pages'] = '42-43,156'; self.rejects(rule=x)

    def test_wrong_source_rejected(self):
        x = copy.deepcopy(self.rule); x['source'] = 'source.sr3-core'; self.rejects(rule=x)

    def test_numerical_charge_capacity_cannot_be_string(self):
        x = copy.deepcopy(self.rule); x['data']['original_equipment_table']['ammunition'] = '12'; self.rejects(rule=x)

    def test_capacity_11_not_source(self):
        x = copy.deepcopy(self.rule); x['data']['activation']['uses_before_recharge'] = 11; self.rejects(rule=x)

    def test_firearm_mode_inferred_rejected(self):
        x = copy.deepcopy(self.rule); x['data']['original_equipment_table']['mode'] = 'SA'; self.rejects(rule=x)

    def test_inferred_foot_prohibition_rejected(self):
        x = copy.deepcopy(self.rule); x['data']['implantation']['other_permitted_extremities'] = ['elbow']; self.rejects(rule=x)

    def test_missing_natural_hand_insulation_rejected(self):
        x = copy.deepcopy(self.rule); x['data']['implantation']['natural_hand_insulation'] = None; self.rejects(rule=x)

    def test_not_a_second_entity_or_second_damage_code(self):
        x = copy.deepcopy(self.rule); x['data']['canonical_entity_id'] = 'entity.cyberware.shock-hand-2'; self.rejects(rule=x)

    def test_original_existing_damage_change_rejected(self):
        x = copy.deepcopy(self.canon); x['intrinsic']['damage'] = '10S Stun'; self.rejects(canon=x)

    def test_unreconciled_duplicate_not_hidden(self):
        x = copy.deepcopy(self.rule); x['data']['nonduplication']['original_duplicate_entity_id_not_retired_by_this_record'] = False; self.rejects(rule=x)

    def test_legacy_table_cost_disagreement_rejected(self):
        x = copy.deepcopy(self.table); x['intrinsic']['cost_nuyen'] = 1200; self.rejects(table=x)

if __name__ == '__main__':
    unittest.main()
