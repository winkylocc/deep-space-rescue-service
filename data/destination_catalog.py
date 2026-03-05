from models.destination import Destination

DESTINATION_CATALOG = {
    "Kreet": Destination("Kreet", "research_site", 3_000_000, "Outer Rim", "HIGH"),
    "Neebas": Destination("Neebas", "repair_site", 4_500_909, "Far Far Away", "MEDIUM"),
    "Eridan II": Destination("Eridan II", "alpha_space_station", 800_000, "Gas Belt", "MEDIUM"),
    "Muphrid IV": Destination("Muphrid IV", "penitentiary", 54_543_987, "Outer Rim", "EXTREMELEY_HIGH"),
    "Toliman II": Destination("Toliman II", "imperial_outpost", 2_569_098, "Sol Sector", "LOW"),
    "Jemison": Destination("Jemison", "nuclear_waste_processing", 901_593_983, "Mid Rim", "HIGH"),
    "Codos": Destination("Codos", "weapons_manufactorer", 99_453_983, "Sol Sector", "LOW")
}

def choose_destination_from_catalog() -> Destination:
    """Prompts user to pick a destination"""
    names = list(DESTINATION_CATALOG.keys())

    while True:
        print("\nChoose a destination:")
        for i, name in enumerate(names, start=1):
            d = DESTINATION_CATALOG[name]
            print(f"{i} {d.name} ({d.destination_type}, {d.sector}, {d.distance_from_hub_in_km:,} km, danger={d.danger_level})")
        try:
            choice = int(input("> ").strip())
            if 1 <= choice <= len(names):
                return DESTINATION_CATALOG[names[choice - 1]]
            print(f"Please enter a number between 1 and {len(names)}.")
        except ValueError:
            print("Invalid input. Please enter a whole number (ex: 1).")