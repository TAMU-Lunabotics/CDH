# Legacy Dependencies and Assumptions — 2025–26

This file documents dependencies visible in the imported CDH code. It does **not** declare them as current 2026–27 selections.

## Hardware / OS interfaces

| Interface | Historical value |
|---|---|
| RoboClaw USB serial | `/dev/ttyACM0`, 38400 baud |
| RoboClaw Jetson UART | `/dev/ttyTHS1`, 38400 baud |
| Pico serial | `/dev/ttyACM1`, 115200 baud |
| ISM330DLC I2C | `/dev/i2c-7`, address `0x6A` |
| SPARK MAX SocketCAN | `can1` |

## Software dependencies visible in the source

ROS 2 code uses `rclpy`, `rclcpp`, `sensor_msgs`, `std_msgs`, launch/launch_ros, and `cv_bridge`. Standalone scripts also use pyserial, smbus2, python-can, OpenCV, and NumPy.

The imported `vendor/roboclaw/roboclaw_3.py` file is retained because the historical CDH drive nodes import it directly. Its provenance/license was not documented in the old repository, so verify upstream licensing before promoting it into current-season code.

## Referenced but not imported as source

- **Astra camera:** the old ROS workspace contains a gitlink named `ros2_astra_camera` at commit `f7e71d9ce806e788cb48d8580aac2c778fba4214`. The driver itself is not copied into this archive.
- **Unitree LiDAR:** the old top-level README documents `unitree_lidar_ros2` and topics `/unilidar/cloud` and `/unilidar/imu`, but a clean source package was not present under the audited `ros2_ws/src` tree.
- **candleLight / gs_usb:** old CAN experiments included firmware archives/binaries and a copied Linux `gs_usb.c` driver. Those upstream/vendor artifacts were excluded; only the team-facing Spark MAX scripts were retained.

Before reuse, replace hard-coded device paths, verify topic conventions, and confirm current hardware ownership/interfaces with Electrical and GNC.
