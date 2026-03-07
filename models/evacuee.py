from dataclasses import dataclass


@dataclass
class Evacuee:
    name: str
    severity: int
    destination_port: str

    #  summary
    def summary(self) -> str:
        return f"Evacuee: {self.name} | Severity: {self.severity} | Destination Port: {self.destination_port}"


"""# data update method
    def update_destination(self, new_port: str) -> None:
        if new_port not in PORTS:
            raise ValueError("Port not recognized.")
        self.destination_port = new_port

# input method with input() + try/except + reprompt
    @classmethod
    def build_from_user_input(cls) -> "Evacuee":
        while True:
            name = input("Enter evacuee name: ").strip()

            try:
                severity = int(input("Enter casualty severity (1-6): "))

                print("\nAvailable Ports (max severity they can treat):")
                for p, info in PORTS.items():
                    print(f" - {p} (up to {info['max_severity']})")

                destination = input("Choose destination port: ").strip()

                if severity < 1 or severity > 6:
                    raise ValueError("Severity must be between 1 and 6.")
                if destination not in PORTS:
                    raise ValueError("Port not recognized.")
                if severity > PORTS[destination]["max_severity"]:
                    raise ValueError(
                        f"{destination} cannot treat severity {severity}. "
                        f"Max is {PORTS[destination]['max_severity']}."
                    )

                return cls(name=name, severity=severity, destination_port=destination)

            except ValueError as e:
                print(f"\nInvalid input: {e}")
                print("Reprompting... try again.\n")"""
