"""Read-only proof of a new or changed verified manifest registration."""

ALIASES = (('id', 'record_id'), ('path', 'record_path'),
           ('commit', 'current_commit', 'commit_sha'),
           ('blob', 'current_blob', 'blob_sha'))
GATE_ALIASES = ('gate', 'gate_status')


def _require(ok, reason):
    if not ok:
        raise ValueError(reason)


def _values(entry, names):
    return [entry[k] for k in names if k in entry]


def _identity(entry):
    out = []
    for names in ALIASES:
        values = _values(entry, names)
        _require(values and all(type(v) is str and v == values[0] for v in values),
                 'registration_missing_or_conflicting_alias:' + names[0])
        out.append(values[0])
    return tuple(out)


def _gate(entry):
    """Require all simultaneously present gate aliases to agree exactly."""
    values = _values(entry, GATE_ALIASES)
    _require(all(type(v) is str and v == values[0] for v in values),
             'registration_conflicting_gate_status')
    return values[0] if values else None


def _registrations(tree, identity, ancestors=frozenset()):
    if not isinstance(tree, (dict, list)):
        return
    _require(id(tree) not in ancestors, 'cyclic_manifest_registration_tree')
    ancestors = ancestors | {id(tree)}
    if isinstance(tree, dict):
        # Inspect all independently accepted alias families, even when a
        # manifest nests corrections or reorders their registration lists.
        if (identity[0] in _values(tree, ALIASES[0]) or
                identity[1] in _values(tree, ALIASES[1])) and all(
                    _values(tree, names) for names in ALIASES):
            actual = _identity(tree)
            if actual[:2] == identity[:2]:
                yield actual, _gate(tree)
            elif actual[2:] == identity[2:]:
                raise ValueError('registration_identity_conflict')
        children = tree.values()
    else:
        children = tree
    for child in children:
        yield from _registrations(child, identity, ancestors)


def verify(git, manifest_path, index_commit, entry_pointer, identity, parse, ptr, blob):
    """Verify actual parent-to-index transition; never infer original receipts.

    Supports explicit id/path/commit/blob, record_id/record_path/current_*,
    and Target Wastelands id/path/commit_sha/blob_sha/gate_status schemas.
    Mixed aliases must agree; moving an old registration is not a new one.
    """
    record_id, record_path, semantic_commit, semantic_blob = identity
    git.changed(record_path, semantic_commit)
    git.changed(manifest_path, index_commit)
    parents = git.run('rev-list', '--parents', '-n', '1', index_commit).decode().split()
    _require(len(parents) == 2, 'single_index_parent_required')
    parent = parents[1]
    git.ancestor(semantic_commit, parent)
    git.ancestor(index_commit, git.head)
    _require(blob(git.read(record_path, semantic_commit)) == semantic_blob,
             'registration_semantic_blob_mismatch')
    historical = parse(git.read(manifest_path, index_commit))
    entry = ptr(historical, entry_pointer)
    _require(isinstance(entry, dict) and _identity(entry) == identity and
             _gate(entry) == 'verified', 'index_target_identity_mismatch')
    after = list(_registrations(historical, identity))
    _require(after.count((identity, 'verified')) == 1, 'duplicate_verified_registration')
    # An absent manifest is different from an unreadable or missing parent.
    present = git.run('ls-tree', '-z', parent, '--', manifest_path)
    before = list(_registrations(parse(git.read(manifest_path, parent)), identity)) if present else []
    _require((identity, 'verified') not in before, 'registration_already_verified_in_index_parent')
    return {'status': 'new_or_changed_verified_registration', 'index_parent': parent,
            'index_commit': index_commit, 'index_pointer': entry_pointer,
            'prior_same_record_registrations': len(before), 'formal_acceptance': False}
