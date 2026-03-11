from models.destination import Destination
from utils.menu import choose_from_options
import random

DESTINATION_CATALOG = {
    "Kreet": Destination(
        "Kreet",
        "research_site",
        3_000_000,
        "Outer Rim",
        "HIGH",
        "Rocky desert world"
    ),
    "Vallis Marineris Station": Destination(
        "Vallis Marineris Station",
        "colony",
        1_200_000,
        "Mars Sector",
        "MEDIUM",
        "Canyon settlement"
    ),
    "Titan Outpost": Destination(
        "Titan Outpost",
        "mining_outpost",
        5_800_000,
        "Outer Rim",
        "HIGH",
        "Methane ice plains"
    ),
    "Europa Research Colony": Destination(
        "Europa Research Colony",
        "research_colony",
        4_900_000,
        "Jovian Sector",
        "EXTREME",
        "Frozen ocean crust"
    ),
}

def choose_destination_from_catalog() -> Destination:
    return random.choice(list(DESTINATION_CATALOG.values()))