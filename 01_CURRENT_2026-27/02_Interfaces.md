# CDH Interfaces — 2026–27

**Status: CURRENT DOCUMENT / INTERFACE BASELINE IN DEVELOPMENT**

CDH is the integration layer between robot hardware, Electrical, GNC, Communications, and the operator.

## Important
No 2025–26 topic name, message schema, transport choice, or motor-command interface is automatically current. For example, `/cmd_vel` is a common/legacy pattern, **not an approved 2026–27 contract unless baselined here**.

## Current Logical Data Flow
```
Sensors / Controllers
        |
        v
 CDH Hardware / Transport Layer
        |
        v
   ROS 2 Interfaces
        |
        +----> GNC
        |
        +----> Telemetry / Ground Station
        |
        <---- Commands / Mode / Safety State
        |
        v
 Actuator / Motor Interface
```

## Interface Contract
Every cross-team interface must define:
- status: CURRENT / WORKING / LEGACY
- owning and consuming subteams
- ROS 2 topic/service/action and message type
- units and valid ranges
- coordinate frame, where applicable
- timestamp source / clock assumptions
- expected update rate and latency
- health/status indication
- timeout and stale-data behavior
- failure / safe-state behavior

Use SI units unless explicitly documented otherwise.

## 2026–27 Baseline Table
| Interface | Producer | Consumer | Status | Notes |
|---|---|---|---|---|
| Sensor data -> GNC | CDH | GNC | WORKING | Exact topics/messages TBD |
| GNC motion command -> CDH | GNC | CDH | WORKING | Exact command contract TBD |
| Robot health/telemetry -> ground | CDH | Operator | WORKING | Must support competition monitoring |
| Operator teleop/mode -> robot | Ground station | CDH/GNC | WORKING | Must clearly separate manual vs autonomy state |
| Obstacle/map/path visualization | GNC via CDH | Mission Control | CURRENT REQUIREMENT | 2026–27 travel-autonomy review requires real-time visualization |

## Ownership Boundary
Electrical powers and wires the system. GNC decides where/how the robot should move. CDH owns the data/command/telemetry/comms/software-integration path that connects them.
