# CDH Legacy Code Snapshot — 2025–26

> **LEGACY / REFERENCE ONLY.** This directory is not the 2026–27 software baseline.

This is the CDH-relevant subset extracted from the former monolithic repository `ev-17/TAMU_SEDS_Lunabotics`.

- Source commit: `e0dd1597553613358bf7c7fd8d3dc7f71578c366`
- Source commit date: 2026-05-11
- Imported into the CDH organization archive: 2026-10-05

## What is preserved

| Area | Preserved material | Historical purpose |
|---|---|---|
| ROS 2 drive integration | `ros2_ws/src/drive/` | Teleop, autonomous drive command routing, RoboClaw drive, Pico excavation control, camera subscriptions |
| ROS 2 sensor integration | `ros2_ws/src/sensors/` | ISM330DLC IMU acquisition and ROS 2 publication |
| Encoder diagnostics | `tools/encoder/` | Direct encoder/RoboClaw serial checks |
| IMU diagnostics | `tools/imu/` | Direct Jetson I2C checks for the ISM330DLC |
| Spark MAX experiments | `tools/sparkmax/` | CAN and Pico/PWM motor-control experiments |
| RoboClaw diagnostics | `tools/roboclaw/` | Motor, encoder, and UART/baud checks |
| RoboClaw dependency snapshot | `vendor/roboclaw/roboclaw_3.py` | Python library imported by the historical drive nodes |
| TF snapshot | `docs/tf_frames_2026-05-11.gv` | Late-season frame-tree reference |

## Historical interfaces visible in the code

- `auto_drive` topic: two signed motor commands, nominally in `[-127, 127]`
- `encoders` topic: left/right RoboClaw encoder counts
- `/joy`: game-controller input for drive and Pico excavation controls
- `/auger_angle`: Pico-reported auger angle
- `/imu/data`: ISM330DLC accelerometer/gyro data
- Camera topics: `/camera/color/image_raw`, `/camera/depth/image_raw`, `/camera/ir/image_raw`, `/camera/depth/points`

Historical device assumptions include `/dev/ttyACM0`, `/dev/ttyACM1`, `/dev/ttyTHS1`, SocketCAN `can1`, and Jetson I2C bus `/dev/i2c-7`.

## Intentionally not copied

The old repository contained large amounts of generated or third-party material that should not live in the CDH source archive:

- ROS/colcon `build/`, `install/`, and `log/`
- Python `__pycache__` and `.pyc`
- compiled binaries such as `a.out`
- candleLight firmware binaries/archives and its full vendor bundle
- the copied Linux `gs_usb.c` driver source
- duplicate RoboClaw vendor example programs
- repeated generated TF PDFs
- the GNC repository/gitlink
- unrelated non-CDH material

See `docs/LEGACY_CODE_INDEX.md` at the repository root for the migration index and reuse cautions.
