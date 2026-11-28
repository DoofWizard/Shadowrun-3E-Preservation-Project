"""Exact, bounded legacy table and NPC rating pointer admission; no certification."""
import re

SOURCE = {
    'id': 'source.fasa-7219', 'catalog': 'FASA7219', 'publisher': 'FASA',
    'edition': 'SR3', 'physical_pages': 138,
    'manifest': 'sources/manifests/TargetMatrix.yml',
    'sha256': 'dc9fbba78b9eb5efc60941213a90dfa0be190275dc92ea671631ddb7db154c4b',
}
PATH = 'rules/matrix/target-matrix-grids.yml'
TABLES = {
    116: r'/satellite_host_ratings/(?:comsats|weather_sats|research_sats|surveillance_sats|sat_control_systems)/(?:security_code|acifs)',
    117: r'/doj/search_modifiers/(?:INS|FBI|UCAS_Marshals|DEA|Bureau_of_Prisons|Anti_Trust_Division|Office_of_Inspector_General)',
    118: r'/magicknet/threshold_guardian/stats/(?:core_rating|mpcp|pilot_skill|initiative|utility_pool|hacking_pool|utility_payload|utilities/(?:Attack_S|Armor|Scanner|Lock_on))',
    119: r'/shiawase_mifd/(?:smart_frames/(?:core_rating|initiative|pilot_rating|bod|evasion|masking|sensor|utilities/(?:Attack_M_sensitive|Armor_sensitive|Sniffer_sensitive|Browse_sensitive))|agents/(?:core_rating|initiative|pilot_rating|hacking_pool|bod|evasion|masking|sensor|utilities/(?:Attack_M_sensitive|Armor_sensitive|Sniffer_sensitive|Browse_sensitive))|semi_autonomous_knowbots/(?:core_rating|initiative|pilot_rating|hacking_pool|utility_pool|bod|evasion|masking|sensor|utilities/(?:Attack_S_sensitive|Armor_sensitive|Track_sensitive)))',
}


PERSONA_PATH = 'rules/matrix/target-matrix-persona-ratings.yml'
PERSONAS = {
    126: ('anubis', 'fastjack', 'grid_reaper'),
    127: ('link', 'red_wraith'),
    128: ('silvery_k', 'slamm_0', 'smiling_bandit', 'snow_tiger'),
    129: ('michael_sutherland',),
}


def target_matrix_table_pointer(binding, field, source, page):
    """Only the reviewed table shapes and ten exact NPC rating-pair pointers.

    The caller still verifies the actual original, typed value, class, record
    provenance, immutable journal, historical registration and independent review.
    """
    if not all(isinstance(x, dict) for x in (binding, field, source, page)):
        return False
    if any(type(source.get(k)) is not type(v) or source.get(k) != v for k, v in SOURCE.items()):
        return False
    n, pdf, pointer = page.get('printed'), page.get('pdf'), binding.get('pointer')
    if not (binding.get('mode', 'source_local') == 'source_local' and
            field.get('class') == 'rule_exact' and field.get('kind') == 'row' and
            type(n) is int and type(pdf) is int and pdf == n + 1 and
            isinstance(pointer, str)):
        return False
    if binding.get('path') == PATH:
        return n in TABLES and re.fullmatch(TABLES[n], pointer) is not None
    if binding.get('path') == PERSONA_PATH:
        return pointer in {f'/ratings/{name}/npc_ratings' for name in PERSONAS.get(n, ())}
    return False
