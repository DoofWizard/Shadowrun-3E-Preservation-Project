"""Source-reviewed SR3 baseline Condition Monitor adapter, not canonical ingestion.

Original: FASA Corporation, Shadowrun, Third Edition (FASA7001), printed
pp125-126/PDF126-127. Advanced Man & Machine consciousness procedures are
separate extensions, NOT silently substituted for the SR3 baseline.
"""
from __future__ import annotations
from dataclasses import dataclass

DAMAGE_BOXES = {"L": 1, "M": 3, "S": 6, "D": 10}
INJURY_MODIFIERS = {"uninjured": 0, "L": 1, "M": 2, "S": 3}
INITIATIVE_MODIFIERS = {"uninjured": 0, "L": -1, "M": -2, "S": -3}


def condition_level(boxes: int) -> str:
    """Cumulative highest wound level on a single ten-box track."""
    if type(boxes) is not int or boxes < 0:
        raise ValueError("damage boxes must be nonnegative integers")
    if boxes >= 10:
        return "D"
    if boxes >= 6:
        return "S"
    if boxes >= 3:
        return "M"
    if boxes >= 1:
        return "L"
    return "uninjured"


@dataclass(frozen=True)
class ConditionMonitor:
    body: int
    physical: int = 0
    stun: int = 0

    def __post_init__(self):
        if type(self.body) is not int or self.body < 1:
            raise ValueError("Body must be a positive integer")
        for x in (self.physical, self.stun):
            if type(x) is not int or x < 0:
                raise ValueError("damage must be nonnegative integer boxes")
        if self.stun > 10:
            raise ValueError("excess Stun must overflow to Physical")

    @property
    def physical_level(self) -> str:
        return condition_level(self.physical)

    @property
    def stun_level(self) -> str:
        return condition_level(self.stun)

    @property
    def physical_overflow(self) -> int:
        return max(0, self.physical - 10)

    @property
    def dead(self) -> bool:
        # SR3 p125: death on Physical overflow > Body, not >= Body.
        return self.physical_overflow > self.body

    @property
    def incapacitated(self) -> bool:
        return self.dead or self.physical >= 10 or self.stun >= 10

    @property
    def unconscious(self) -> bool:
        # Baseline; M&M p131 introduces additional resistance possibilities.
        return self.stun >= 10 or self.physical >= 10

    def apply(self, level: str, kind: str) -> "ConditionMonitor":
        """Apply final *staged* damage code; armor/resistance occurred upstream."""
        if level not in DAMAGE_BOXES:
            raise ValueError("expected staged damage L/M/S/D")
        boxes = DAMAGE_BOXES[level]
        if kind == "Physical":
            return ConditionMonitor(self.body, self.physical + boxes, self.stun)
        if kind == "Stun":
            new_stun = self.stun + boxes
            return ConditionMonitor(self.body, self.physical + max(0, new_stun - 10),
                                    min(10, new_stun))
        raise ValueError("damage kind must be Physical or Stun")

    def modifiers(self) -> tuple[int, int] | None:
        """(TN injury modifier, Initiative modifier); no actions if incapacitated.

        Original p126: highest wound level per track contributes independently,
        and Physical + Stun penalties are cumulative. Optional status effects
        from implants/pain editors/other supplements are not computed here.
        """
        if self.incapacitated:
            return None
        levels = (self.physical_level, self.stun_level)
        return (sum(INJURY_MODIFIERS[v] for v in levels),
                sum(INITIATIVE_MODIFIERS[v] for v in levels))
