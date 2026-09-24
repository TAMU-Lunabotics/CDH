# TAMU Lunabotics — CDH

Command & Data Handling (CDH) software for the Texas A&M Lunabotics team.

## Scope
CDH owns the robot's computing and data infrastructure:
- onboard computing and ROS 2 integration
- hardware/sensor/motor data paths
- subsystem communications and command routing
- logging, telemetry, health/status, and time synchronization
- teleop/autonomy mode handling
- software interfaces between Electrical and GNC

## Current Platform
- NVIDIA Jetson Orin Nano
- ESP32 for recovery/reboot and embedded support
- Ubuntu 22.04
- ROS 2 Humble
- C++ / Python
- PlatformIO / Arduino for ESP32 development

## Repository Layout
```
src/        ROS 2 nodes and hardware interfaces
launch/     system launch files
config/     runtime configuration
tools/      diagnostics and developer utilities
tests/      unit/integration tests
docs/       architecture and interface documentation
```

## Integration
Typical data flow:

```
Electrical / Sensors -> CDH -> GNC -> CDH / Motor Interface -> Actuators
```

CDH standardizes ROS topics/messages, timestamps, units, frames, rates, health flags, logging, and failure behavior.

## Workflow
Develop on feature branches and merge into `main` through pull requests. Keep `main` integration-ready.
