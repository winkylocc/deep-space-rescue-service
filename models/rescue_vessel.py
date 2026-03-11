from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timedelta

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

    def summary(self) -> str:
        return (
            f"{self.name}: fuel={self.fuel_level_pct}%, "
            f"capacity (C/P/S)={self.critical_capacity}/{self.priority_capacity}/{self.stable_capacity}, "
            f"range={self.max_range_full_ly} LY"
        )

    @staticmethod
    def schedule_rescue_launch(vessel: "RescueVessel", incident) -> dict:
        start_time = datetime.now()

        travel_seconds = incident.destination.distance_from_hub_in_km / vessel.speed_km_s
        arrival_time = start_time + timedelta(seconds=travel_seconds)

        flight_log = {
            "vessel_name": vessel.name,
            "incident_id": incident.incident_id,
            "destination_name": incident.destination.name,
            "start_time": start_time,
            "arrival_time": arrival_time,
            "travel_seconds": travel_seconds,
            "flight_message": (
                f"{vessel.name} departing at "
                f"{start_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"expected arrival time is {arrival_time.strftime('%Y-%m-%d %H:%M:%S')} "
                f"at {incident.destination.name}."
            ),
        }
        return flight_log

    def refuel(self):
        while True:
            try:
                amount = int(input("Enter fuel added fuel amount: "))

                if self.fuel_level_pct + amount > self.fuel_capacity:
                    raise ValueError("Error with fuel capacity")

                self.fuel_level_pct += amount
                print(f"Current Fuel load: {self.fuel_level_pct}")
                break

            except ValueError as e:
                print("Invalid fuel amount", e)
                print("Try again!")