# Development Setup

**Status: WORKING — 2026–27**

Use one consistent development environment unless the team approves a change.

## Required
- Ubuntu 22.04 (native, dual boot, VM, or WSL2)
- ROS 2 Humble Desktop
- Git + GitHub SSH access
- VS Code with C++ / Python support
- colcon, rosdep, build-essential, CMake
- RViz2 and rqt

## As Needed
- PlatformIO / Arduino tools for ESP32 work
- Wireshark for network debugging
- PlotJuggler for telemetry
- gamepad test/driver utilities
- NVIDIA JetPack only on Jetson hardware

## Verify
```bash
source /opt/ros/humble/setup.bash
ros2 topic list

mkdir -p ~/lunabotics_ws/src
cd ~/lunabotics_ws
colcon build
source install/setup.bash
```

Before hardware work, confirm repo access, ROS 2 build/run, and any required lab/safety access.
