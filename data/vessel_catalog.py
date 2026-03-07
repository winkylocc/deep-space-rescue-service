from models.rescue_vessel import RescueVessel
from utils.menu import choose_from_options

VESSEL_CATALOG = {
    "SSH Hotlips": RescueVessel("SSH Hotlips", critical_capacity=4, priority_capacity=4, stable_capacity=8, max_range_full_ly=5.0),
    "SSH Perkins": RescueVessel("SSH Perkins", critical_capacity=8, priority_capacity=10, stable_capacity=12, max_range_full_ly=5.7),
    "SSH Pomfrey": RescueVessel("SSH Pomfrey", critical_capacity=20, priority_capacity=6, stable_capacity=6, max_range_full_ly=6.7),
    "SSH Focker": RescueVessel("SSH Focker", critical_capacity=5, priority_capacity=10, stable_capacity=30, max_range_full_ly=7.7),
    "SSH Jackie": RescueVessel("SSH Jackie", critical_capacity=13, priority_capacity=11, stable_capacity=29, max_range_full_ly=8.7),
    "SSH Dana": RescueVessel("SSH Dana", critical_capacity=16, priority_capacity=34, stable_capacity=14, max_range_full_ly=9.6),
    "SSH Carla": RescueVessel("SSH Carla", critical_capacity=23, priority_capacity=44, stable_capacity=12, max_range_full_ly=10.8),
    "SSH Joy": RescueVessel("SSH Joy", critical_capacity=15, priority_capacity=20, stable_capacity=48, max_range_full_ly=11.8),
    "SSH Wilkes": RescueVessel("SSH Wilkes", critical_capacity=54, priority_capacity=25, stable_capacity=20, max_range_full_ly=13.9),
    "SSH Ratched": RescueVessel("SSH Ratched", critical_capacity=42, priority_capacity=39, stable_capacity=24, max_range_full_ly=16.0),
}


def choose_vessel_from_catalog() -> RescueVessel:
    """Prompts user to pick a vessel"""
    return choose_from_options(
        VESSEL_CATALOG,
        title="Choose a vessel:",
        line_formatter=lambda key, v: (
            f"{v.name} (C={v.critical_capacity}, P={v.priority_capacity}, S={v.stable_capacity}, "
            f"range={v.max_range_full_ly} LY)"
        ),
    )