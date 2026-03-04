from models import MainHub, RescueVessel, Destination, Incident, Port

def main():
    hub = MainHub(name="DSRS Main Hub")

    v1 = RescueVessel("Ann Perkins", 90, 5_000_000, 25.0, 24, 4, 10_000)
    v2 = RescueVessel("Carla", 60, 1_200_000, 18.0, 4, 1, 2_000)

    hub.register_vessel(v1)
    hub.register_vessel(v2)

    dest = Destination("Nevarro", "station", 3_000_000, "Outer Rim", "HIGH")
    inc = Incident("INC-001", dest, "reactor_malfunction", "HIGH", 2, 6, 10, "2187-03-03T18:30")

    print(v1.summary())
    print(dest.summary())
    print(inc.summary())

if __name__ == "__main__":
    main()