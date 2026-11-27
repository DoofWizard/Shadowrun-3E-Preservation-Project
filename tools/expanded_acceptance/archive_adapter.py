"""Read-only adapter for retained split prewrite/confirmed journal ZIPs.

This is a diagnostic, not an acceptance gate or a historical receipt issuer.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile
import yaml

PRE = ('journal/baseline.yml', 'journal/candidate.yml', 'journal/plan.json', 'source-review.txt')
POST = PRE + ('journal/verified.json', 'journal/readback-receipt.json', 'journal/index-receipt.json', 'journal/indexed-manifest.yml')


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def pairs(items):
    result = {}
    for k, v in items:
        require(isinstance(k, str) and k not in result, 'duplicate_or_invalid_key')
        result[k] = v
    return result


class Strict(yaml.SafeLoader):
    pass


Strict.add_constructor('tag:yaml.org,2002:map', lambda loader, node: pairs(loader.construct_pairs(node)))


def load_json(raw):
    return json.loads(raw, object_pairs_hook=pairs)


def read_archive(raw, expected_sha, names):
    require(sha(raw) == expected_sha, 'archive_pin_mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        all_names = [x.filename for x in z.infolist()]
        require(len(all_names) == len(set(all_names)), 'duplicate_zip_member')
        require(set(all_names) - {'journal/'} == set(names), 'unsupported_or_missing_archive_members')
        require(sum(x.file_size for x in z.infolist()) <= 32 * 1024 * 1024, 'archive_size_limit')
        return {n: z.read(n) for n in names}


def inspect(pre, post, pre_sha, post_sha, gate, semantic_commit_blob, live_record_blob, index_commit_blob):
    a = read_archive(pre, pre_sha, PRE)
    b = read_archive(post, post_sha, POST)
    require(all(a[n] == b[n] for n in PRE), 'prewrite_archive_changed')
    require(a['source-review.txt'].strip(), 'missing_source_review')
    plan = load_json(a['journal/plan.json'])
    receipt = load_json(b['journal/verified.json'])
    rb = load_json(b['journal/readback-receipt.json'])
    idx = load_json(b['journal/index-receipt.json'])
    raw = a['journal/candidate.yml']
    baseline = a['journal/baseline.yml']
    mr = b['journal/indexed-manifest.yml']
    for c in (rb['commit'], idx['commit']):
        require(re.fullmatch('[0-9a-f]{40}', c), 'full_commit_required')
    require(rb['exact_commit_live_bytes'] is True and idx['exact_commit_live_bytes'] is True, 'stored_readback_missing')
    require(type(rb['candidate_bytes']) is int and rb['candidate_bytes'] == len(raw), 'readback_length_mismatch')
    require(blob(raw) == rb['blob'] == semantic_commit_blob == live_record_blob, 'record_blob_mismatch')
    require(blob(mr) == idx['blob'] == index_commit_blob, 'index_blob_mismatch')
    require(re.fullmatch(r'sources/manifests/[A-Za-z0-9_.-]+\.yml', idx['path']), 'manifest_path_required')
    m = yaml.load(mr, Loader=Strict)
    e = m[idx['registration_key']]
    record = yaml.load(raw, Loader=Strict)
    required = {'source_id': plan['source'], 'original_pdf_sha256': plan['pdf_sha256'], 'record_id': plan['record_id'], 'record_path': plan['path'], 'current_commit': rb['commit'], 'current_blob': rb['blob'], 'baseline_sha256': sha(baseline), 'candidate_sha256': sha(raw), 'immutable_sha256': plan['immutable_sha256'], 'gate': 'verified', 'actual_confirm': 'verified'}
    require(all(e[k] == v for k, v in required.items()), 'correction_registration_mismatch')
    require(m['id'] == plan['source'] and m['source_pdf_sha256'] == plan['pdf_sha256'], 'index_source_mismatch')
    require(record['content_class'] == [e['content_class']], 'index_class_mismatch')
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)
        for n in PRE[:3]:
            (p / Path(n).name).write_bytes(a[n])
        def execute(*args):
            return load_json(subprocess.check_output([sys.executable, str(Path(gate).resolve()), *map(str, args)]))
        actual = execute('prepare', p/'baseline.yml', p/'candidate.yml', plan['path'], plan['source'], plan['pdf_sha256'])
        require(actual == plan, 'present_day_prepare_mismatch')
        actual = execute('confirm', p/'plan.json', p/'candidate.yml', rb['commit'], rb['blob'])
        require(actual == receipt, 'present_day_confirm_mismatch')
    return {'status': 'BLOCKED', 'journal_consistency': 'consistent_stored_evidence', 'reason': 'requires_independent_editorial_binding_live_index_and_ancestry_original_review', 'source': plan['source'], 'path': plan['path'], 'semantic_commit': rb['commit'], 'semantic_blob': rb['blob'], 'index_commit': idx['commit'], 'index_blob': idx['blob'], 'registration_key': idx['registration_key'], 'prewrite_sha256': pre_sha, 'confirmed_sha256': post_sha, 'artifact_sha256': {n: sha(b[n]) for n in POST}, 'present_day_prepare_rechecked': True, 'present_day_confirm_rechecked': True, 'formal_acceptance': False, 'global_pages_advanced': 0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for n in ('pre', 'post', 'pre-sha', 'post-sha', 'gate', 'semantic-commit-blob', 'live-record-blob', 'index-commit-blob'):
        p.add_argument('--' + n, required=True)
    a = p.parse_args()
    try:
        r = inspect(Path(a.pre).read_bytes(), Path(a.post).read_bytes(), a.pre_sha, a.post_sha, a.gate, a.semantic_commit_blob, a.live_record_blob, a.index_commit_blob)
    except (ValueError, TypeError, KeyError, IndexError, OSError, yaml.YAMLError, zipfile.BadZipFile, subprocess.SubprocessError) as e:
        r = {'status': 'BLOCKED', 'reason': str(e), 'formal_acceptance': False, 'global_pages_advanced': 0}
    print(json.dumps(r, sort_keys=True))
    return 1


if __name__ == '__main__':
    sys.exit(main())
