from models import MainHub, RescueVessel, Port

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
        "SSH Joy"
    ]
    hub = MainHub(name="DSRS Main Hub")

    v1 = RescueVessel(vessel_fleet[0])
    v2 = RescueVessel(vessel_fleet[1])
        
    hub.register_vessel(v1)
    hub.register_vessel(v2)

    print(hub.summary())

    for name in vessel_fleet:
        hub.register_vessel(RescueVessel(name))

    incident = hub.report_incident_from_user_input()
    print(incident.summary())

if __name__ == "__main__":
    main()