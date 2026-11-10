"""Exact SR3 original rigger/vehicle Street Gear pricing and prerequisites.

FASA Corporation, *Shadowrun, Third Edition* (FASA7001), fictional tabletop
RPG, original printed p306 / physical PDF315. Canonical verified record:
``equipment/sr3-core-rigger-vehicle-gear-p306.yml``. The cataloged original
PDF SHA-256 is 7661ba959edba8376373ed0cef13a39ecb63a2e9da3a311c3f4982d15b758914.

These are *consumer* fixtures, not semantic ingestion or real-world vehicle
modification guidance. No automatic Rigger 3 / Rigger 3 Revised supersession.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class GearEntry:
    cost_nuyen: int
    availability: str
    street_index: float | None
    legality: str
    weight_kg: float | None = None
    cargo_factor: int | None = None
    load_kg: int | None = None
    granted_pilot_rating: int | None = None


def _positive_int(value: int, label: str) -> int:
    if type(value) is not int or value < 1:
        raise ValueError(f"{label} must be a positive integer")
    return value


def datajack_port(*, motorcycle: bool = False) -> GearEntry:
    """Original p306 per-vehicle item; not an implanted human datajack."""
    if type(motorcycle) is not bool:
        raise ValueError("motorcycle flag must be boolean")
    return GearEntry(5000 if motorcycle else 2500, "3/72 hrs", 1.5, "Legal",
                     cargo_factor=1, load_kg=15)


def remote_control_gear(*, vehicle_body: int, sensor_rating: int) -> GearEntry:
    """Vehicle remote network interface: Sensor >=1; costs Body x 2,500.

    Grants vehicle Pilot 1 and consumes no cargo space. This does *not* itself
    provide the separate Vehicle Control Gear needed for direct VCR rigging.
    """
    _positive_int(vehicle_body, "vehicle Body")
    _positive_int(sensor_rating, "vehicle Sensor Rating")
    return GearEntry(2500 * vehicle_body, "4/72 hrs", 2.0, "Legal",
                     cargo_factor=0, granted_pilot_rating=1)


def vehicle_control_gear(*, sensor_rating: int, datajack_port_installed: bool,
                         remote_control_gear_installed: bool) -> GearEntry:
    """VCR rigging adaptation, requiring Sensor>=1 and either source interface.

    Does not silently include the price/space of the required interface.
    """
    _positive_int(sensor_rating, "vehicle Sensor Rating")
    if type(datajack_port_installed) is not bool or type(remote_control_gear_installed) is not bool:
        raise ValueError("interface-installation flags must be boolean")
    if not (datajack_port_installed or remote_control_gear_installed):
        raise ValueError("Vehicle Control Gear requires datajack port or remote-control gear")
    return GearEntry(2500, "4/7 days", 2.0, "Legal",
                     cargo_factor=1, load_kg=10)


def remote_control_deck(rating: int) -> GearEntry:
    """Original remote-control deck, not a cyberdeck or free radio link."""
    _positive_int(rating, "deck Rating")
    return GearEntry(5000 * rating, "4/72 hrs", 2.0, "Legal", weight_kg=3.0)


def remote_control_eccm(rating: int) -> GearEntry:
    """One original ECCM rating tier, including Rating 10's missing Index.

    A null street index means the source prints an em dash; it is not 0.
    Unknown ratings are not extrapolated beyond the published table.
    """
    _positive_int(rating, "ECCM Rating")
    if rating <= 3:
        return GearEntry(7500 * rating, "4/7 days", 2.0, "Legal", weight_kg=1.5)
    if rating <= 6:
        return GearEntry(15000 * rating, "6/14 days", 3.0, "6P–V", weight_kg=2.0)
    if rating <= 9:
        return GearEntry(35000 * rating, "12/28 days", 4.0, "5P–W", weight_kg=2.5)
    if rating == 10:
        return GearEntry(500000, "18/45 days", None, "4P–W", weight_kg=2.5)
    raise ValueError("ECCM Rating 1–10 is the entire original p306 table")


def hitcher_jacks(*, rating: int, jack_count: int = 1) -> GearEntry:
    """Rating x 100 nuyen *per jack*; no unsupported rating ceiling assumed."""
    _positive_int(rating, "hitcher-jack Rating")
    _positive_int(jack_count, "jack count")
    return GearEntry(100 * rating * jack_count, "2/48 hours", 1.0, "Legal", weight_kg=0.0)


def screen_display() -> GearEntry:
    return GearEntry(100, "2/24 hours", 1.0, "Legal", weight_kg=0.5)


def intercom_speaker() -> GearEntry:
    return GearEntry(25, "2/24 hours", 1.0, "Legal", weight_kg=0.0)
