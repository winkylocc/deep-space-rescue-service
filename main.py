from models import MainHub, Port
from data.port_catalog import PORT_CATALOG
from data.vessel_catalog import VESSEL_CATALOG


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
    hub = MainHub(name="DSRS Main Hub")
    print("This is the ")
    for vessel in VESSEL_CATALOG.values():
        hub.register_vessel(vessel)

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

            vessel = hub.select_best_vessel(incident)

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