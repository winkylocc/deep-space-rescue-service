from models.destination import Destination
from utils.menu import choose_from_options

DESTINATION_CATALOG = {
    "Kreet": Destination("Kreet", "research_site", 3_000_000, "Outer Rim", "HIGH"),
    "Neebas": Destination("Neebas", "repair_site", 4_500_909, "Far Far Away", "MEDIUM"),
    "Eridan II": Destination(
        "Eridan II", "alpha_space_station", 800_000, "Gas Belt", "MEDIUM"
    ),
    "Muphrid IV": Destination(
        "Muphrid IV", "penitentiary", 54_543_987, "Outer Rim", "HIGH"
    ),
    "Toliman II": Destination(
        "Toliman II", "imperial_outpost", 2_569_098, "Sol Sector", "LOW"
    ),
    "Jemison": Destination(
        "Jemison", "nuclear_waste_processing", 901_593_983, "Mid Rim", "HIGH"
    ),
    "Codos": Destination(
        "Codos", "weapons_manufacturer", 99_453_983, "Sol Sector", "LOW"
    ),
}


def choose_destination_from_catalog() -> Destination:
    """Prompts user to pick a destination"""
    return choose_from_options(
        DESTINATION_CATALOG,
        title="Choose a destination:",
        line_formatter=lambda key, d: (
            f"{d.name} ({d.destination_type}, {d.sector}, "
            f"{d.distance_from_hub_in_km:,} km, danger={d.danger_level})"
        ),
    )
