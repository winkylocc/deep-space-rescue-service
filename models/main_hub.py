from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .rescue_vessel import RescueVessel
    from .port import Port
    from .incident import Incident
    from .rescue_mission import RescueMission

"""
Central command and logistics center that coordinates rescue operations.
Rescue vessels are stationed
Incidents are reported
Missions are planned
Vessels are dispatched
Survivors are returned or routed to ports
"""
@dataclass
class MainHub:
    name: str
    fleet: List[RescueVessel] = field(default_factory=list)
    ports: List[Port] = field(default_factory=list)

    def register_vessel(self, vessel: RescueVessel) -> None:
        return f"Registers the vessel"
    def register_port(self, port: Port) -> None:
        f"Registers the port"
    def report_incident(self, incident: Incident) -> None:
        return f"Report the incident"
    def select_best_vessel(self, incident: Incident) -> Optional[RescueVessel]:
        return f"Select best vessel for this journey"
    def create_mission(self, incident: Incident) -> RescueMission:
        return f"Create initial mission"
    def dispatch(self, mission: RescueMission) -> None:
        return f"Dispatch the vessel to the site"