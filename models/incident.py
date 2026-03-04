from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .destination import Destination


@dataclass
class Incident:
    incident_id: str
    destination: Destination
    incident_type: str  # solar_flare, asteroid_collision, reactor_malfunction, hull_breach
    severity: str       # LOW, MEDIUM, HIGH, EXTREME
    casualties_critical: int
    casualties_priority: int
    casualties_stable: int
    time_reported: str  # keep simple for now

    def total_casualties(self) -> int:
        return f"Total casualties"
    def summary(self) -> str:
        return f"A summary of the Incident for logging"