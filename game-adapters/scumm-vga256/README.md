# SCUMM-style VGA 256-color game adapter — v0

**State:** isolated proof-of-contract / draft implementation. **Not** a completed game, compiled Godot project, full SR3 resolver, source-verification receipt, or modification to the preservation worker.

## Intent

Build a tabletop-rules-driven point-and-click narrative rather than a chain of hardcoded key-and-door puzzles. Graphics should feel like 320×200, indexed **VGA 256-color** adventure artwork; the palette is a rendering choice, not a limit on simulation complexity. Visible verbs and inventory expose actions. Source-backed Third Edition rules decide supported uncertain outcomes. Authored fiction describes the world and lets failure persist rather than resetting every scene.

The implementation is **engine-neutral**, with Godot a candidate for the eventual presentation. The authoritative corpus is the existing repository's accepted canonical SR3 records. The prototype does not modify any source manifest, checkpoint, source book, canonical rule, or automated ingestion routine.

## What this first package actually contains

- engine_ruleset_v0.json: machine-readable rule-ID/source mapping, implementation gates, missing source-review obligations, SR3 edition boundary and the action contract.
- reference_resolver.py: pure deterministic success tests, Rule of One, Rule of Six, open tests, basic opposed tests, success contests, initiative rolls, and initiative-pass grouping; each test consumes **explicit recorded dice** so results are replayable.
- tests/test_reference_resolver.py: executable standard-library regression vectors, including exploding sixes, all-ones, TN floor, ties, and non-exploding initiative. Tests are authored here; do not claim CI passed unless execution was independently confirmed.
- scenes/clinic_hallway_v0.json: original illustrative one-room action model; LOOK, USE, TALK, FORCE, PERSUADE, DECK, PERCEIVE, LISTEN and a **Shadow Beat** intent. It is a design contract, not yet a running point-and-click screen.

Run reference vectors from the repository root:

    python -m unittest discover -s game-adapters/scumm-vga256/tests -v

No dependencies beyond Python's standard library are used.

## Rule authority and scope separation

1. **Official SR3 current/operative:** resolve only a named, normalized, implemented SR3 rule with stable ID, exact provenance and tested inputs. The rules/tests and rules/initiative YAML records currently supply the reference kernel.
2. **Official SR3 present but not yet executable:** character creation, combat, magic, Matrix, rigging, progression, special opposed/melee ties and advanced options remain mapped and gated. A canonical YAML file is evidence of an existing record, not evidence of complete mechanics or validated source calculations.
3. **Historical/optional:** Second Edition materials may be stored in the same archive, but do not become SR3 rules by accidental import. Later books' additional, optional, updated or conflicting rules require explicit provenance and effective-status policy.
4. **Authored scenario:** props, dialogue, consequences and clue flags can be written for the game; they may not silently change the numbers, exceptions or precedence of an SR3 test.
5. **New game standards:** **Music** and **Shadow Beat** are separately versioned supplemental systems. This name is explicitly **Shadow Beat, not Shadow Weave**. No undocumented mechanics or sourcebook authority have been assigned to Shadow Beat; its behavior needs a specification before implementation.

The ruleset distinguishes canonical record presence, reference code, authored vectors, executed tests, independent source re-verification and game integration. Do not promote a record across those gates just because a file exists.

## Scene command flow

    mouse click / verb + hotspot
        -> authored action intent (actor, object, prerequisites)
        -> select authority (SR3 implemented / SR3 gated / authored / supplement)
        -> acquire required stats, equipment, modifiers and recorded RNG stream
        -> deterministic SR3 rule trace (if implemented)
        -> emit consequence event + persistent world-state delta
        -> render response and optional inspection of mechanics

**Important:** A gated action must *not* be reported as success or failure; the game can show a development placeholder until implementation. For example, the clinic has multiple potential approaches, but only basic LOOK/USE/TALK authored paths are specified; hacking and astral actions are not falsely presented as mechanically operational.

## Next precise engineering steps

1. Execute the tests against the committed Python file; fix failures and attach results. Inspect SR3 core source pages for every implemented test before calling it source-reverified.
2. Normalize the numerical Master Character Creation Table into a versioned fixture, including priority assignments, metatype, Magic, Attributes, Skills, Resources and relevant Companion variants.
3. Add attack/dodge/resist/staging/Condition Monitor vectors, followed by combat pool timing and initiative ties, including **melee's attacker-favoring tie exception** without corrupting ordinary opposed tests.
4. Add magical Drain and simultaneous Matrix System/Security traces using their source-reviewed numeric examples; keep Matrix pp76–94 deferred options separate.
5. Link action intent objects and logged game-state events to the tested resolver, then render the clinic in indexed VGA art.
6. Specify Music and Shadow Beat as creative supplemental systems only after their actual expected behavior is defined.

## Evidence / outstanding preservation issues

The existing docs/engine-readiness/MECHANICS_READINESS_24H_2026-11-09.md records the current mechanical triage, including SR3 Street Gear p275–282/p305–311, Companion p32–43/p44–58, Matrix p76–94 and Sprawl Survival Guide p118–126 normalization debt. The authoritative preservation checkpoint and its separate hourly worker stay unchanged. For this adapter, the original publisher page images have **not** yet been independently reacquired or reverified, so there is **no** new claim of published-source fidelity.

This package remains deliberately small so that complete source-reviewed behavior, rather than overbroad untested ingestion counts, can establish the first playable milestone.
