#!/usr/bin/env python3
"""Read-only PDF preparation for forward Pass B work; never acceptance evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import time

import fitz

SCHEMA = 'sr3-source-cache/v1'
PROFILE = hashlib.sha256(f'{SCHEMA}:{fitz.VersionBind}'.encode()).hexdigest()[:16]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def atomic_write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.tmp-')
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def select_pages(value, total):
    if value == 'all':
        return list(range(1, total + 1))
    selected = set()
    for part in value.split(','):
        if not re.fullmatch(r'[0-9]+(?:-[0-9]+)?', part):
            raise ValueError('invalid physical page selection')
        ends = list(map(int, part.split('-')))
        lo, hi = ends[0], ends[-1]
        if not 1 <= lo <= hi <= total:
            raise ValueError('physical page selection out of range')
        selected.update(range(lo, hi + 1))
    return sorted(selected)


def read_cache(path, identity):
    try:
        envelope = json.loads(path.read_bytes())
        payload = envelope['payload']
        if envelope['sha256'] == digest(encode(payload)) and all(payload[k] == v for k, v in identity.items()):
            return payload
    except (OSError, ValueError, TypeError, KeyError):
        pass
    return None


def extract_page(page, identity):
    tp = page.get_textpage(flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)
    text = page.get_text('text', textpage=tp, sort=False)
    blocks = page.get_text('dict', textpage=tp, sort=False)['blocks']
    words = page.get_text('words', textpage=tp, sort=False)
    hints = []
    if len(text.strip()) < 80 or len(words) < 15:
        hints.append('sparse_text_inspect_image')
    if '\ufffd' in text or '\x00' in text or re.search(r'\(cid:\d+\)', text):
        hints.append('suspect_glyphs_inspect_image')
    if len(re.findall(r'\b\d+\b', text)) >= 20:
        hints.append('numeric_dense_review_tables_and_units')
    mid = page.rect.width / 2
    left = sum(w[2] <= mid for w in words)
    right = sum(w[0] >= mid for w in words)
    if left >= 30 and right >= 30:
        hints.append('possible_columns_review_reading_order')
    return dict(identity, rect=list(page.rect), rotation=page.rotation,
                embedded_text=text, blocks=blocks, words=words,
                routing_hints=hints, review_required=True,
                mechanical_status='unreviewed', page_credit=False)


def render_page(page, folder, dpi):
    path = folder / f'image-{dpi}.png'
    sidecar = folder / f'image-{dpi}.sha256'
    try:
        if digest(path.read_bytes()) == sidecar.read_text().strip():
            return False
    except OSError:
        pass
    raw = page.get_pixmap(dpi=dpi, alpha=False).tobytes('png')
    atomic_write(path, raw)
    atomic_write(sidecar, (digest(raw) + '\n').encode())
    return True


def run(pdf, expected_sha, expected_pages, cache, selection='all', dpi=0):
    started = time.perf_counter()
    if not re.fullmatch(r'[0-9a-f]{64}', expected_sha) or expected_pages < 1:
        raise ValueError('independently pinned original SHA-256 and page count required')
    if dpi != 0 and not 72 <= dpi <= 400:
        raise ValueError('render DPI must be zero or 72-400')
    raw = Path(pdf).read_bytes()
    if digest(raw) != expected_sha:
        raise ValueError('original SHA-256 mismatch')
    hits = misses = rendered = 0
    hints = {}
    with fitz.open(stream=raw, filetype='pdf') as doc:
        if doc.is_repaired or doc.needs_pass or doc.page_count != expected_pages:
            raise ValueError('source is repaired, encrypted, or has unexpected physical page count')
        selected = select_pages(selection, doc.page_count)
        root = Path(cache) / expected_sha / PROFILE
        for n in selected:
            folder = root / f'p{n:04d}'
            path = folder / 'layout.json'
            identity = dict(schema=SCHEMA, profile=PROFILE, source_sha256=expected_sha,
                            physical_pages=expected_pages, physical_page=n)
            payload = read_cache(path, identity)
            if payload is None:
                payload = extract_page(doc[n - 1], identity)
                atomic_write(path, encode(dict(payload=payload, sha256=digest(encode(payload)))))
                misses += 1
            else:
                hits += 1
            for hint in payload['routing_hints']:
                hints[hint] = hints.get(hint, 0) + 1
            if dpi and render_page(doc[n - 1], folder, dpi):
                rendered += 1
    return dict(status='PREPARATION_ONLY', source_sha256=expected_sha, physical_pages=expected_pages,
                selected_pages=len(selected), cache_hits=hits, extracted_pages=misses,
                new_images=rendered, routing_hints=hints, cache_path=str(root),
                elapsed_seconds=round(time.perf_counter() - started, 3),
                mechanical_acceptance=False, page_credit=0)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdf', type=Path, required=True)
    p.add_argument('--sha256', required=True)
    p.add_argument('--expected-pages', type=int, required=True)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--select', default='all', help='physical PDF pages: all or 1,4-7')
    p.add_argument('--render-dpi', type=int, default=0, help='0 for layout only; render selected pages on demand')
    a = p.parse_args()
    try:
        result = run(a.pdf, a.sha256, a.expected_pages, a.cache, a.select, a.render_dpi)
    except (OSError, ValueError, RuntimeError) as exc:
        p.exit(1, f'PREPARATION_BLOCKED: {exc}\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
