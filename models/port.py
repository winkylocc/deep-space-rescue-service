from dataclasses import dataclass
from typing import Dict


@dataclass
class Port:
    name: str
    distance_from_hub_km: int
    casualty_capacity: Dict[str, int]  # {"critical": 10, "priority": 20, "stable": 40}
    quality_of_care: str              # "A", "B", "C", etc.

    def summary(self) -> str:
        return f"This Port status is"