from dataclasses import dataclass, field

@dataclass
class Port:
    name: str
    distance_from_hub_ly: float
    casualty_capacity: dict
    quality_of_care: str
    status: str = "OPERATIONAL"
    sector: str = "Mid Rim"
    current_load: dict = field(default_factory=lambda: {
        "critical": 0,
        "priority": 0,
        "stable": 0
    })

    def available_capacity(self) -> dict:
        return {
            triage: self.casualty_capacity[triage] - self.current_load[triage]
            for triage in ["critical", "priority", "stable"]
        }

    def receive_casualties(self, critical: int, priority: int, stable: int) -> None:
        self.current_load["critical"] += critical
        self.current_load["priority"] += priority
        self.current_load["stable"] += stable

    def treat_casualties(self, hours: int) -> dict:
        treated = {
            "critical": min(self.current_load["critical"], hours * 1),
            "priority": min(self.current_load["priority"], hours * 2),
            "stable": min(self.current_load["stable"], hours * 4),
        }

        self.current_load["critical"] -= treated["critical"]
        self.current_load["priority"] -= treated["priority"]
        self.current_load["stable"] -= treated["stable"]

        return treated