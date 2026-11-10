"""Consumer-only rules: FanPro Sprawl Survival Guide, Shadowrun Third Edition.

FanPro10667, printed pp122-123 / physical PDF pp123-124. Catalog source hash:
b0855865c06b20f8c71251d45d980d54470990af656277f5b9ace9264a9e309f.
Authoritative data: equipment/ssg-household-drone-market-p122.yml and
 equipment/ssg-electronic-paper-colorchange-p123.yml. No source approval,
Pass B page authorization, invented Rigger stats or ambiguous market alignment.
"""
from __future__ import annotations
from collections.abc import Mapping, Sequence


class UnresolvedSSGRule(ValueError):
    """No unverified inference from a fictional source table."""


def _data(record, identity):
    if not isinstance(record, Mapping) or record.get("id") != identity or record.get("source") != "source.fanpro-10667":
        raise UnresolvedSSGRule("wrong canonical source/record")
    result = record.get("data")
    if not isinstance(result, Mapping):
        raise UnresolvedSSGRule("missing canonical source data")
    return result


def household_drone_market(record):
    """Join the paired original eleven-row stat/price blocks by exact name."""
    d = _data(record, "equipment.ssg-household-drone-tables-p122")
    sc, vc, sr, vr = (d.get(k) for k in ("stat_columns", "vehicle_columns", "stat_rows", "vehicle_rows"))
    if not all(isinstance(x, list) for x in (sc, vc, sr, vr)) or len(sr) != len(vr) or len(sr) != 11:
        raise UnresolvedSSGRule("incomplete source table")
    if not {"model", "pilot", "handling"}.issubset(sc) or not {"model", "price_nuyen", "availability"}.issubset(vc):
        raise UnresolvedSSGRule("incorrect source columns")
    result = {}
    for a, b in zip(sr, vr):
        if len(a) != len(sc) or len(b) != len(vc):
            raise UnresolvedSSGRule("row/column mismatch")
        stats, market = dict(zip(sc, a)), dict(zip(vc, b))
        name = stats["model"]
        if not isinstance(name, str) or name != market["model"] or name in result:
            raise UnresolvedSSGRule("unmatched or duplicated model variant")
        price = market["price_nuyen"]
        if type(price) is not int or price <= 0 or not isinstance(market["availability"], str):
            raise UnresolvedSSGRule("unknown price/availability notation")
        result[name] = {"stats": stats, "market": market}
    return result


def household_fleet_cost_nuyen(record, exact_model_names):
    if isinstance(exact_model_names, (str, bytes)) or not isinstance(exact_model_names, Sequence):
        raise UnresolvedSSGRule("must provide an ordered list of exact model names")
    models = household_drone_market(record)
    try:
        return sum(models[name]["market"]["price_nuyen"] for name in exact_model_names)
    except (KeyError, TypeError) as exc:
        raise UnresolvedSSGRule("model/variant not printed in source") from exc


def electronic_paper_sheet_nuyen(record, size):
    """Only published 20 Mp standard and 50 Mp tabloid at 0.1¥/Mp."""
    d = _data(record, "equipment.ssg-electronic-paper-colorchange-p123")
    p = d.get("electronic_paper", {})
    key = {"standard": "standard_sheet_capacity_Mp", "tabloid": "tabloid_capacity_Mp"}.get(size)
    if not key or p.get("published_cost_expression") != "Mp x .1¥":
        raise UnresolvedSSGRule("unpublished paper size or cost expression")
    mp = p.get(key)
    if type(mp) is not int or mp <= 0 or mp % 10:
        raise UnresolvedSSGRule("paper price has unspecified fractional rounding")
    return mp // 10


def colorchange_paint_quote_nuyen(record, area_m2, add_controller=False):
    """Whole-meter paint-only price; optional one 2,000¥ controller.

    No guessed fractional-area rounding, installation, or Availability/Street
    Index. The published paint market columns are explicitly ambiguous.
    """
    d = _data(record, "equipment.ssg-electronic-paper-colorchange-p123")
    p = d.get("colorchange_paint", {})
    if type(area_m2) is not int or area_m2 <= 0 or type(add_controller) is not bool:
        raise UnresolvedSSGRule("only positive whole square meters and boolean option")
    unit, control = p.get("cost_per_square_meter_nuyen"), p.get("controller_cost_nuyen")
    if type(unit) is not int or type(control) is not int:
        raise UnresolvedSSGRule("missing source prices")
    return area_m2 * unit + (control if add_controller else 0)


def paint_market_availability(_record):
    raise UnresolvedSSGRule("published p123 paint Availability/Street Index alignment unresolved")
