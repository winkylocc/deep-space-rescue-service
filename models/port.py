from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Port:
    name: str
    distance_from_hub_ly: float
    casualty_capacity: Dict[str, int]  
    quality_of_care: str  # "HIGH", "MEDIUM", "LOW"
    current_load: Dict[str, int] = field(default_factory=lambda: {"critical": 0, "priority": 0, "stable": 0})
  

    def summary(self) -> str:
        return (
            f"{self.name} is {self.distance_from_hub_ly} LY from the hub, "
            f"quality of care: {self.quality_of_care}, "
            f"capacity: critical={self.casualty_capacity['critical']}, priority={self.casualty_capacity['priority']}."
        )