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
        fuel_level_pct: float = 100.0
        fuel_capacity: int = 200_000
        max_range_km: int = 2_000_000
        speed_km_s: float = 20.0
        
        evac_capacity: int = 10
        med_bays: int = 1
        cargo_capacity_in_kgs: int = 2_000
        
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
        
        def refuel(self):
             while True:
                  try:
                    amount = int(input("Enter fuel added fuel amount "))

                    if self.fuel_level_pct + amount > self.fuel_capacity:
                         raise ValueError("Error with fuel capacity")
                    
                    self.fuel_level_pct += amount
                    print(f"Current Fuel load: {self.fuel_level_pct}")
                    break
                  
                  except ValueError as e:
                       print("Invalid fuel amount", e)
                       print("Try again!")
        
        def consume_fuel_for_distance(self, distance_km: int):...
             