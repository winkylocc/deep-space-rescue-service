from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .destination import Destination
    from .incident import Incident
    from .rescue_mission import RescueMission

@dataclass
class RescueVessel:
        name: str
        fuel_level_pct: float
        max_range_km: int
        speed_km_s: float
        
        evac_capacity: int
        med_bays: int
        cargo_capacity_in_kgs: int
        
        status: str = "READY"
        """
        hazard_level to make sure we have that as equipment,maybe
        """
        def summary(self) -> str:
            return f"{self.name}: fuel={self.fuel_level_pct}%, and capacity of {self.evac_capacity}"
        def can_reach(self, destination: Destination) -> bool:
             return f"Is vessel able to get to Destination"
        def has_capacity_for(self, incident: Incident) -> bool:
             return f"Is there space on board for casualties"
        def assign_to_mission(self, mission: RescueMission) -> None:
             return f"Assign vessel to mission"
        def refuel(self, amount_pct: float) -> None:
             return f"Time to refuel"
        def consume_fuel_for_distance(self, distance_km: int) -> None:
             return f"How much fuel consumption"