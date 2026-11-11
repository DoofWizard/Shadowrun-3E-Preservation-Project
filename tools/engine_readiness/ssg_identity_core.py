"""Bounded *consumer* of an accepted FanPro Sprawl Survival Guide SR3 record.

Original fictional tabletop RPG, FanPro10667, printed pp125-127 / physical
PDF126-128, verified source SHA-256:
b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f.
Canonical reference: rules/identity/ssg-fictional-id-creation-options-p125-127.yml.

Only published game-test arithmetic, never real-world identity construction.
No new source ingestion, page advancement, inferred supersession, or rounding.
"""
from __future__ import annotations
from fractions import Fraction
from math import ceil
from collections.abc import Mapping


class UnresolvedSSGIdentity(ValueError):
    """Input or source record does not authorize a deterministic game outcome."""


def _natural(value, name, positive=False):
    if type(value) is not int or value < (1 if positive else 0):
        raise UnresolvedSSGIdentity(f"{name} must be a {'positive' if positive else 'nonnegative'} whole number")
    return value


def _canonical(record):
    if not isinstance(record, Mapping) or record.get("id") != "rule.identity.ssg-fictional-id-creation-options-p125-127" or record.get("source") != "source.fanpro-10667":
        raise UnresolvedSSGIdentity("wrong canonical ID or source")
    data = record.get("data")
    if not isinstance(data, Mapping):
        raise UnresolvedSSGIdentity("missing canonical data")
    publication = data.get("publication")
    if not isinstance(publication, Mapping) or publication.get("catalog_number") != "FanPro10667" or publication.get("edition") != "Shadowrun Third Edition":
        raise UnresolvedSSGIdentity("unverified publication context")
    return data


def id_creation_game_test(record, intended_rating, appropriate_contacts, successes=None):
    """Exact TN/time/cost for the fictional optional ID game test.

    If successes=None, return prerequisites only. A zero-success result is a
    failed game test which consumes half of the ADJUSTED base time. Fractions
    preserve nonintegral times rather than guessing a rounding convention.
    """
    d = _canonical(record).get("optional_id_rating_creation_game_test", {})
    expected = {
        "game_test_target_number_formula": "2 x desired fictional ID rating",
        "base_time_days_formula": "desired fictional ID rating x 10",
        "required_contacts_count": "Number of appropriate fictional professional/institutional contacts equals desired ID rating",
        "fictional_nuyen_cost_formula": "desired ID rating squared x 100",
    }
    if not isinstance(d, Mapping) or any(d.get(k) != v for k, v in expected.items()):
        raise UnresolvedSSGIdentity("canonical game test formulas not established")
    r = _natural(intended_rating, "intended_rating", positive=True)
    c = _natural(appropriate_contacts, "appropriate_contacts")
    deficit = max(r - c, 0)
    tn = 2*r + deficit
    base_days = 10*r + 10*deficit
    outcome = {"target_number": tn, "adjusted_base_days": base_days,
               "nuyen_cost": 100*r*r, "contact_deficit": deficit}
    if successes is not None:
        n = _natural(successes, "successes")
        outcome["test_succeeded"] = n > 0
        outcome["elapsed_days"] = Fraction(base_days, n if n else 2)
    return outcome


def id_random_edge_or_flaw(record, d6):
    """Optional published one-die allocation; never automatic in every game."""
    p = _canonical(record).get("id_edges_flaws_optional_policy", {})
    x = p.get("random_assignment_optional", {}) if isinstance(p, Mapping) else {}
    if x.get("die") != "1D6" or x.get("result_1") != "One fictional ID Flaw" or x.get("result_6") != "One fictional ID Edge":
        raise UnresolvedSSGIdentity("unverified random allocation")
    if type(d6) is not int or not 1 <= d6 <= 6:
        raise UnresolvedSSGIdentity("die outside 1D6")
    return "flaw" if d6 == 1 else "edge" if d6 == 6 else None


def id_price_with_optional_traits(record, base_price_nuyen, edges=0, flaws=0):
    """Apply 20% additive base-price increments, no invented rounding.

    The book *recommends* no more than three Edges/Flaws, rather than enacting
    a mandatory mechanical upper bound. Report that advisory separately.
    """
    p = _canonical(record).get("id_edges_flaws_optional_policy", {})
    if p.get("recommended_maximum_edges_or_flaws") != 3 or p.get("less_expensive_IDs") != "20 percent decrease in fictional purchase price for each Flaw" or p.get("premium_IDs") != "20 percent increase in fictional purchase price for each Edge":
        raise UnresolvedSSGIdentity("unverified game trait price rules")
    base = _natural(base_price_nuyen, "base_price_nuyen", positive=True)
    edge_count = _natural(edges, "edges")
    flaw_count = _natural(flaws, "flaws")
    factor = Fraction(5 + edge_count - flaw_count, 5)
    if factor <= 0:
        raise UnresolvedSSGIdentity("nonpositive price is not addressed by the source")
    return {"nuyen": base*factor, "recommended_trait_count_exceeded": edge_count + flaw_count > 3}


def home_turf_rating(record, rating, in_selected_jurisdiction):
    d = _canonical(record).get("id_edge_effects", {}).get("home_turf", {})
    if d.get("special_jurisdiction_effective_rating") != "ceil(base_rating x 1.5)":
        raise UnresolvedSSGIdentity("unverified Home Turf mechanics")
    r = _natural(rating, "rating", positive=True)
    if type(in_selected_jurisdiction) is not bool:
        raise UnresolvedSSGIdentity("GM-selected jurisdiction must be explicit")
    return (3*r+1)//2 if in_selected_jurisdiction else r


def limitation_rating(record, rating, in_selected_jurisdiction):
    d = _canonical(record).get("id_flaw_effects", {}).get("limitation", {})
    if d.get("effective_rating_in_designated_jurisdiction") != "floor(base ID rating / 2)":
        raise UnresolvedSSGIdentity("unverified Limitation mechanics")
    r = _natural(rating, "rating", positive=True)
    if type(in_selected_jurisdiction) is not bool:
        raise UnresolvedSSGIdentity("GM-selected jurisdiction must be explicit")
    if not in_selected_jurisdiction:
        return {"automatic_failure": False, "effective_rating": r}
    if r == 1:
        return {"automatic_failure": True, "effective_rating": None}
    return {"automatic_failure": False, "effective_rating": r//2}


def id_expiration_months(record, rating, d6):
    d = _canonical(record).get("id_flaw_effects", {}).get("expiration_date", {})
    if d.get("months_after_creation") != "ID rating x result of 1D6":
        raise UnresolvedSSGIdentity("unverified Expiration Date mechanics")
    r = _natural(rating, "rating", positive=True)
    if type(d6) is not int or not 1 <= d6 <= 6:
        raise UnresolvedSSGIdentity("die outside 1D6")
    return r*d6


def deterioration_interval(_record):
    raise UnresolvedSSGIdentity("canonical source explicitly leaves fixed versus changing rating interval ambiguous")
