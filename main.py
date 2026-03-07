from models import MainHub, RescueVessel, Port
from data.port_catalog import PORT_CATALOG


def show_intro():
    print("\n====================================")
    print("  Deep Space Rescue Service (DSRS)")
    print("====================================")
    print("Welcome to the DSRS Command Console.")
    print("This system coordinates rescue vessels")
    print("and medical ports across the sector.")
    print()
    print("You may report incidents and assign")
    print("casualties to available ports.")
    print()


def show_menu():
    print("\nSelect an option:")
    print("1. Report a new incident")
    print("2. Exit")


def main():
    vessel_fleet = [
        "SSH Perkins",
        "SSH Carla",
        "SSH Dana",
        "SSH Jackie",
        "SSH Joy",
        "SSH Ratched",
        "SSH Pomfrey",
        "SSH Focker",
        "SSH Wilkes",
        "SSH Hotlips",
        "SSH Joy",
    ]
    hub = MainHub(name="DSRS Main Hub")
    print("This is the ")
    for name in vessel_fleet:
        hub.register_vessel(RescueVessel(name))

    for port in PORT_CATALOG.values():
        hub.register_port(port)

    show_intro()

    while True:
        show_menu()
        choice = input("> ").strip()

        if choice == "1":
            incident = hub.report_incident_from_user_input()

            print("\nIncident recorded:")
            print(incident.summary())

            assignments = hub.assign_ports_for_casualties(incident)

            for port, critical, priority, stable in assignments:
                available = port.available_capacity()

                print(
                    f"\n{port.name} received "
                    f"{critical} critical, {priority} priority, {stable} stable evacuees."
                )

                print(
                    f"{port.name} remaining capacity -> "
                    f"critical={available['critical']}, "
                    f"priority={available['priority']}, "
                    f"stable={available['stable']}"
                )

        elif choice == "2":
            print("\nShutting down DSRS Command Console.")
            break

        else:
            print("Invalid option. Please choose 1 or 2.")


if __name__ == "__main__":
    main()
