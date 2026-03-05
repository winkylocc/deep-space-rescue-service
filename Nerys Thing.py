from dataclasses import dataclass

# Matt's Group Data 

MAIN_HUB = {
    "name": "MAIN HUB (Celestial Medical Array)",
    "capacity": {"critical": 200, "priority": 250, "stable": 400},
}

# Planets: casualties (critical/priority/stable), distance to hub, nearest port + distance
PLANETS = {
    "Toliman II": {
        "casualties": {"critical": 10, "priority": 26, "stable": 27},
        "dist_hub_ly": 4.3,
        "nearest_port": None,
        "dist_nearest_port_ly": None,
    },
    "Jemison": {
        "casualties": {"critical": 29, "priority": 35, "stable": 59},
        "dist_hub_ly": 4.7,
        "nearest_port": None,
        "dist_nearest_port_ly": None,
    },
    "Codos": {
        "casualties": {"critical": 35, "priority": 39, "stable": 53},
        "dist_hub_ly": 8.9,
        "nearest_port": "Eastman Station",
        "dist_nearest_port_ly": 2.7,
    },
    "Kreet": {
        "casualties": {"critical": 46, "priority": 44, "stable": 42},
        "dist_hub_ly": 15.2,
        "nearest_port": "Eastman Station",
        "dist_nearest_port_ly": 6.3,
    },
    "Eridani II": {
        "casualties": {"critical": 36, "priority": 31, "stable": 55},
        "dist_hub_ly": 16.3,
        "nearest_port": "The PITT",
        "dist_nearest_port_ly": 5.3,
    },
    "Neebas": {
        "casualties": {"critical": 33, "priority": 49, "stable": 48},
        "dist_hub_ly": 22.1,
        "nearest_port": "The PITT",
        "dist_nearest_port_ly": 11.1,
    },
    "Muphrid IV": {
        "casualties": {"critical": 29, "priority": 33, "stable": 44},
        "dist_hub_ly": 27.2,
        "nearest_port": "St. Eligius",
        "dist_nearest_port_ly": 8.9,
    },
}

# Ports: max triage severity range + capacity (critical/priority/stable) + distance to hub
PORTS = {
    "The PITT": {
        "max_severity": 5,
        "capacity": {"critical": 57, "priority": 43, "stable": 14},
        "dist_hub_ly": 11.0,
    },
    "Eastman Station": {
        "max_severity": 4,
        "capacity": {"critical": 45, "priority": 23, "stable": 22},
        "dist_hub_ly": 6.2,
    },
    "Sacred Heart Station": {
        "max_severity": 3,
        "capacity": {"critical": 49, "priority": 28, "stable": 21},
        "dist_hub_ly": 8.8,
    },
    "St. Eligius": {
        "max_severity": 2,
        "capacity": {"critical": 39, "priority": 26, "stable": 13},
        "dist_hub_ly": 9.5,  # note: diagram mentions distance to Sacred Heart
    },
}

# Ships: total capacity + capacity breakdown (critical/priority/stable) + fuel (LY empty/full)
SHIPS = {
    "SSH HOTLIPS": {"total": 16, "cps": (4, 4, 8), "fuel_empty_full_ly": (6.2, 5.0)},
    "SSH PERKINS": {"total": 30, "cps": (8, 10, 12), "fuel_empty_full_ly": (7.1, 5.7)},
    "SSH POMFREY": {"total": 32, "cps": (20, 6, 6), "fuel_empty_full_ly": (8.3, 6.7)},
    "SSH FOCKER": {"total": 45, "cps": (5, 10, 30), "fuel_empty_full_ly": (9.6, 7.7)},
    "SSH JACKIE": {"total": 53, "cps": (13, 11, 29), "fuel_empty_full_ly": (10.9, 8.7)},
    "SSH DANA": {"total": 64, "cps": (16, 34, 14), "fuel_empty_full_ly": (12.0, 9.6)},
    "SSH CARLA": {"total": 79, "cps": (23, 44, 12), "fuel_empty_full_ly": (13.5, 10.8)},
    "SSH JOY": {"total": 83, "cps": (15, 20, 48), "fuel_empty_full_ly": (14.8, 11.8)},
    "SSH WILKES": {"total": 99, "cps": (54, 25, 20), "fuel_empty_full_ly": (17.3, 13.0)},
    "SSH RATCHED": {"total": 105, "cps": (42, 39, 24), "fuel_empty_full_ly": (20.0, 16.0)},
}

# DAY 2. 3 attributes, 3 methods

@dataclass
class Evacuee:
    name: str
    severity: int          
    destination_port: str  

#  summary
    def summary(self) -> str:
        return f"Evacuee: {self.name} | Severity: {self.severity} | Destination Port: {self.destination_port}"

# data update method
    def update_destination(self, new_port: str) -> None:
        if new_port not in PORTS:
            raise ValueError("Port not recognized.")
        self.destination_port = new_port

# input method with input() + try/except + reprompt
    @classmethod
    def build_from_user_input(cls) -> "Evacuee":
        while True:
            name = input("Enter evacuee name: ").strip()

            try:
                severity = int(input("Enter casualty severity (1-6): "))

                print("\nAvailable Ports (max severity they can treat):")
                for p, info in PORTS.items():
                    print(f" - {p} (up to {info['max_severity']})")

                destination = input("Choose destination port: ").strip()

                if severity < 1 or severity > 6:
                    raise ValueError("Severity must be between 1 and 6.")
                if destination not in PORTS:
                    raise ValueError("Port not recognized.")
                if severity > PORTS[destination]["max_severity"]:
                    raise ValueError(
                        f"{destination} cannot treat severity {severity}. "
                        f"Max is {PORTS[destination]['max_severity']}."
                    )

                return cls(name=name, severity=severity, destination_port=destination)

            except ValueError as e:
                print(f"\nInvalid input: {e}")
                print("Reprompting... try again.\n")



def print_hub():
    cap = MAIN_HUB["capacity"]
    print(f"{MAIN_HUB['name']}")
    print(f"Capacity -> Critical: {cap['critical']} | Priority: {cap['priority']} | Stable: {cap['stable']}\n")


def print_ports():
    print("=== PORTS (4) ===")
    for name, info in PORTS.items():
        cap = info["capacity"]
        print(
            f"{name} | MaxSeverity: {info['max_severity']} | "
            f"Cap C:{cap['critical']} P:{cap['priority']} S:{cap['stable']} | "
            f"DistHub: {info['dist_hub_ly']} LY"
        )
    print()


def print_ships():
    print("=== SHIPS (10) ===")
    for name, info in SHIPS.items():
        c, p, s = info["cps"]
        empty_ly, full_ly = info["fuel_empty_full_ly"]
        print(
            f"{name} | TotalCap: {info['total']} (C:{c} P:{p} S:{s}) | "
            f"Fuel(LY) Empty/Full: {empty_ly}/{full_ly}"
        )
    print()


def print_planets():
    print("=== PLANETS (7) ===")
    for name, info in PLANETS.items():
        cas = info["casualties"]
        nearest = info["nearest_port"] if info["nearest_port"] else "N/A"
        ndist = info["dist_nearest_port_ly"] if info["dist_nearest_port_ly"] else "N/A"
        total = cas["critical"] + cas["priority"] + cas["stable"]
        print(
            f"{name} | Casualties C:{cas['critical']} P:{cas['priority']} S:{cas['stable']} (Total:{total}) | "
            f"DistHub: {info['dist_hub_ly']} LY | NearestPort: {nearest} ({ndist} LY)"
        )
    print()



# MAIN Day 2

def total_casualties(planet_info: dict) -> int:
    cas = planet_info["casualties"]
    return cas["critical"] + cas["priority"] + cas["stable"]


def ship_range_loaded(ship_info: dict) -> float:
    """
    Your diagram lists Fuel (LY) Empty/Full. Full is the worst-case (heavier load),
    and it's smaller than empty, so we use FULL as the safe max range.
    """
    empty_ly, full_ly = ship_info["fuel_empty_full_ly"]
    return float(full_ly)


def ships_that_can_reach(distance_ly: float) -> list:
    """Return ship names that can safely reach distance_ly."""
    can = []
    for ship_name, info in SHIPS.items():
        if ship_range_loaded(info) >= distance_ly:
            can.append(ship_name)
    return can


def best_ship_for_mission(distance_ly: float, people_needed: int) -> tuple:
    """
    Choose the "best" ship as:
    1) can reach the distance
    2) has enough capacity (or the largest available if none can carry all)
    3) prefer the smallest ship that still meets the capacity (efficient dispatch)
    Returns: (ship_name, note)
    """
    reachable = []
    for ship_name, info in SHIPS.items():
        if ship_range_loaded(info) >= distance_ly:
            reachable.append((ship_name, info["total"]))

    if not reachable:
        return (None, "No ship can reach this distance with loaded-range limits.")

# ships that can carry everyone in one trip
    one_trip = [(n, cap) for (n, cap) in reachable if cap >= people_needed]

    if one_trip:
# pick smallest ship that still works (efficient)
        one_trip.sort(key=lambda x: x[1])
        ship_name, cap = one_trip[0]
        return (ship_name, f"One trip possible (cap {cap} >= {people_needed}).")

# otherwise pick largest reachable and estimate trips
    reachable.sort(key=lambda x: x[1], reverse=True)
    ship_name, cap = reachable[0]
    trips = (people_needed + cap - 1) // cap  # ceiling division
    return (ship_name, f"Multiple trips needed: ~{trips} trips with cap {cap} for {people_needed}.")


def best_treatment_location(severity: int) -> str:
    """
    Choose the best location for treatment:
    - Prefer the highest-capability port that can treat this severity
    - If none can treat it, send to MAIN HUB (assumed highest care)
    """
    candidates = [(p, info["max_severity"]) for p, info in PORTS.items() if info["max_severity"] >= severity]
    if not candidates:
        return "MAIN HUB"
# pick the port with the highest max severity (best treatment)
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]


def recommend_dispatch_for_planet(planet_name: str, planet_info: dict) -> dict:
    """
    Decide:
    - better route (to nearest port vs to main hub) based on reachability
    - best ship for that route
    - best treatment location for CRITICAL severity (since it's the hardest)
    """
# Use CRITICAL as the deciding severity (hardest to treat)
# treating "critical" as top severity in 1-6 scale
    crit_severity = 6  

    dist_hub = planet_info["dist_hub_ly"]
    nearest_port = planet_info["nearest_port"]
    dist_port = planet_info["dist_nearest_port_ly"]

    people_needed = total_casualties(planet_info)

    # Route A: Planet -> HUB
    ship_hub, note_hub = best_ship_for_mission(dist_hub, people_needed)

    # Route B: Planet -> Nearest Port (if exists)
    ship_port, note_port = (None, "No nearest port listed.")
    if nearest_port and dist_port:
        ship_port, note_port = best_ship_for_mission(dist_port, people_needed)

    # Choose route: prefer nearest port route IF it has a reachable ship AND port can handle criticals
    chosen_route = "HUB"
    chosen_ship = ship_hub
    chosen_note = note_hub
    chosen_dest = "MAIN HUB"

    if nearest_port and dist_port:
        port_can_treat_critical = PORTS[nearest_port]["max_severity"] >= crit_severity
        if ship_port is not None and port_can_treat_critical:
            chosen_route = f"NEAREST PORT ({nearest_port})"
            chosen_ship = ship_port
            chosen_note = note_port
            chosen_dest = nearest_port

#If nearest port can't treat critical, you can still stage there for stabilization,
# but final treatment should go to MAIN HUB .
        elif ship_port is not None and not port_can_treat_critical:
            chosen_route = f"NEAREST PORT ({nearest_port}) then MAIN HUB"
            chosen_ship = ship_port
            chosen_note = note_port + " Port cannot treat critical; transfer to MAIN HUB."
            chosen_dest = "MAIN HUB"

    return {
        "planet": planet_name,
        "people_needed": people_needed,
        "dist_hub_ly": dist_hub,
        "nearest_port": nearest_port if nearest_port else "N/A",
        "dist_nearest_port_ly": dist_port if dist_port else "N/A",
        "recommended_route": chosen_route,
        "recommended_ship": chosen_ship if chosen_ship else "NONE",
        "notes": chosen_note,
        "treatment_destination": chosen_dest,
        "best_port_for_critical": best_treatment_location(6),
    }
if __name__ == "__main__":
    print("\n=== DEEP SPACE RESCUE SERVICE (DAY 2) ===\n")

    print_hub()
    print_ports()
    print_ships()
    print_planets()
    
print("=== DISPATCH RECOMMENDATIONS ===")
for planet_name, info in PLANETS.items():
    rec = recommend_dispatch_for_planet(planet_name, info)
    print(
        f"{rec['planet']} | People:{rec['people_needed']} | Hub:{rec['dist_hub_ly']}LY | "
        f"Nearest:{rec['nearest_port']}({rec['dist_nearest_port_ly']}LY)\n"
        f" -> Route: {rec['recommended_route']}\n"
        f" -> Ship: {rec['recommended_ship']}\n"
        f" -> Treatment: {rec['treatment_destination']}\n"
        f" -> Note: {rec['notes']}\n"
    )

    evacuee_manifest = []

    print("Add evacuees (enter ONE bad input to prove error handling for your screenshot):\n")

    for i in range(3):  
        print(f"--- Evacuee #{i+1} ---")
        evacuee_manifest.append(Evacuee.build_from_user_input())
        print()

    print("\n=== EVACUEE MANIFEST (PRINTED WITH LOOP) ===")
    for evac in evacuee_manifest:
        print(evac.summary())