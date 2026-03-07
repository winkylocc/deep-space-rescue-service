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

    # Removed summary() for now.
    def register_vessel(self, vessel: RescueVessel) -> None:
        """Adds a rescue vessel to the hub's fleet"""
        self.fleet.append(vessel)

    def register_port(self, port: Port) -> None:
        """Registers the port"""
        self.ports.append(port)
    
    def get_total_available_capacity(self) -> dict:
        totals = {"critical": 0, "priority": 0, "stable": 0}

        for port in self.ports:
            for triage in ["critical", "priority", "stable"]:
                available = port.casualty_capacity[triage] - port.current_load[triage]
                totals[triage] += available

        return totals

    def assign_ports_for_casualties(self, incident: Incident) -> list:
        print("\nBegin casualty placement.")
        print("Select a port to receive casualties. You can choose multiple ports until all are placed.")

        remaining = {
            "critical": incident.casualties_critical,
            "priority": incident.casualties_priority,
            "stable": incident.casualties_stable,
        }

        assignments = []

        while any(v > 0 for v in remaining.values()):
            print("\nThe following casualties need placement:")
            print(
                f"Critical: {remaining['critical']}, "
                f"Priority: {remaining['priority']}, "
                f"Stable: {remaining['stable']}"
            )

            print("\nAvailable ports:")
            available_ports = []

            for i, port in enumerate(self.ports, start=1):
                available = port.available_capacity()

                if any(v > 0 for v in available.values()):
                    available_ports.append(port)
                    print(
                        f"{len(available_ports)}) {port.name} "
                        f"[critical={available['critical']}, "
                        f"priority={available['priority']}, "
                        f"stable={available['stable']}]"
                    )

            if not available_ports:
                print("These people have exhausted our bed space!")
                break

            try:
                choice = int(input("> Select a port number: ").strip())
                chosen_port = available_ports[choice - 1]
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")
                continue

            assigned = {}

            for triage in ["critical", "priority", "stable"]:
                available = (
                    chosen_port.casualty_capacity[triage]
                    - chosen_port.current_load[triage]
                )
                assigned[triage] = min(remaining[triage], available)

            if all(v == 0 for v in assigned.values()):
                print(f"{chosen_port.name} has no space left for these casualties.")
                continue

            for triage in ["critical", "priority", "stable"]:
                chosen_port.current_load[triage] += assigned[triage]
                remaining[triage] -= assigned[triage]
            available = chosen_port.available_capacity()
            assignments.append(
                (
                    chosen_port,
                    assigned["critical"],
                    assigned["priority"],
                    assigned["stable"],
                )
            )

        leftover = [f"{v} {k}" for k, v in remaining.items() if v > 0]
        if leftover:
            print(f"WARNING: {', '.join(leftover)} casualties could not be placed.")

        return assignments

    def report_incident_from_user_input(self) -> Incident:
        """Prompt user for incident detail"""

        print("Enter a description of the incident")
        incident_description = input("> ").strip()
        print("Enter destination type")
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
                print("Number of priority casualties")
                priority = int(input("> ").strip())
                print("Number of stable casualties")
                stable = int(input("> ").strip())

                available = self.get_total_available_capacity()

                if critical > available["critical"]:
                    print(f"Not enough critical capacity. Available: {available['critical']}")
                    continue
                if priority > available["priority"]:
                    print(f"Not enough priority capacity. Available: {available['priority']}")
                    continue
                if stable > available["stable"]:
                    print(f"Not enough stable capacity. Available: {available['stable']}")
                    continue

                break

            except ValueError:
                print("Invalid input. Please enter numbers.")

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
        print("\nSelect a vessel to dispatch to the incident.")

        available = [v for v in self.fleet if v.status == "READY"]

        if not available:
            print("No vessels are currently available.")
            return None

        print("\nAvailable vessels:")
        for i, vessel in enumerate(available, start=1):
            print(
                f"{i}) {vessel.name} "
                f"[C={vessel.critical_capacity}, P={vessel.priority_capacity}, S={vessel.stable_capacity}, "
                f"range={vessel.max_range_full_ly} LY]"
            )

        while True:
            try:
                choice = int(input("> Select a vessel number: ").strip())
                if 1 <= choice <= len(available):
                    selected = available[choice - 1]
                    selected.status = "DISPATCHED"
                    print(f"\n{selected.name} dispatched to incident {incident.incident_id}.")
                    return selected
                print(f"Please enter a number between 1 and {len(available)}.")
            except ValueError:
                print("Invalid input. Please enter a whole number (ex: 1).")
    def create_mission(self, incident: Incident) -> RescueMission:
        return f"Create initial mission"
    def dispatch(self, mission: RescueMission) -> None:
        return f"Dispatch the vessel to the site"