from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
import random
import time

from .casualties import Casualties
from .incident import Incident
from data.destination_catalog import choose_destination_from_catalog

if TYPE_CHECKING:
    from .rescue_vessel import RescueVessel
    from .port import Port
    from .rescue_mission import RescueMission


@dataclass
class MainHub:
    name: str
    fleet: List[RescueVessel] = field(default_factory=list)
    ports: List[Port] = field(default_factory=list)
    incident_counter: int = 0

    # for future "incoming incident" feature
    hub_state: str = "IDLE"  # IDLE, INCOMING_INCIDENT, ACTIVE_MISSION
    current_incoming_incident: Optional[Incident] = None
    incoming_incident_created_at: Optional[float] = None

    def register_vessel(self, vessel: RescueVessel) -> None:
        """Add a rescue vessel to the hub fleet."""
        self.fleet.append(vessel)

    def register_port(self, port: Port) -> None:
        """Add a port to the hub."""
        self.ports.append(port)

    def create_incident(
        self,
        destination,
        incident_type: str,
        severity: str,
        critical: int,
        priority: int,
        stable: int,
        incident_description: str,  
    ):
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
            time_reported,
        )

        print(f"Incident #{incident_id} reported successfully at {time_reported}")
        return incident


    def assign_ports_for_casualties_with_selector(self, incident, select_port_fn):
        print("\nBegin casualty placement.")
        print("Click a port on the map to place casualties there.")

        remaining = {
            "critical": incident.casualties_critical,
            "priority": incident.casualties_priority,
            "stable": incident.casualties_stable,
        }
        assignments = []

        while any(v > 0 for v in remaining.values()):
            available_ports = []
            for port in self.ports:
                available = port.available_capacity()
                if any(v > 0 for v in available.values()):
                    available_ports.append(port)

            if not available_ports:
                print("WARNING: No more port space available.")
                break

            chosen_port = select_port_fn(remaining, available_ports)
            if chosen_port is None:
                print("Port selection cancelled.")
                break

            assigned = {}
            available = chosen_port.available_capacity()

            for triage in ["critical", "priority", "stable"]:
                assigned[triage] = min(remaining[triage], available[triage])

            if all(v == 0 for v in assigned.values()):
                print(f"{chosen_port.name} has no space left for these casualties.")
                continue

            for triage in ["critical", "priority", "stable"]:
                chosen_port.current_load[triage] += assigned[triage]
                remaining[triage] -= assigned[triage]

            assignments.append(
                (
                    chosen_port,
                    assigned["critical"],
                    assigned["priority"],
                    assigned["stable"],
                )
            )

            print(
                f"{chosen_port.name} received "
                f"{assigned['critical']} critical, "
                f"{assigned['priority']} priority, "
                f"{assigned['stable']} stable casualties."
            )
            print(
                f"{chosen_port.name} remaining capacity -> "
                f"critical={chosen_port.available_capacity()['critical']}, "
                f"priority={chosen_port.available_capacity()['priority']}, "
                f"stable={chosen_port.available_capacity()['stable']}"
            )

        return assignments    

    def get_total_available_capacity(self) -> dict[str, int]:
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
            "critical": incident.casualties.critical,
            "priority": incident.casualties.priority,
            "stable": incident.casualties.stable,
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

            for port in self.ports:
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
                available = chosen_port.casualty_capacity[triage] - chosen_port.current_load[triage]
                assigned[triage] = min(remaining[triage], available)

            if all(v == 0 for v in assigned.values()):
                print(f"{chosen_port.name} has no space left for these casualties.")
                continue

            for triage in ["critical", "priority", "stable"]:
                chosen_port.current_load[triage] += assigned[triage]
                remaining[triage] -= assigned[triage]

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
        """Prompt the user for incident details and create an Incident."""
        if self.hub_state == "INCOMING_INCIDENT":
            raise RuntimeError("Manual incident entry is disabled while an incoming incident is active.")

        print("Enter a description of the incident")
        incident_description = input("> ").strip()

        print("Enter incident type")
        incident_type = input("> ").strip()

        while True:
            print("Enter severity (LOW/MEDIUM/HIGH/EXTREME)")
            severity = input("> ").strip().upper()

            if severity in ["LOW", "MEDIUM", "HIGH", "EXTREME"]:
                break

            print("Invalid entry. Please enter LOW, MEDIUM, HIGH, or EXTREME.")

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
                print("Invalid input. Please enter whole numbers.")

        destination = choose_destination_from_catalog()

        self.incident_counter += 1
        incident_id = f"INC-{self.incident_counter:03d}"
        time_reported = datetime.now().strftime("%Y-%m-%dT%H:%M")

        casualties = Casualties(
            critical=critical,
            priority=priority,
            stable=stable,
        )

        incident = Incident(
            incident_id=incident_id,
            destination=destination,
            incident_type=incident_type,
            severity=severity,
            casualties=casualties,
            description=incident_description,
            time_reported=time_reported,
        )

        print(f"\nIncident #{incident_id} reported successfully at {time_reported}")
        return incident

    def generate_random_incident(self) -> Incident:
        destination = choose_destination_from_catalog()

        incident_types = [
            "Hull breach",
            "Radiation surge",
            "Life support failure",
            "Cryogenic malfunction",
            "Rover crash",
            "Mining collapse",
            "Docking bay fire",
            "Solar flare exposure",
        ]

        descriptions = [
            "Emergency beacon triggered after structural damage.",
            "Medical distress signal indicates multiple injured personnel.",
            "Hazardous environmental conditions have overwhelmed local support systems.",
            "Critical systems failure has left survivors awaiting evacuation.",
        ]

        severities = ["LOW", "MEDIUM", "HIGH", "EXTREME"]

        available = self.get_total_available_capacity()

        critical = random.randint(0, min(4, available["critical"]))
        priority = random.randint(0, min(6, available["priority"]))
        stable = random.randint(1, min(8, available["stable"])) if available["stable"] > 0 else 0

        # ensure at least one casualty somewhere
        if critical == 0 and priority == 0 and stable == 0:
            stable = 1

        casualties = Casualties(
            critical=critical,
            priority=priority,
            stable=stable,
        )

        self.incident_counter += 1
        incident_id = f"INC-{self.incident_counter:03d}"
        time_reported = datetime.now().strftime("%Y-%m-%dT%H:%M")

        return Incident(
            incident_id=incident_id,
            destination=destination,
            incident_type=random.choice(incident_types),
            severity=random.choice(severities),
            casualties=casualties,
            description=random.choice(descriptions),
            time_reported=time_reported,
            expires_in_seconds=random.randint(150, 300),
        )

    def activate_random_incoming_incident(self) -> Optional[Incident]:
        if self.hub_state != "IDLE":
            return None

        incident = self.generate_random_incident()
        self.current_incoming_incident = incident
        self.incoming_incident_created_at = time.time()
        self.hub_state = "INCOMING_INCIDENT"
        return incident

    def accept_incoming_incident(self) -> Optional[Incident]:
        if self.current_incoming_incident is None:
            print("There is no incoming incident to accept.")
            return None

        self.current_incoming_incident.accepted = True
        self.hub_state = "ACTIVE_MISSION"
        print(f"Incoming incident {self.current_incoming_incident.incident_id} accepted.")
        return self.current_incoming_incident

    def incoming_incident_has_expired(self) -> bool:
        if self.current_incoming_incident is None or self.incoming_incident_created_at is None:
            return False

        elapsed = time.time() - self.incoming_incident_created_at
        return elapsed >= self.current_incoming_incident.expires_in_seconds

    def expire_incoming_incident_if_needed(self) -> bool:
        if self.hub_state != "INCOMING_INCIDENT":
            return False

        if self.incoming_incident_has_expired():
            print(
                f"\nIncoming incident {self.current_incoming_incident.incident_id} "
                f"from {self.current_incoming_incident.destination.name} has expired."
            )
            self.clear_incoming_incident()
            return True

        return False

    def clear_incoming_incident(self) -> None:
        self.current_incoming_incident = None
        self.incoming_incident_created_at = None
        self.hub_state = "IDLE" 

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
                f"[C={vessel.critical_capacity}, P={vessel.priority_capacity}, "
                f"S={vessel.stable_capacity}, range={vessel.max_range_full_ly} LY]"
            )

        while True:
            try:
                choice = int(input("> Select a vessel number: ").strip())

                if 1 <= choice <= len(available):
                    selected = available[choice - 1]
                    incident.assigned_vessel = selected

                    print(f"\n{selected.name} dispatched to incident {incident.incident_id}.")
                    return selected

                print(f"Please enter a number between 1 and {len(available)}.")

            except ValueError:
                print("Invalid input. Please enter a whole number.")

    def set_incoming_incident(self, incident: Incident) -> None:
        """Store an auto-generated incoming incident in the hub."""
        self.current_incoming_incident = incident
        self.hub_state = "INCOMING_INCIDENT"

    def create_mission(self, incident: Incident) -> RescueMission:
        raise NotImplementedError("Create initial mission logic goes here.")

    def dispatch(self, mission: RescueMission) -> None:
        raise NotImplementedError("Dispatch logic goes here.")