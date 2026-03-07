"""
VESSEL_CATALOG = {
    "SSH Hotlips": Vessel("SSH Hotlips", 6.2, 5.0, speedneeded, weightneeded, 4, 4, 8),
    "SSH Perkins": Vessel("SSH Perkins", 7.1, 5.7, speedneeded, weightneeded, 8, 10, 12),
    "SSH Pomfrey": Vessel("SSH Pomfrey", 8.3, 6.7, speedneeded, weightneeded, 20, 6, 6),
    "SSH Focker": Vessel("SSH Focker", 9.6, 7.7, speedneeded, weightneeded, 5, 10, 30),
    "SSH Jackie": Vessel("SSH Jackie", 10.9, 8.7, speedneeded, weightneeded, 13, 11, 29),
    "SSH Dana": Vessel("SSH Dana", 12.0, 9.6, speedneeded, weightneeded, 16, 34, 14),
    "SSH Carla": Vessel("SSH Carla", 13.5, 10.8, speedneeded, weightneeded, 23, 44, 12),
    "SSH Joy": Vessel("SSH Joy", 14.8, 11.8, speedneeded, weightneeded, 15, 20, 48),
    "SSH Wilkes": Vessel("SSH Wilkes", 17.3, 13.9, speedneeded, weightneeded, 54, 25, 20),
    "SSH Ratched": Vessel("SSH Ratched", 20.0, 16.0, speedneeded, weightneeded, 42, 39, 24)
}

def choose_vessel_from_catalog() -> Vessel:
    return choose_from_options(
        VESSEL_CATALOG,
        title="Choose a vessel:",
        line_formatter=lambda key, d: (
            f"{v.name} ({v.critical_capacity}, {v.priority_capacity}, {v.stable_capacity},"
            f"{v.distance_from_destination_in_km:,} km, danger={d.danger_level})"
        ),
    )"""
