# TAMU Lunabotics — CDH (2026–27)

**Current development repository for the 2026–27 NASA Lunabotics season.**

Command & Data Handling (CDH) owns the software/integration layer that makes robot hardware, autonomy, operators, and competition communications work together.

> **Version rule:** 2025–26 and 2024–25 designs are historical references only. They are not current 2026–27 architecture unless explicitly promoted through a current design decision.

## 2026–27 Scope
- onboard computing and ROS 2 bring-up
- hardware/sensor/motor data paths
- command routing and subsystem interfaces
- telemetry, logging, timing, health/status
- teleoperation/autonomy mode plumbing
- ground-station/operator tooling
- integration support for Electrical and GNC

## Current Working Development Baseline
As of September 2026:
- Ubuntu 22.04
- ROS 2 Humble
- C++ / Python
- GitHub + colcon workflow
- PlatformIO / Arduino tooling where ESP32 development is required

The 2025–26 Jetson Orin Nano, ESP32 recovery controller, Dear PyGui ground station, game-controller teleop, and related hardware/software choices are **inherited baseline references**, not automatically current-season selections.

## Repository Layout
```
src/        current 2026–27 ROS 2 nodes / integration code
launch/     current system launch files
config/     current runtime configuration
tools/      diagnostics and developer utilities
tests/      unit / integration tests
docs/       architecture, interfaces, requirements, decisions
legacy/     historical code retained only for reference
```

## Read First
- [Development setup](docs/SETUP.md)
- [Status & versioning](docs/STATUS_AND_VERSIONING.md)
- [2026–27 competition constraints](docs/COMPETITION_2026-27.md)
- [Interfaces](docs/INTERFACES.md)
- [Interface questions](docs/INTERFACE_QUESTIONS.md)
- [2025–26 legacy baseline](docs/LEGACY_2025-26.md)
- [2025–26 legacy code index](docs/LEGACY_CODE_INDEX.md)
- [Decision log](docs/DECISIONS.md)

## Workflow
Develop on short-lived branches and merge through pull requests. Keep `main` representative of the **current 2026–27 system**, not a mixture of current and legacy implementations.
