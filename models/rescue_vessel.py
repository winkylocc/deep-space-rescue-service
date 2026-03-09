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
    critical_capacity: int = 5
    priority_capacity: int = 5
    stable_capacity: int = 10
    max_range_full_ly: float = 5.0

    evac_capacity: int = 10
    med_bays: int = 1
    cargo_capacity_in_kgs: int = 2_000

    status: str = "READY"
    distance_from_hub_km: float = 0.0
    """
        hazard_level to make sure we have that as equipment,maybe
        """

    def summary(self) -> str:
        return (
           f"{self.name}: fuel={self.fuel_level_pct}%, "
           f"capacity (C/P/S)={self.critical_capacity}/{self.priority_capacity}/{self.stable_capacity}, "
           f"range={self.max_range_full_ly} LY" 
        )

    def estimated_travel_time_hrs(self, destination: Destination) -> float:
        total_distance = destination.distance_from_hub_in_km + self.distance_from_hub_km
        return round((total_distance / self.speed_km_s) / 3600, 1)

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

    def consume_fuel_for_distance(self, distance_km: int): ...
