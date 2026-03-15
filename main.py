from models import MainHub
from data.port_catalog import PORT_CATALOG
from data.vessel_catalog import VESSEL_CATALOG
from models.rescue_vessel import RescueVessel
from map_view import draw_intro_screen, draw_map


def simulate_rescue_launches(hub: MainHub):
    ready_vessels = [v for v in hub.fleet if v.status == "READY"]

    if len(ready_vessels) < 2:
        print("Need at least 2 READY vessels of ready status.")
        return

    print("\n=== RESCUE LAUNCH SIMULATION ===")

    incident1 = hub.generate_random_incident()
    log1 = RescueVessel.schedule_rescue_launch(ready_vessels[0], incident1)
    print(log1["flight_message"])

    incident2 = hub.generate_random_incident()
    log2 = RescueVessel.schedule_rescue_launch(ready_vessels[1], incident2)
    print(log2["flight_message"])

    print("=== END SIMULATION ===")


def main():
    hub = MainHub(name="DSRS Main Hub")

    for vessel in VESSEL_CATALOG.values():
        hub.register_vessel(vessel)

    for port in PORT_CATALOG.values():
        hub.register_port(port)

    # desired startup sequence:
    # intro -> map -> console
    draw_intro_screen()
    draw_map(hub, selected_vessel=None)

    loop_counter = 0
    next_auto_incident_at = 1  # testing: trigger fast

    while True:
        hub.expire_incoming_incident_if_needed()

        print(f"\n=== {hub.name} ===")
        print(f"Hub State: {hub.hub_state}")

        if hub.hub_state == "INCOMING_INCIDENT" and hub.current_incoming_incident:
            print("\n*** INCOMING INCIDENT ***")
            print(hub.current_incoming_incident.summary())
            print("1) Accept incident")
            print("2) View incident details")
            print("3) Ignore for now")
            print("4) Simulate rescue launches")
            print("5) Exit")

            choice = input("> ").strip()

            if choice == "1":
                incident = hub.accept_incoming_incident()

                if incident:
                    selected_vessel = hub.select_best_vessel(incident)

                    if selected_vessel:
                        draw_map(hub, selected_vessel=selected_vessel)

                        launch_result = selected_vessel.launch_rescue(incident)

                        print("\n=== MISSION RESULT ===")
                        print(launch_result["message"])

                        if launch_result["success"]:
                            print(launch_result["flight_log"]["flight_message"])
                            print("======================\n")
                            hub.assign_ports_for_casualties(incident)
                            hub.clear_incoming_incident()
                        else:
                            print("======================\n")

            elif choice == "2":
                print(hub.current_incoming_incident.details())

            elif choice == "3":
                print("Incoming incident left pending for now.")

            elif choice == "4":
                simulate_rescue_launches(hub)

            elif choice == "5":
                break

            else:
                print("Invalid option.")

        else:
            print("1) Report manual incident")
            print("2) Show vessels")
            print("3) Run rescue launch simulation")
            print("4) Exit")

            choice = input("> ").strip()

            if choice == "1":
                incident = hub.report_incident_from_user_input()
                selected_vessel = hub.select_best_vessel(incident)

                if selected_vessel:
                    draw_map(hub, selected_vessel=selected_vessel)

                    launch_result = selected_vessel.launch_rescue(incident)

                    print("\n=== MISSION RESULT ===")
                    print(launch_result["message"])

                    if launch_result["success"]:
                        print(launch_result["flight_log"]["flight_message"])
                        print("======================\n")
                        hub.assign_ports_for_casualties(incident)
                    else:
                        print("======================\n")

            elif choice == "2":
                for vessel in hub.fleet:
                    print(vessel.summary())

            elif choice == "3":
                simulate_rescue_launches(hub)

            elif choice == "4":
                break

            else:
                print("Invalid option.")

            loop_counter += 1
            if loop_counter >= next_auto_incident_at and hub.hub_state == "IDLE":
                incident = hub.activate_random_incoming_incident()
                if incident:
                    print("\n*** INCOMING INCIDENT ***")
                    print(incident.summary())
                    print("Manual incident entry is now disabled.")

                loop_counter = 0
                next_auto_incident_at = 4


if __name__ == "__main__":
    main()