from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from .incident import Incident


@dataclass
class RescueVessel:
    name: str
    fuel_level_pct: float = 100.0
    fuel_capacity: int = 200_000

    max_range_full_ly: float = 5.0
    speed_ly_s: float = 0.25

    critical_capacity: int = 5
    priority_capacity: int = 5
    stable_capacity: int = 10

    evac_capacity: int = 10
    med_bays: int = 1
    cargo_capacity_in_kgs: int = 2_000
    status: str = "READY"

    def summary(self) -> str:
        return (
            f"{self.name}: fuel={self.fuel_level_pct}%, "
            f"capacity (C/P/S)={self.critical_capacity}/{self.priority_capacity}/{self.stable_capacity}, "
            f"range={self.max_range_full_ly} LY, "
            f"status={self.status}"
        )

    def can_reach(self, incident: "Incident") -> bool:
        return incident.destination.distance_ly <= self.max_range_full_ly

    def has_capacity_for(self, incident: "Incident") -> bool:
        return (
            incident.casualties.critical <= self.critical_capacity
            and incident.casualties.priority <= self.priority_capacity
            and incident.casualties.stable <= self.stable_capacity
        )

    def schedule_rescue_launch(self, incident: "Incident") -> dict:
        if self.speed_ly_s <= 0:
            raise ValueError(f"{self.name} cannot launch because speed_ly_s must be greater than 0.")

        start_time = datetime.now()
        travel_seconds = incident.destination.distance_ly / self.speed_ly_s
        arrival_time = start_time + timedelta(seconds=travel_seconds)

        return {
            "vessel_name": self.name,
            "incident_id": incident.incident_id,
            "destination_name": incident.destination.name,
            "start_time": start_time,
            "arrival_time": arrival_time,
            "travel_seconds": travel_seconds,
            "flight_message": (
                f"{self.name} departing at "
                f"{start_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"expected arrival time is {arrival_time.strftime('%Y-%m-%d %H:%M:%S')} "
                f"at {incident.destination.name}."
            ),
        }

    def launch_rescue(self, incident: "Incident") -> dict:
        destination = incident.destination

        if self.status != "READY":
            return {
                "success": False,
                "message": f"Mission aborted: {self.name} is not READY."
            }

        if not self.can_reach(incident):
            return {
                "success": False,
                "message": (
                    f"Mission aborted: destination {destination.name} is too far "
                    f"({destination.distance_ly} LY). "
                    f"Max range is {self.max_range_full_ly} LY."
                )
            }

        if incident.casualties.critical > self.critical_capacity:
            return {
                "success": False,
                "message": (
                    f"Mission aborted: critical casualty count exceeds capacity "
                    f"({incident.casualties.critical}/{self.critical_capacity})."
                )
            }

        if incident.casualties.priority > self.priority_capacity:
            return {
                "success": False,
                "message": (
                    f"Mission aborted: priority casualty count exceeds capacity "
                    f"({incident.casualties.priority}/{self.priority_capacity})."
                )
            }

        if incident.casualties.stable > self.stable_capacity:
            return {
                "success": False,
                "message": (
                    f"Mission aborted: stable casualty count exceeds capacity "
                    f"({incident.casualties.stable}/{self.stable_capacity})."
                )
            }

        flight_log = self.schedule_rescue_launch(incident)
        self.status = "DEPLOYED"

        return {
            "success": True,
            "message": (
                f"Mission started successfully: {self.name} launched to "
                f"{destination.name}. Distance: {destination.distance_ly} LY. "
                f"Casualties onboard - Critical: {incident.casualties.critical}, "
                f"Priority: {incident.casualties.priority}, "
                f"Stable: {incident.casualties.stable}."
            ),
            "flight_log": flight_log
        }

    def mark_ready(self) -> None:
        self.status = "READY"