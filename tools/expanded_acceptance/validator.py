#!/usr/bin/env python3
"""Read-only candidate assessment, not source or corpus certification."""
import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

from source_edition import manifest_edition_matches, record_edition_matches
from binding_schema import safe_git_path, substantive_pointer, mm_registration, wastelands_registration

PROTOCOL = 'sr3-expanded-acceptance/v1'
CLASSES = {'rule_exact', 'rule_procedure', 'equipment_stat', 'character_option', 'campaign_guidance'}


class Blocked(ValueError):
    pass


def need(ok, code):
    if not ok:
        raise Blocked(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()


def pairs(items):
    out = {}
    for k, v in items:
        need(isinstance(k, str) and k not in out, 'duplicate_or_invalid_key')
        out[k] = v
    return out


class Strict(yaml.SafeLoader):
    pass


Strict.add_constructor('tag:yaml.org,2002:map', lambda loader, node: pairs(loader.construct_pairs(node)))


def parse(raw):
    return yaml.load(raw, Loader=Strict)


def pinned(path, digest):
    raw = Path(path).read_bytes()
    need(sha(raw) == digest, 'external_evidence_pin_mismatch:' + str(path))
    return json.loads(raw, object_pairs_hook=pairs)


def ptr(obj, path):
    need(isinstance(path, str) and path.startswith('/'), 'invalid_pointer')
    for p in path[1:].split('/'):
        need(not re.search(r'~(?![01])', p), 'invalid_pointer_escape')
        p = p.replace('~1', '/').replace('~0', '~')
        if isinstance(obj, list):
            need(bool(re.fullmatch(r'0|[1-9][0-9]*', p)), 'invalid_list_index')
            obj = obj[int(p)]
        else:
            obj = obj[p]
    return obj


def page_set(text):
    need(isinstance(text, str) and re.fullmatch(r'[1-9][0-9]*(?:-[1-9][0-9]*)?(?:,\s*[1-9][0-9]*(?:-[1-9][0-9]*)?)*', text), 'unsupported_page_notation')
    vals = []
    for token in text.split(','):
        a = token.strip().split('-')
        lo, hi = int(a[0]), int(a[-1])
        need(lo <= hi <= 10000, 'invalid_page_range')
        vals.extend(range(lo, hi + 1))
    need(vals == sorted(set(vals)), 'duplicate_or_unsorted_pages')
    return set(vals)


class Git:
    def __init__(self, root, head):
        self.root, self.head = Path(root), head
        self.commit(head)

    def run(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.PIPE)

    def commit(self, ref):
        need(isinstance(ref, str) and re.fullmatch(r'[0-9a-f]{40}', ref), 'full_commit_required')
        need(self.run('cat-file', '-t', ref).strip() == b'commit', 'not_commit')

    def ancestor(self, old, new):
        self.commit(old)
        self.commit(new)
        self.run('merge-base', '--is-ancestor', old, new)

    def changed(self, path, ref):
        self.commit(ref)
        parents = self.run('rev-list', '--parents', '-n', '1', ref).decode().split()
        # Inspect the complete tree delta, not a path-filtered diff. Treat a
        # rename as a deletion plus an addition; neither is a one-path write.
        need(len(parents) == 2, 'exact_path_commit_required:' + path)
        changed = self.run('diff', '--no-renames', '--name-only', '-z', parents[1], ref, '--')
        need(changed == path.encode('utf-8') + b'\0', 'exact_path_commit_required:' + path)

    def read(self, path, ref=None):
        need(safe_git_path(path), 'unsafe_path')
        return self.run('show', (ref or self.head) + ':' + path)


def artifact(a):
    raw = base64.b64decode(a['bytes_base64'], validate=True)
    need(a['original_locator'] and sha(raw) == a['sha256'], 'artifact_bytes_or_locator_mismatch')
    return raw


def assess(git, review, bindings, evidence, pdf_sha, pdf_count):
    s = review['source']
    need(review['protocol'] == PROTOCOL and evidence['protocol'] == PROTOCOL, 'schema_mismatch')
    need(review['reviewer'] and evidence['custodian'] and review['reviewer'] != evidence['custodian'], 'independent_review_required')
    need(s['sha256'] == pdf_sha and s['edition'] in ('SR2', 'SR3'), 'original_identity_mismatch')
    need(s['physical_pages'] == pdf_count and type(pdf_count) is int and pdf_count > 0, 'physical_page_count_mismatch')
    mp = s['manifest']
    need(mp.startswith('sources/manifests/') and mp.endswith('.yml'), 'manifest_path_required')
    mr = git.read(mp)
    manifest = parse(mr)
    for k, v in [('id', s['id']), ('source_pdf_sha256', pdf_sha), ('catalog_number', s['catalog']), ('publisher', s['publisher'])]:
        need(manifest[k] == v, 'manifest_identity_mismatch:' + k)
    need(manifest_edition_matches(s, manifest), 'manifest_identity_mismatch:edition')
    need(review['unresolved_fields'] == [], 'unresolved_original_fields')
    pages = review['pages']
    need([p['pdf'] for p in pages] == list(range(1, pdf_count + 1)), 'missing_duplicate_or_unordered_pdf_page')
    fields = {}
    printed = set()
    for p in pages:
        need(type(p['pdf']) is int and p['image_review'] and p['heading'], 'page_review_missing')
        n = p['printed']
        need(n is None or (type(n) is int and n > 0 and n not in printed), 'invalid_printed_mapping')
        if n is not None:
            printed.add(n)
        fs = p['fields']
        need(isinstance(fs, list), 'field_inventory_required')
        if p['disposition'] == 'mechanical':
            need(fs and n is not None, 'missing_page_mechanics_or_unsupported_unnumbered_mechanics')
        else:
            need(not fs and p['disposition'] in ('zero_rules', 'owner_omission') and p['reason'], 'explicit_zero_rule_disposition_required')
            if p['disposition'] == 'owner_omission':
                need(p['owner_authority'] and p['no_page_credit'] is True, 'omission_authority_required')
        for f in fs:
            fid = f['id']
            need(fid and fid not in fields and f['heading'] and f['class'] in CLASSES and f['kind'] in ('rule', 'row', 'condition', 'exception', 'example', 'procedure'), 'invalid_obligation')
            need(f['lineage'] in ('sr3_effective', 'sr3_optional', 'sr2_unsuperseded', 'sr2_superseded', 'preserved_variant'), 'lineage_required')
            need(not (s['edition'] == 'SR2' and f['lineage'].startswith('sr3')) and not (s['edition'] == 'SR3' and f['lineage'].startswith('sr2')), 'wrong_lineage_edition')
            if f['lineage'].startswith('sr2'):
                need(f['precedence_review'] and (f['lineage'] != 'sr2_superseded' or f['named_successor']), 'legacy_precedence_missing')
            need(f['value'] is not None and f['value'] != '' and f['value'] != [] and f['value'] != {}, 'empty_mechanical_value')
            fields[fid] = (f, p)
    for item in review['unrepresented_printed']:
        n = item['printed']
        need(type(n) is int and n > 0 and n not in printed and item['reason'] and item['authority'] and item['no_page_credit'] is True and item['disposition'] in ('accepted_scan_omission', 'original_folio_not_present'), 'unrepresented_printed_unresolved')
        printed.add(n)
    need(sorted(printed) == review['expected_printed_folios'], 'printed_folio_inventory_gap')
    need(fields and set(bindings) == set(fields), 'missing_or_extra_obligation_binding')
    conflicts = review['contradictions']
    seen = set()
    for c in conflicts:
        ids = c['fields']
        need(len(set(ids)) >= 2 and set(ids) <= set(fields) and c['disposition'] == 'preserve_distinct_variants' and c['reason'], 'unresolved_or_collapsed_contradiction')
        need(len({encoded(fields[i][0]['value']) for i in ids}) >= 2, 'contradiction_values_collapsed')
        need(all(fields[i][0]['lineage'] == 'preserved_variant' for i in ids), 'contradiction_lineage_missing')
        seen.update(ids)
    need(seen == {i for i, (f, _) in fields.items() if f['lineage'] == 'preserved_variant'}, 'unmapped_variant')
    cache = {}
    archive_diagnostics = {}
    for fid, (f, p) in fields.items():
        b = bindings[fid]
        if b.get('mode') == 'sr3-accepted-core-equivalence/v1':
            from core_equivalence import verify as verify_accepted_core_equivalence
            archive_diagnostics['core_equivalence:' + fid] = verify_accepted_core_equivalence(
                git, s, f, p, b, evidence.get('accepted_core_equivalence'),
                review['reviewer'], evidence['custodian'])
            continue
        need(b.get('mode', 'source_local') == 'source_local', 'unsupported_binding_mode:' + fid)
        path = b['path']
        need(substantive_pointer(b, f), 'cosmetic_binding:' + fid)
        if path not in cache:
            e = evidence['transactions'][path]
            if e.get('layout') == 'split_archive/v1':
                from receipt_binding import bind_archive
                r, archive_diagnostics[path] = bind_archive(git, s, path, e, review['reviewer'], evidence['custodian'])
            else:
                need('layout' not in e, 'unsupported_transaction_layout')
                rraw = git.read(path)
                r = parse(rraw)
                plan, receipt = e['plan'], e['confirm']
                need(e['historical_confirm_artifact'] and e['prewrite_journal_artifact'] and e['editorial_review_artifact'], 'historical_evidence_missing:' + path)
                journal = e['prewrite_journal_artifact']
                baseline_raw = artifact(journal['baseline'])
                need(artifact(journal['candidate']) == rraw and sha(baseline_raw) == e['baseline_sha256'] and json.loads(artifact(journal['plan']), object_pairs_hook=pairs) == plan, 'historical_journal_bytes_mismatch')
                frozen = lambda rec: {k: v for k, v in rec.items() if k not in {'headline', 'summary', 'framing'}}
                need(encoded(frozen(parse(baseline_raw))) == encoded(frozen(r)) and sha(encoded(frozen(r))) == plan['immutable_sha256'], 'historical_immutable_mismatch')
                need(json.loads(artifact(e['historical_confirm_artifact']), object_pairs_hook=pairs) == receipt, 'historical_confirm_artifact_mismatch')
                editorial = json.loads(artifact(e['editorial_review_artifact']), object_pairs_hook=pairs)
                need(editorial['source'] == s['id'] and editorial['source_sha256'] == pdf_sha and editorial['edition'] == s['edition'] and editorial['publisher'] == s['publisher'] and editorial['catalog'] == s['catalog'] and editorial['path'] == path and editorial['candidate_sha256'] == sha(rraw) and editorial['baseline_sha256'] == e['baseline_sha256'] and editorial['baseline_reviewed_independently'] is True and editorial['candidate_reviewed_independently'] is True and editorial['nested_text_reviewed'] is True and editorial['printed_pages'] == r['printed_pages'] and editorial['pdf_pages'] == r['pdf_pages'] and editorial['reviewed_edition_scope'] == r['edition_scope'], 'editorial_evidence_mismatch')
                need(re.fullmatch(r'[0-9a-f]{64}', e['baseline_sha256']) and re.fullmatch(r'[0-9a-f]{64}', plan['immutable_sha256']), 'journal_digest_missing')
                need(plan['protocol'] == 'sr3-gate/v1' and plan['status'] == 'preflighted', 'historical_prepare_missing')
                commit, index_commit = receipt['commit_sha'], e['index_commit']
                need(receipt == {**plan, 'status': 'verified', 'commit_sha': commit, 'readback_blob_sha': blob(rraw)}, 'historical_confirm_mismatch')
                for k, v in [('path', path), ('source', s['id']), ('pdf_sha256', pdf_sha), ('record_id', r['id']), ('printed_pages', r['printed_pages']), ('pdf_pages', r['pdf_pages']), ('candidate_sha256', sha(rraw)), ('expected_blob_sha', blob(rraw))]:
                    need(plan[k] == v, 'historical_plan_mismatch:' + k)
                need(r['source'] == s['id'] and r['edition_scope'] == editorial['reviewed_edition_scope'], 'record_source_or_edition_mismatch')
                git.changed(path, commit)
                git.changed(mp, index_commit)
                git.ancestor(commit, index_commit)
                git.ancestor(index_commit, git.head)
                need(git.read(path, commit) == rraw, 'semantic_commit_bytes_mismatch')
                ip = e['index_pointer']
                historical_ip = e.get('historical_index_pointer', ip)
                entry = ptr(manifest, ip)
                historical_manifest = parse(git.read(mp, index_commit))
                for k in ('id', 'source_pdf_sha256', 'catalog_number', 'publisher'):
                    need(historical_manifest[k] == manifest[k], 'index_source_identity_mismatch:' + k)
                need(manifest_edition_matches(s, historical_manifest), 'index_source_identity_mismatch:edition')
                need(encoded(entry) == encoded(ptr(historical_manifest, historical_ip)), 'index_history_mismatch')
                if mp == 'sources/manifests/TargetWastelands.yml':
                    wastelands_registration(s, r, plan, receipt, entry, ip)
                    if historical_ip != ip:
                        wastelands_registration(s, r, plan, receipt, entry, historical_ip)
                else:
                    for k, v in [('id', r['id']), ('path', path), ('commit', commit), ('blob', blob(rraw)), ('gate', 'verified')]:
                        need(entry[k] == v, 'unindexed_or_changed_record:' + k)
                    if 'content_class' in entry:
                        need(r['content_class'] == [entry['content_class']], 'index_class_mismatch')
                    else:
                        mm_registration(s, r, plan, receipt, e['baseline_sha256'], entry, ip)
                        if historical_ip != ip:
                            mm_registration(s, r, plan, receipt, e['baseline_sha256'], entry, historical_ip)
            need(record_edition_matches(s, r), 'record_source_or_edition_mismatch:' + path)
            cache[path] = r
        r = cache[path]
        need(r['content_class'] == [f['class']], 'bound_class_mismatch:' + fid)
        need(p['printed'] in page_set(r['printed_pages']) and p['pdf'] in page_set(r['pdf_pages']), 'bound_page_mismatch:' + fid)
        need(encoded(ptr(r, b['pointer'])) == encoded(f['value']), 'typed_field_mismatch:' + fid)
    return {'protocol': PROTOCOL, 'status': 'PASS', 'source': s['id'], 'manifest_blob': blob(mr), 'head': git.head, 'source_sha256': pdf_sha, 'fields': len(fields), 'physical_pages_checked': pdf_count, 'records_checked': len(cache), 'accepted_core_match_candidates': sum(k.startswith('core_equivalence:') for k in archive_diagnostics), 'archive_diagnostics': archive_diagnostics, 'formal_acceptance': False, 'engine_certified': False, 'global_pages_advanced': 0}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ('repo', 'head', 'pdf', 'review', 'review-sha', 'bindings', 'bindings-sha', 'evidence', 'evidence-sha'):
        ap.add_argument('--' + name, required=True)
    a = ap.parse_args()
    try:
        git = Git(a.repo, a.head)
        review = pinned(a.review, a.review_sha)
        bindings = pinned(a.bindings, a.bindings_sha)
        evidence = pinned(a.evidence, a.evidence_sha)
        import fitz
        with fitz.open(a.pdf) as doc:
            need(doc.is_pdf, 'original_pdf_required')
            count = len(doc)
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            for name in ('preservation_method.py', 'connector_preflight.py'):
                (t / name).write_bytes(git.read('tools/ingestion/' + name))
            (t / 'manifest.yml').write_bytes(git.read(review['source']['manifest']))
            out = subprocess.check_output([sys.executable, str(t / 'preservation_method.py'), 'verify-source', str(Path(a.pdf).resolve()), str(t / 'manifest.yml')])
            verification = json.loads(out)
        pdf_sha = sha(Path(a.pdf).read_bytes())
        need(verification['status'] == 'source_pdf_hash_verified' and verification['source'] == review['source']['id'] and verification['sha256'] == pdf_sha, 'actual_source_verification_required')
        result = assess(git, review, bindings, evidence, pdf_sha, count)
        # assess() is the structural comparison; the CLI additionally proves
        # each actual historical registration transition, for both layouts.
        from index_transition import verify as verify_index_transition
        transitions = {}
        for path in sorted({b['path'] for b in bindings.values() if b.get('mode', 'source_local') == 'source_local'}):
            e = evidence['transactions'][path]
            record = parse(git.read(path))
            if e.get('layout') == 'split_archive/v1':
                d = result['archive_diagnostics'][path]
                pointer = '/' + d['registration_key'].replace('~', '~0').replace('/', '~1')
                index_commit, semantic_commit = d['index_commit'], d['semantic_commit']
            else:
                pointer = e.get('historical_index_pointer', e['index_pointer'])
                index_commit, semantic_commit = e['index_commit'], e['confirm']['commit_sha']
            transitions[path] = verify_index_transition(
                git, review['source']['manifest'], index_commit, pointer,
                (record['id'], path, semantic_commit, blob(git.read(path))), parse, ptr, blob)
        result['index_registration_transitions'] = transitions
        # Original local index artifacts are distinct from present-day Git
        # history. Inline evidence must retain both; split archives already
        # bind their original receipt and snapshot in bind_archive().
        from inline_index_receipt import verify as verify_inline_index_receipt
        original_index_artifacts = {}
        for path, transition in transitions.items():
            e = evidence['transactions'][path]
            if e.get('layout') != 'split_archive/v1':
                original_index_artifacts[path] = verify_inline_index_receipt(
                    git, review['source']['manifest'], e, transition)
        result['original_inline_index_artifacts'] = original_index_artifacts
        # A corrected same-ID M&M record retains both original registrations.
        # Never pass the newest receipt alone when the predecessor is present.
        from mm_successor import PATH as mm_successor_path, verify as verify_mm_successor
        successor_chains = {}
        if mm_successor_path in transitions:
            e = evidence['transactions'][mm_successor_path]
            successor_chains[mm_successor_path] = verify_mm_successor(
                git, review['source'], e, review['reviewer'], evidence['custodian'],
                parse, ptr, blob, sha, encoded, artifact, pairs)
        result['successor_chains'] = successor_chains
        with tempfile.TemporaryDirectory() as tmp:
            t = Path(tmp)
            for name in ('ingestion_gate.py', 'connector_preflight.py'):
                (t / name).write_bytes(git.read('tools/ingestion/' + name))
            for path in sorted({b['path'] for b in bindings.values() if b.get('mode', 'source_local') == 'source_local'}):
                e = evidence['transactions'][path]
                if e.get('layout') == 'split_archive/v1':
                    continue  # Both actual gate rechecks already ran in bind_archive.
                j = e['prewrite_journal_artifact']
                (t / 'baseline.yml').write_bytes(artifact(j['baseline']))
                (t / 'candidate.yml').write_bytes(artifact(j['candidate']))
                actual = subprocess.check_output([sys.executable, str(t / 'ingestion_gate.py'), 'prepare', str(t / 'baseline.yml'), str(t / 'candidate.yml'), path, review['source']['id'], pdf_sha])
                need(json.loads(actual) == e['plan'], 'present_day_prepare_recheck_mismatch:' + path)
        result['present_day_prepare_rechecked'] = result['records_checked']
        result.update(source_verification=verification, review_sha256=a.review_sha, bindings_sha256=a.bindings_sha, evidence_sha256=a.evidence_sha, validator_blob=blob(Path(__file__).read_bytes()))
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, TypeError, KeyError, IndexError, OSError, subprocess.SubprocessError, yaml.YAMLError, ImportError, zipfile.BadZipFile, AttributeError) as exc:
        print(json.dumps({'protocol': PROTOCOL, 'status': 'BLOCKED', 'reason': str(exc), 'formal_acceptance': False, 'global_pages_advanced': 0}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
