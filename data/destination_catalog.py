from models.destination import Destination

DESTINATION_CATALOG = {
    "Kreet": Destination(
        name="Kreet",
        destination_type="Frontier Outpost",
        distance_ly=2.5,
        sector="Outer Rim",
        danger_level="MEDIUM",
        description="A remote frontier station with unstable life-support systems."
    ),
    "Titan Outpost": Destination(
        name="Titan Outpost",
        destination_type="Mining Colony",
        distance_ly=4.5,
        sector="Saturn Reach",
        danger_level="HIGH",
        description="A hazardous mining outpost known for tunnel collapses and methane fires."
    ),
    "Europa Research Colony": Destination(
        name="Europa Research Colony",
        destination_type="Research Site",
        distance_ly=9.2,
        sector="Jovian Frontier",
        danger_level="HIGH",
        description="A deep-space research colony operating under extreme ice-world conditions."
    ),
    "Vallis Marineris Station": Destination(
        name="Vallis Marineris Station",
        destination_type="Civilian Settlement",
        distance_ly=6.8,
        sector="Mars Corridor",
        danger_level="MEDIUM",
        description="A major canyon settlement with heavy civilian and cargo traffic."
    ),
}


def choose_destination_from_catalog() -> Destination:
    import random
    return random.choice(list(DESTINATION_CATALOG.values()))