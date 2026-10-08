#!/usr/bin/env python3
"""Validate editorial changes against source-reviewed structured extraction.

Usage: python connector_preflight.py BASELINE.yml CANDIDATE.yml
       python connector_preflight.py --self-test
Requires Python 3.10+ and PyYAML. No network, model calls, writes or word filter.
This is a preservation check, NOT a source verifier or connector acceptance test.
Only root headline/summary/framing are presentation. All other fields are frozen.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
import unittest
from typing import Any
import yaml

PROTECTED = frozenset({'rule_exact', 'rule_procedure', 'equipment_stat', 'character_option'})
NONMECHANICAL = frozenset({'world_fact', 'campaign_guidance', 'attributed_claim', 'narrative_context'})
PRESENTATION = frozenset({'headline', 'summary', 'framing'})
FRAMING = frozenset({'newsroom_neutral', 'broadcast_safe', 'reference_exact'})
REQUIRED = ('id', 'record_type', 'status', 'source', 'printed_pages', 'pdf_pages', 'edition_scope')

class InvalidRecord(ValueError):
    """Machine code only: never copy source prose into error receipts."""

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader: UniqueLoader, node: Any, deep: bool = False) -> dict:
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise InvalidRecord('mapping_key_must_be_string')
        if key in result:
            raise InvalidRecord('duplicate_mapping_key')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def load_text(text: str) -> dict:
    try:
        value = yaml.load(text, Loader=UniqueLoader)
    except InvalidRecord:
        raise
    except yaml.YAMLError as exc:
        raise InvalidRecord('yaml_parse_error') from exc
    if not isinstance(value, dict):
        raise InvalidRecord('record_must_be_mapping')
    return value

def check_json_tree(value: Any) -> None:
    if value is None or type(value) in (str, bool, int):
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise InvalidRecord('nonfinite_number')
        return
    if type(value) is list:
        for child in value:
            check_json_tree(child)
        return
    if type(value) is dict and all(type(k) is str for k in value):
        for child in value.values():
            check_json_tree(child)
        return
    raise InvalidRecord('unsupported_scalar_or_container')

def canonical(value: Any) -> str:
    check_json_tree(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)

def validate_shape(record: dict, candidate: bool) -> str:
    if not isinstance(record, dict):
        raise InvalidRecord('record_must_be_mapping')
    canonical(record)
    for key in REQUIRED:
        if type(record.get(key)) is not str or not record[key].strip():
            raise InvalidRecord('required_metadata_missing_or_invalid')
    classes = record.get('content_class')
    if type(classes) is not list or len(classes) != 1 or type(classes[0]) is not str:
        raise InvalidRecord('one_semantic_class_per_write_required')
    kind = classes[0]
    if kind not in PROTECTED | NONMECHANICAL:
        raise InvalidRecord('unknown_semantic_class')
    if type(record.get('data')) is not dict or not record['data']:
        raise InvalidRecord('structured_data_required')
    for field in PRESENTATION:
        if field in record and type(record[field]) is not str:
            raise InvalidRecord('presentation_must_be_text')
    if candidate:
        if record.get('framing') not in FRAMING:
            raise InvalidRecord('approved_framing_required')
        if kind in NONMECHANICAL and record['framing'] not in {'newsroom_neutral', 'broadcast_safe'}:
            raise InvalidRecord('nonmechanical_editorial_framing_required')
        if kind in PROTECTED and record['framing'] != 'reference_exact':
            raise InvalidRecord('protected_content_requires_reference_exact')
    return kind

def validate_pair(baseline: dict, candidate: dict) -> dict:
    kind = validate_shape(baseline, False)
    validate_shape(candidate, True)
    frozen_before = {k: v for k, v in baseline.items() if k not in PRESENTATION}
    frozen_after = {k: v for k, v in candidate.items() if k not in PRESENTATION}
    if canonical(frozen_before) != canonical(frozen_after):
        raise InvalidRecord('immutable_data_or_provenance_changed')
    digest = hashlib.sha256(canonical(frozen_before).encode('utf-8')).hexdigest()
    return {'status': 'pass', 'record_id': candidate['id'], 'content_class': kind,
            'immutable_sha256': digest, 'source_accuracy': 'requires_source_review',
            'connector_acceptance': 'not_tested'}

def validate_files(baseline: Path, candidate: Path) -> dict:
    baseline_bytes = baseline.read_bytes()
    candidate_bytes = candidate.read_bytes()
    result = validate_pair(load_text(baseline_bytes.decode('utf-8')), load_text(candidate_bytes.decode('utf-8')))
    result['baseline_file_sha256'] = hashlib.sha256(baseline_bytes).hexdigest()
    result['candidate_file_sha256'] = hashlib.sha256(candidate_bytes).hexdigest()
    return result

def fixture(kind: str = 'rule_procedure') -> dict:
    return {'id': 'reference.synthetic.fixture', 'record_type': 'reference', 'status': 'reviewed',
            'source': 'source.synthetic', 'printed_pages': '1', 'pdf_pages': '2',
            'edition_scope': 'synthetic_only', 'content_class': [kind],
            'framing': 'reference_exact' if kind in PROTECTED else 'newsroom_neutral',
            'summary': 'Synthetic reference.', 'data': {'target_number': 4, 'damage': '6M',
            'modifier': '+2', 'enabled': True, 'procedure': ['first', 'second'],
            'claim': {'speaker': 'Example', 'certainty': 'alleged', 'negated': False,
                      'voluntary': False, 'scope': 'one_site', 'actor': 'org.example'}}}

class PreflightTests(unittest.TestCase):
    def reject(self, candidate: dict, baseline: dict | None = None) -> None:
        with self.assertRaises(InvalidRecord):
            validate_pair(baseline or fixture(), candidate)
    def test_headline_and_summary_only(self):
        b = fixture(); c = copy.deepcopy(b); c['headline'] = 'Reference'; c['summary'] = 'Neutral reference.'
        self.assertEqual(validate_pair(b, c)['status'], 'pass')
    def test_each_protected_class(self):
        for kind in PROTECTED:
            with self.subTest(kind=kind):
                b = fixture(kind); self.assertEqual(validate_pair(b, copy.deepcopy(b))['status'], 'pass')
    def test_each_nonmechanical_class(self):
        for kind in NONMECHANICAL:
            with self.subTest(kind=kind):
                b = fixture(kind); self.assertEqual(validate_pair(b, copy.deepcopy(b))['status'], 'pass')
    def test_numeric_change(self):
        c=fixture(); c['data']['target_number']=5; self.reject(c)
    def test_damage_change(self):
        c=fixture(); c['data']['damage']='6L'; self.reject(c)
    def test_modifier_sign_change(self):
        c=fixture(); c['data']['modifier']='-2'; self.reject(c)
    def test_bool_not_integer(self):
        c=fixture(); c['data']['enabled']=1; self.reject(c)
    def test_integer_not_float(self):
        c=fixture(); c['data']['target_number']=4.0; self.reject(c)
    def test_integer_not_string(self):
        c=fixture(); c['data']['target_number']='4'; self.reject(c)
    def test_step_order_change(self):
        c=fixture(); c['data']['procedure'].reverse(); self.reject(c)
    def test_omission(self):
        c=fixture(); del c['data']['damage']; self.reject(c)
    def test_unsupported_addition(self):
        c=fixture(); c['data']['new_rule']=True; self.reject(c)
    def test_claim_attribution(self):
        c=fixture(); c['data']['claim']['speaker']='Other'; self.reject(c)
    def test_claim_certainty(self):
        c=fixture(); c['data']['claim']['certainty']='established'; self.reject(c)
    def test_negation(self):
        c=fixture(); c['data']['claim']['negated']=True; self.reject(c)
    def test_consent(self):
        c=fixture(); c['data']['claim']['voluntary']=True; self.reject(c)
    def test_scope(self):
        c=fixture(); c['data']['claim']['scope']='all_sites'; self.reject(c)
    def test_identity(self):
        c=fixture(); c['data']['claim']['actor']='org.other'; self.reject(c)
    def test_source_page_change(self):
        c=fixture(); c['printed_pages']='2'; self.reject(c)
    def test_edition_change(self):
        c=fixture(); c['edition_scope']='current_rules'; self.reject(c)
    def test_mixed_semantic_classes(self):
        c=fixture(); c['content_class'].append('world_fact'); self.reject(c)
    def test_unknown_class(self):
        c=fixture(); c['content_class']=['rule_approximate']; self.reject(c)
    def test_missing_data(self):
        c=fixture(); c['data']={}; self.reject(c)
    def test_bad_framing(self):
        c=fixture('world_fact'); b=copy.deepcopy(c); c['framing']='raw'; self.reject(c,b)
    def test_protected_framing(self):
        c=fixture(); c['framing']='newsroom_neutral'; self.reject(c)
    def test_duplicate_yaml_keys(self):
        with self.assertRaises(InvalidRecord): load_text('id: first\nid: second\n')
    def test_nonfinite_values(self):
        c=fixture(); c['data']['number']=float('nan'); self.reject(c)
    def test_list_root(self):
        with self.assertRaises(InvalidRecord): load_text('- one\n- two\n')
    def test_yaml_roundtrip(self):
        b=fixture(); self.assertEqual(validate_pair(b, load_text(yaml.safe_dump(b)))['status'], 'pass')

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', nargs='?', type=Path)
    parser.add_argument('candidate', nargs='?', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PreflightTests))
        return 0 if result.wasSuccessful() else 1
    if args.baseline is None or args.candidate is None:
        parser.error('baseline and candidate are required')
    try:
        result = validate_files(args.baseline, args.candidate)
    except (InvalidRecord, OSError, UnicodeError) as exc:
        code = str(exc) if isinstance(exc, InvalidRecord) else type(exc).__name__
        print(json.dumps({'status': 'fail', 'error_code': code}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == '__main__':
    sys.exit(main())
