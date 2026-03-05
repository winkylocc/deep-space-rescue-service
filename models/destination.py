from dataclasses import dataclass

@dataclass
class Destination:
    name: str
    destination_type: str
    distance_from_hub_in_km: int
    sector: str
    danger_level: str
    
    def summary(self) -> str:
        return (
            f"{self.name} is a {self.destination_type} in sector {self.sector}, "
            f"{self.distance_from_hub_in_km:,} km from the hub (danger={self.danger_level})."
        )