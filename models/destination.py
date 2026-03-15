from dataclasses import dataclass


@dataclass
class Destination:
    name: str
    destination_type: str
    distance_ly: float
    sector: str
    danger_level: str
    description: str

    def summary(self) -> str:
        return (
            f"{self.name} is a {self.destination_type} in sector {self.sector}, "
            f"{self.distance_ly} LY from the hub (danger={self.danger_level})."
        )