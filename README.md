Download Instructions
1. Make a new directory and cd to it.

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
### To add code:
Create a Feature Branch
Before making changes, create a new branch from main:

```
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

Example:
```
git checkout -b feature/incident-reporting
```
Make Your Changes

Edit the code, then stage and commit:
```
git add .
git commit -m "Add incident reporting feature"
```
Push the Branch

Push the branch to the remote repository:
```
git push origin feature/your-feature-name
```
Create a Pull Request

Go to the repository on GitHub.

Click Compare & pull request.

Add a description of your changes.

Submit the Pull Request.

The pull reques should be merged into main unless unresolved errors exists.
Examples branch names
```
feature/incident-reporting
feature/vessel-dispatch
feature/user-input-validation
bugfix/incident-import
docs/readme-update
```
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

### ENTITIES

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

  %% Relationships
  MainHub "1" o-- "*" RescueVessel : manages
  MainHub "1" o-- "*" Port : knows

  Incident "0..*" --> "1" Destination : occurs_at

  RescueMission "1" --> "1" Incident : responds_to
  RescueMission "0..1" --> "1" RescueVessel : assigned_vessel
  RescueMission "0..1" --> "1" Port : assigned_port
```
