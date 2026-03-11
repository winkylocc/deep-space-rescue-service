from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from models.rescue_vessel import RescueVessel
from .casualties import Casualties

if TYPE_CHECKING:
    from .destination import Destination


@dataclass
class Incident:
    incident_id: str
    destination: Destination
    incident_type: str
    severity: str  # LOW, MEDIUM, HIGH, EXTREME
    casualties: Casualties
    description: str
    time_reported: str  # keep simple for now
    expires_in_seconds: int = 0
    accepted: bool = False
    assigned_vessel: Optional[RescueVessel] = None

    def total_casualties(self) -> int:
        return self.casualties.total()

    def summary(self) -> str:
        c = self.casualties
        return (
            f"{self.incident_id}: {self.incident_type} at {self.destination.name} "
            f"(severity={self.severity}) | "
            f"total={c.total()} | "
            f"reported={self.time_reported}"
        )
    
    def details(self) -> str:
        vessel_name = self.assigned_vessel.name if self.assigned_vessel else "None"
        accepted_status = "Yes" if self.accepted else "No"

        return (
            "\n=== Incident DETAILS ===\n"
            f"Destination: {self.destination.name}\n"
            f"Environment: {self.destination.environment}\n"
            f"Danger Level: {self.destination.danger_level}\n"
            f"Incident Type: {self.incident_type}\n"
            f"Severity: {self.severity}\n"
            f"Casualties: {self.casualties}\n"
            f"Description: {self.description}\n"
            f"Accepted: {accepted_status}\n"
            f"Assigned Vessel: {vessel_name}\n"
            f"Expires: {self.expires_in_seconds}\n"
        )