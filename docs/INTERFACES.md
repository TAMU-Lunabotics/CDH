# CDH Interfaces

CDH is the integration layer between robot hardware, Electrical, and GNC.

## Current Data Flow
```
Sensors / Controllers
        |
        v
   CDH Hardware Nodes
        |
        v
 ROS 2 Topics / Status
        |
        v
        GNC
        |
        v
 Motion Command (current pattern: /cmd_vel)
        |
        v
 CDH Motor Interface -> Actuators
```

## Interface Rules
Every cross-team interface should define:
- ROS 2 topic/service/action and message type
- units and valid ranges
- coordinate frame
- timestamp source
- expected update rate
- health/status indication
- timeout and failure behavior

Use SI units unless the interface document explicitly states otherwise.

## CDH Responsibilities
- hardware drivers and transport
- ROS 2 message publication/subscription
- command routing
- launch/configuration
- logging and replay support
- time synchronization
- telemetry and system health
- teleop/autonomy mode plumbing

Keep hardware-specific details inside CDH so GNC can consume stable software interfaces.
