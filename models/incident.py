from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .destination import Destination


@dataclass
class Incident:
    incident_id: str
    destination: Destination
    incident_type: (
        str  # solar_flare, asteroid_collision, reactor_malfunction, hull_breach
    )
    severity: str  # LOW, MEDIUM, HIGH, EXTREME
    casualties_critical: int
    casualties_priority: int
    casualties_stable: int
    description: str
    time_reported: str  # keep simple for now

    def total_casualties(self) -> int:
        return (
            self.casualties_critical + self.casualties_priority + self.casualties_stable
        )

    def summary(self) -> str:
        return (
            f"{self.incident_id}: {self.incident_type} at {self.destination} "
            f"(severity={self.severity}) | "
            f"critical={self.casualties_critical}, "
            f"priority={self.casualties_priority}, "
            f"stable={self.casualties_stable}, "
            f"total={self.total_casualties()} | "
            f"reported={self.time_reported}"
        )
