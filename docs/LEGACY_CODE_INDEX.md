# 2025–26 CDH Legacy Code Index

**Status: historical reference only.** The imported code below came from `ev-17/TAMU_SEDS_Lunabotics` at commit `e0dd1597553613358bf7c7fd8d3dc7f71578c366` (2026-05-11).

## Imported CDH code

| Legacy area | Destination | What it tells us |
|---|---|---|
| Drive/autonomy bridge | `legacy/2025-26/ros2_ws/src/drive/drive/auto_drive.py` | Accepted two motor commands on `auto_drive`, drove RoboClaw, published encoders |
| Drive test publisher | `legacy/2025-26/ros2_ws/src/drive/drive/auto_pub_test.py` | Manual test source for `auto_drive` |
| Game-controller drive | `legacy/2025-26/ros2_ws/src/drive/drive/tank_drive.py` | `Joy` axes mapped to left/right RoboClaw motors over USB |
| UART drive variant | `legacy/2025-26/ros2_ws/src/drive/drive/tank_drive_uart.py` | Same drive path using Jetson UART |
| Pico excavation interface | `legacy/2025-26/ros2_ws/src/drive/drive/pico_drive.py` | `/joy` buttons mapped to auger/deposit/lift serial commands |
| Pico + auger encoder | `legacy/2025-26/ros2_ws/src/drive/drive/pico_drive_encoders.py` | Added `/auger_angle` publication from serial feedback |
| Camera subscriber | `legacy/2025-26/ros2_ws/src/drive/drive/camera.py` | Historical RGB/depth/IR/point-cloud topic assumptions |
| System launch | `legacy/2025-26/ros2_ws/src/drive/launch/drive.launch.py` | Started Pico plus USB/UART RoboClaw nodes |
| IMU ROS publishers | `legacy/2025-26/ros2_ws/src/sensors/src/` | ISM330DLC I2C ingestion and `sensor_msgs/Imu` publication |
| Encoder/IMU/RoboClaw/Spark MAX tools | `legacy/2025-26/tools/` | Bring-up and hardware-debug scripts |
| TF graph | `legacy/2025-26/docs/tf_frames_2026-05-11.gv` | Late-season transform topology reference |

## Important historical interface details

| Item | Historical behavior |
|---|---|
| Autonomous drive command | `Int32MultiArray` on `auto_drive`; nominal range -127 to 127 |
| Drive encoder output | `Int32MultiArray` on `encoders` |
| Operator input | `sensor_msgs/Joy` on `/joy` |
| IMU | ISM330DLC at I2C address `0x6A`, Jetson bus `/dev/i2c-7` |
| IMU ROS output | `/imu/data`, frame `imu_link` |
| Pico excavation serial | `/dev/ttyACM1` at 115200 baud |
| RoboClaw USB | `/dev/ttyACM0` at 38400 baud |
| RoboClaw UART | `/dev/ttyTHS1` at 38400 baud |
| Camera | Astra-style RGB/depth/IR/point-cloud topics |
| LiDAR reference | `/unilidar/cloud`, `/unilidar/imu` documented, driver source not cleanly present |

## Excluded from migration

Generated build products, logs, caches, compiled binaries, repeated generated PDFs, GNC content, and bulk third-party firmware/example trees were intentionally excluded. This keeps the CDH organization repository focused on team-facing source and technical information.

## Reuse rule

Do not copy these files into current `src/` unchanged. Any promoted component should first be reviewed for current hardware, ROS interfaces, safety behavior, hard-coded paths, error handling, and ownership boundaries.
