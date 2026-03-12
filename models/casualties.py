from dataclasses import dataclass

@dataclass
class Casualties:
    critical: int
    priority: int
    stable: int

    def total(self) -> int:
        return self.critical + self.priority + self.stable
