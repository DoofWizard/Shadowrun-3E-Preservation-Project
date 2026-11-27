"""FASA7126 p47 Signature baseline contract; no new mechanics or certification.

The numeric starting value lives in an individually confirmed rules/ record.
The original cyberware Signature modifier at its historical (gate-ineligible)
path is reused as a single dependency. This test never rewrites either record.
"""
import copy
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
BASE = 'rules/cyberware/mm-signature-baseline-p47.yml'
MODIFIER = 'modifiers/cyberware/signature.yml'


def check_binding(base, modifier):
    def need(ok, reason):
        if not ok:
            raise ValueError(reason)

    need(base.get('id') == 'rule.cyberware.mm-signature-baseline-p47' and
         base.get('source') == 'source.mm' and
         base.get('printed_pages') == '47' and base.get('pdf_pages') == '47' and
         base.get('content_class') == ['rule_exact'], 'source_or_page_identity_mismatch')
    data = base['data']
    need(data.get('original_section') == 'Cyberware and Signature',
         'wrong_original_section')
    sig = data['character_signature']
    need(type(sig.get('ordinary_metahumans_other_than_trolls')) is int and
         sig['ordinary_metahumans_other_than_trolls'] == 6 and
         type(sig.get('trolls')) is int and sig['trolls'] == 5,
         'typed_original_signature_baseline_mismatch')
    need(sig.get('normally_applies') is True and sig.get('purpose') ==
         ['Sensor Tests', 'sensor-enhanced Gunnery Tests'],
         'original_application_scope_changed')
    link = data['modifier_reuse']
    need(link.get('existing_modifier_id') == 'modifier.cyberware.signature' and
         link.get('existing_modifier_path') == MODIFIER and
         link.get('base_record_does_not_repeat_modifier') is True,
         'unbound_or_double_applied_modifier')
    need(modifier.get('id') == 'modifier.cyberware.signature' and
         modifier.get('effective', {}).get('source') == 'source.mm' and
         modifier.get('effective', {}).get('page') == 47 and
         modifier.get('effect', {}).get('operation') == 'reduce' and
         modifier.get('effect', {}).get('target') == ['character Signature'] and
         modifier.get('effect', {}).get('value') ==
         'Character with Essence 0-3: -1 Signature; cyberzombie: an additional -1 per 2 points of negative Essence.',
         'existing_cyberware_modifier_changed_or_missing')
    need('cyberware_penalty' not in data and 'essence_penalty' not in data and
         'negative_essence_penalty' not in data,
         'duplicate_modifier_inside_baseline_record')
    return True


class MMSignatureBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = yaml.safe_load((ROOT / BASE).read_bytes())
        cls.modifier = yaml.safe_load((ROOT / MODIFIER).read_bytes())

    def rejects(self, base, modifier=None):
        with self.assertRaises(ValueError):
            check_binding(base, modifier or self.modifier)

    def test_live_original_source_bundle(self):
        self.assertTrue(check_binding(self.base, self.modifier))

    def test_source_is_exact_printed_p47_not_adjacent_page(self):
        b = copy.deepcopy(self.base); b['pdf_pages'] = '48'; self.rejects(b)

    def test_wrong_authoritative_source_is_rejected(self):
        b = copy.deepcopy(self.base); b['source'] = 'source.sr3-core'; self.rejects(b)

    def test_rejects_non_troll_base_5(self):
        b = copy.deepcopy(self.base); b['data']['character_signature']['ordinary_metahumans_other_than_trolls'] = 5; self.rejects(b)

    def test_rejects_troll_base_6(self):
        b = copy.deepcopy(self.base); b['data']['character_signature']['trolls'] = 6; self.rejects(b)

    def test_rejects_string_6_for_numeric_rating(self):
        b = copy.deepcopy(self.base); b['data']['character_signature']['ordinary_metahumans_other_than_trolls'] = '6'; self.rejects(b)

    def test_rejects_other_gameplay_scope(self):
        b = copy.deepcopy(self.base); b['data']['character_signature']['purpose'].append('all combat actions'); self.rejects(b)

    def test_rejects_silent_second_essence_penalty(self):
        b = copy.deepcopy(self.base); b['data']['essence_penalty'] = -1; self.rejects(b)

    def test_rejects_relocated_modifier_path(self):
        b = copy.deepcopy(self.base); b['data']['modifier_reuse']['existing_modifier_path'] = BASE; self.rejects(b)

    def test_rejects_double_apply(self):
        b = copy.deepcopy(self.base); b['data']['modifier_reuse']['base_record_does_not_repeat_modifier'] = False; self.rejects(b)

    def test_rejects_changed_existing_modifier(self):
        m = copy.deepcopy(self.modifier); m['effect']['value'] = 'apply -2'; self.rejects(self.base, m)

    def test_gate_eligible_new_baseline_path_separate_from_original_modifier(self):
        self.assertTrue(BASE.startswith('rules/'))
        self.assertTrue(MODIFIER.startswith('modifiers/'))
        self.assertNotEqual(BASE, MODIFIER)

if __name__ == '__main__':
    unittest.main()
