"""Small fail-closed SR3 *original core* vehicle-mount consumer adapter.

Source: FASA Corporation, fictional tabletop game Shadowrun, Third Edition,
FASA7001 printed p307 / physical PDF316 (source SHA-256 begins 7661ba95).
Canonical: rules/vehicles/sr3-core-original-mounts-p307.yml.
NOT Rigger 3, Rigger 3 Revised, a complete vehicle builder, or a semantic
ingestion record. All source-specific equipment tables remain separate.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Sequence
from rules_probe import UnresolvedRule


# This consumes Body *mount points*, not an ammunition load or Cargo Factor.
# p307: hardpoint counts two Body points; firmpoint one; ordinary turret
# consumes *two hardpoints*, mini-turret one hardpoint.
MOUNT_POINTS = {
    "fixed_firmpoint": 1,
    "fixed_hardpoint": 2,
    "pintle": 1,
    "turret": 4,
    "mini_turret": 2,
}
INSTALLATION = {
    "fixed_firmpoint": (4, 24),
    "fixed_hardpoint": (4, 24),
    "pintle": (2, 12),
    "turret": (4, 72),
    "mini_turret": (4, 72),
}


def _nonnegative_int(value: int, name: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


@dataclass(frozen=True)
class MountCapacity:
    body: int
    used: int
    remaining: int
    legal: bool


def mount_capacity(body: int, mounts: Sequence[str]) -> MountCapacity:
    """Check core p307 point capacity; no Rigger 3 revised assumptions."""
    _nonnegative_int(body, "Body")
    if isinstance(mounts, (str, bytes)) or not isinstance(mounts, Sequence):
        raise ValueError("mounts must be a sequence of named mount types")
    used = 0
    for mount in mounts:
        if mount not in MOUNT_POINTS:
            raise UnresolvedRule(f"no original p307 mount-point rule for {mount!r}")
        used += MOUNT_POINTS[mount]
    return MountCapacity(body=body, used=used, remaining=body-used, legal=used<=body)


def mounting_allowed(mount: str, weapon_size: str) -> bool:
    """Only the three coarse sizes explicitly distinguished by p307.

    `small` means LMG, assault rifle or smaller; `mmg` means exactly MMG;
    `larger_than_mmg` includes HMG and larger. Caller's weapon catalog must
    establish size. The adapter never infers class from a model or caliber.
    """
    if mount not in MOUNT_POINTS:
        raise UnresolvedRule("mount type not provided by original p307")
    if weapon_size not in ("small", "mmg", "larger_than_mmg"):
        raise UnresolvedRule("weapon size needs an original source classification")
    if mount in ("fixed_firmpoint", "pintle"):
        return weapon_size == "small"
    if mount == "mini_turret":
        return weapon_size in ("small", "mmg")
    return True  # fixed hardpoint / full turret (subject to other rules)


@dataclass(frozen=True)
class Installation:
    test: str
    target_number: int
    base_hours: int


def mount_installation(mount: str) -> Installation:
    if mount not in INSTALLATION:
        raise UnresolvedRule("original p307 does not set installation for this mount")
    tn, hours = INSTALLATION[mount]
    return Installation(test="Vehicle B/R", target_number=tn, base_hours=hours)


@dataclass(frozen=True)
class SideFire:
    updated_handling: int
    requires_crash_test: bool


def fixed_mount_sidefire(handling: int, recoil: int) -> SideFire:
    """p307 only: side-facing fixed mount adds recoil to Handling, Crash Test.

    Do not synthesize Crash Test TN or resolve driver dice here.
    """
    _nonnegative_int(handling, "Handling")
    _nonnegative_int(recoil, "recoil")
    return SideFire(handling + recoil, True)


def halved_fixed_mount_recoil(recoil: int) -> int:
    """p307 says halve recoil; refuse odd values with unspecified rounding.

    This is *before* other compensation and does not independently decide
    doubled-heavy-weapon recoil or any optional Rigger 3 modifiers.
    """
    _nonnegative_int(recoil, "recoil")
    if recoil % 2:
        raise UnresolvedRule("core p307 gives no rounding rule for halved odd recoil")
    return recoil // 2


def mount_signature_delta(mount: str, *, external: bool | None = None) -> int:
    """Only explicitly asserted core p307 Signature changes.

    External fixed mounts reduce Signature by 1. Turrets and mini-turrets
    reduce it by 1. The excerpt does not establish the Signature of a
    concealed/internal fixed mount or a pintle; those paths fail closed.
    """
    if mount in ("fixed_firmpoint", "fixed_hardpoint"):
        if external is True:
            return -1
        raise UnresolvedRule("p307 only describes EXTERNAL fixed-mount Signature")
    if mount in ("turret", "mini_turret"):
        return -1
    raise UnresolvedRule("no specified original p307 Signature effect for this mount")


def turret_cargo_change(mount: str) -> int:
    """Return only p307 extra Cargo Factor, not p312 installed CF market cost."""
    if mount == "turret":
        return 2
    if mount == "mini_turret":
        return 1
    raise UnresolvedRule("p307 does not give a turret CF delta for this mount")


@dataclass(frozen=True)
class AircraftMissileMounts:
    number_of_mounts: int
    total_weight_kg: int
    legal: bool
    counts_against_body_mount_points: bool = False


def aircraft_external_missile_mounts(body: int, weights_kg: Sequence[int]) -> AircraftMissileMounts:
    """p307: at most Body external aircraft mounts, at most 300 kg each.

    Distinct from ground mounting, weapon launch control, and heavier
    reinforced mounts introduced elsewhere; not a full missile subsystem.
    """
    _nonnegative_int(body, "Body")
    if isinstance(weights_kg, (str, bytes)) or not isinstance(weights_kg, Sequence):
        raise ValueError("weights_kg must be a sequence")
    weights = tuple(_nonnegative_int(w, "missile weight") for w in weights_kg)
    return AircraftMissileMounts(
        number_of_mounts=len(weights),total_weight_kg=sum(weights),
        legal=len(weights)<=body and all(w<=300 for w in weights),
    )
