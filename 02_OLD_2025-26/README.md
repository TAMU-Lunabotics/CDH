# 2025–26 CDH Code — Old Reference

**This folder is an archive of useful CDH code from last season. It is NOT the current 2026–27 robot software.**

The files were extracted from the old monolithic repository `ev-17/TAMU_SEDS_Lunabotics` at commit `e0dd1597553613358bf7c7fd8d3dc7f71578c366` from May 11, 2026.

## Pick What You Want to See

| Folder | What is inside |
|---|---|
| **[01_Drive](01_Drive/)** | Driving the rover with RoboClaw, joystick control, and autonomous left/right motor commands |
| **[02_Excavation](02_Excavation/)** | Pico-based auger, deposit, lift, and auger-encoder control |
| **[03_Sensors](03_Sensors/)** | Camera and ISM330DLC IMU ROS 2 code |
| **[04_Hardware_Tests](04_Hardware_Tests/)** | Small scripts used to test encoders, IMU, RoboClaw, and Spark MAX hardware |
| **[05_Technical_Support](05_Technical_Support/)** | Old ROS package/build metadata and the RoboClaw Python dependency |

## What the Old Robot Used

The code shows these historical interfaces:

| Item | 2025–26 value |
|---|---|
| Main computer | NVIDIA Jetson Orin Nano |
| ROS environment | ROS 2 Humble / Ubuntu 22.04 |
| RoboClaw USB | `/dev/ttyACM0`, 38400 baud |
| RoboClaw UART | `/dev/ttyTHS1`, 38400 baud |
| Pico serial | `/dev/ttyACM1`, 115200 baud |
| IMU | ISM330DLC, I2C address `0x6A`, bus `/dev/i2c-7` |
| Spark MAX test CAN interface | `can1` |
| Operator input | ROS `/joy` |
| Autonomous drive command | `auto_drive` |
| Wheel encoder output | `encoders` |
| Auger angle output | `/auger_angle` |
| IMU output | `/imu/data` |

The old source also referenced an Astra depth camera and Unitree LiDAR integration. Their full drivers were not cleanly contained in the old repository, so they are not copied here.

## What Was Removed

To keep this archive readable, the following were intentionally removed:
- ROS `build/`, `install/`, and `log/` output
- Python caches and compiled binaries
- empty ROS package marker files
- duplicate generated TF diagrams/PDFs
- large third-party firmware bundles and example collections
- GNC material
- repeated legacy documentation
- unrelated files from the old monolithic repository

## Reuse Warning

This code contains old hard-coded device paths, topic names, motor directions, controller mappings, and hardware assumptions. Treat it as a **reference**, not something to run unchanged on the 2026–27 robot.
