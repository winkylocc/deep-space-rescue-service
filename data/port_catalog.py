from models.port import Port
from utils.menu import choose_from_options

PORT_CATALOG = {
    "Eastman Station": Port("Eastman Station", 6.2, {"critical": 23, "priority": 22, "stable": 0}, "HIGH"),
    "The PITT": Port("The PITT", 11.0, {"critical": 43, "priority": 14, "stable": 0}, "HIGH"),
    "Sacred Heart Station": Port("Sacred Heart Station", 8.8, {"critical": 28, "priority": 21, "stable": 0}, "MEDIUM"),
    "St. Eligius": Port("St. Eligius", 9.5, {"critical": 26, "priority": 13, "stable": 0}, "LOW"),
}

def choose_port_from_catalog() -> Port:
    """Prompts user to pick a port"""
    return choose_from_options(
        PORT_CATALOG,
        title="Choose a port:",
        line_formatter=lambda key, p: (
            f"{p.name} (quality={p.quality_of_care}, {p.distance_from_hub_ly} LY, "
            f"critical={p.casualty_capacity['critical']}, priority={p.casualty_capacity['priority']})"
        ),
    )