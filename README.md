Download Instructions

Windows (Git Bash)
```
git clone https://github.com/winkylocc/deep-space-rescue-service.git
cd deep-space-rescue-service
python --version
python -m main
```

Mac Terminal

```
git clone https://github.com/winkylocc/deep-space-rescue-service.git
cd deep-space-rescue-service
python3 --version
python3 -m main
```

If you don't have Python, they install Python 3 from python.org.

---

## Visual architecture diagram for Deep Space Rescue Service

```mermaid
flowchart TD
  A[Incident occurs at Destination] --> B[MainHub receives report]
  B --> C{Select best RescueVessel}
  C -->|Feasible vessel found| D[Create RescueMission]
  D --> E[Dispatch vessel]
  E --> F[On-scene rescue]
  F --> G[Transport survivors]
  G --> H[Port / Medical facility]
  C -->|No feasible vessel| X[Abort mission / escalate]
```

### Entity View

```mermaid
classDiagram
  class MainHub {
    +name: str
    +fleet: List[RescueVessel]
    +ports: List[Port]
    +register_vessel()
    +select_best_vessel()
    +create_mission()
    +dispatch()
  }

  class RescueVessel {
    +name: str
    +fuel_level_pct: float
    +max_range_km: int
    +speed_km_s: float
    +evac_capacity: int
    +med_bays: int
    +status: str
    +can_reach()
    +has_capacity_for()
  }

  class Destination {
    +name: str
    +destination_type: str
    +distance_from_hub_in_km: int
    +sector: str
    +danger_level: str
  }

  class Incident {
    +incident_id: str
    +incident_type: str
    +severity: str
    +casualties_critical: int
    +casualties_priority: int
    +casualties_stable: int
    +total_casualties()
  }

  class RescueMission {
    +mission_id: str
    +status: str
    +plan()
    +launch()
    +abort()
  }

  class Port {
    +name: str
    +distance_from_hub_in_km: int
    +quality_of_care: str
  }

  MainHub "1" o-- "*" RescueVessel
  MainHub "1" o-- "*" Port
  Incident "*" --> "1" Destination
  RescueMission "*" --> "1" Incident
  RescueMission "*" --> "0..1" RescueVessel
  RescueMission "*" --> "0..1" Port
```
