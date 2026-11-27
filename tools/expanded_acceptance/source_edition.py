"""Explicit source-edition identities; never infer edition from substrings."""

# The observed FanPro10662 manifest uses the long printed edition label.
# The review protocol keeps its canonical SR3 lineage token. No other source
# receives this exception and no record or manifest bytes are normalized.
RIGGER_REVISED = ('source.fanpro-10662', 'FanPro10662', 'FanPro',
                  'sources/manifests/Rigger3Revised.yml')
RIGGER_SCOPE = 'FanPro Rigger 3 Revised (FanPro10662), Shadowrun Third Edition'
RIGGER_LABEL = 'Shadowrun Third Edition'


def _identity(source):
    return tuple(source.get(k) for k in ('id', 'catalog', 'publisher', 'manifest'))


def manifest_edition_matches(source, manifest):
    """Compare canonical review edition with the exact source manifest label."""
    expected = source.get('edition')
    actual = manifest.get('edition')
    if expected not in ('SR2', 'SR3'):
        return False
    if _identity(source) == RIGGER_REVISED:
        return (expected == 'SR3' and actual in ('SR3', RIGGER_LABEL) and
                tuple(manifest.get(k) for k in ('id', 'catalog_number', 'publisher')) == RIGGER_REVISED[:3])
    return actual == expected


def record_edition_matches(source, record):
    """Narrow record-scope guard for the explicitly mapped source only."""
    if _identity(source) != RIGGER_REVISED:
        return True  # Other sources retain existing editorial scope gates.
    if (source.get('edition') != 'SR3' or record.get('source') != source.get('id') or
            record.get('edition_scope') != RIGGER_SCOPE):
        return False
    data = record.get('data')
    if not isinstance(data, dict):
        return False
    if 'publication' not in data:
        return True  # Exact record scope plus existing independent review still required.
    publication = data['publication']
    if not isinstance(publication, dict):
        return False
    expected = {'title': 'Rigger 3 Revised', 'publisher': 'FanPro',
                'catalog_number': 'FanPro10662', 'edition': RIGGER_LABEL,
                'source_id': source['id'], 'source_pdf_sha256': source['sha256'],
                'original_file_sha256': source['sha256']}
    # Do not allow any supplied publication identity to contradict its source.
    return all(k not in publication or publication[k] == v for k, v in expected.items())
