from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

# Why is this needed
if TYPE_CHECKING:
    from .incident import Incident
    from .rescue_vessel import RescueVessel
    from .port import Port

@dataclass
class RescueMission:
    mission_id: str
    incident: Incident
    assigned_vessel: Optional[RescueVessel] = None
    status: str = "PLANNED" # PLANNED, LAUNCHED, ON_SCENE, EVACUATING, COMPLETED, ABORTED

    def plan(self, vessel: RescueVessel, port: Optional[Port] = None) -> None:
        return f"Plan something here"
    def launch(self) -> None:
        return f"Launch instructions go here"
    def complete(self) -> None:
        return f"Trip complete"
    def abort(self, reason: str) -> None:
        return f"ABORT, ABORT, ABORT!!!!"