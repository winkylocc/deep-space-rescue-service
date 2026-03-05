from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from .incident import Incident
from data.destination_catalog import choose_destination_from_catalog

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
    incident_counter: int = 0

    def summary(self) -> str:
        return f"{self.name}: {len(self.fleet)} vessels registered, {len(self.ports)} ports available"

    def register_vessel(self, vessel: RescueVessel) -> None:
        """Adds a rescue vessel to the hub's fleet"""
        self.fleet.append(vessel)
        print(f"Vessel {vessel.name} registered at {self.name}")

    def register_port(self, port: Port) -> None:
        f"Registers the port"
    def report_incident_from_user_input(self) -> Incident:
        """Prompt user for incident detail"""

        print("Enter a description of the incident")
        incident_description = input("> ").strip()
        print("Enter type")
        incident_type = input("> ").strip()
        while True:
            print("Enter severity (LOW/MEDIUM/HIGH)")
            severity = input("> ").strip()

            if severity in ["LOW", "MEDIUM", "HIGH"]:
                break
            else:
                print("Invalid entry. Please enter LOW, MEDIUM, or HIGH!")
        while True:
            try:
                print("Number of critical casualties")
                critical = int(input("> ").strip())
                print("Number of priority casualites")
                priority = int(input("> ").strip())
                print("Number of stable casualites")
                stable = int(input("> ").strip())
                break
            except ValueError:
                print("Invalid input. Please enter numbers.")
        """Consider details/conflicts about the predefined sites we have"""
        print("Enter the name of the site where this incident has taken place")

        destination = choose_destination_from_catalog()
        self.incident_counter += 1
        incident_id = f"INC-{self.incident_counter:03d}"
        time_reported = datetime.now().strftime("%Y-%m-%dT%H:%M")
        incident = Incident(
            incident_id,
            destination,
            incident_type,
            severity,
            critical,
            priority,
            stable,
            incident_description,
            time_reported
        )
        
        print(f"Incident #{incident_id} reported successfully at {time_reported}")
        

        return incident
    def select_best_vessel(self, incident: Incident) -> Optional[RescueVessel]:
        return f"Select best vessel for this journey"
    def create_mission(self, incident: Incident) -> RescueMission:
        return f"Create initial mission"
    def dispatch(self, mission: RescueMission) -> None:
        return f"Dispatch the vessel to the site"