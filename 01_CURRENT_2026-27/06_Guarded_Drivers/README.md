# Guarded drive and tool candidate

**Status: WORKING — 2026–27.** These ROS 2 Humble drivers remain disarmed with the launch defaults. The 2025–26 Jetson backup and CDH archive provided the RoboClaw/Pico protocol examples. They do not prove deployed firmware, motor signs, sensor calibration, or current-season hardware selection.

The RoboClaw node subscribes to `/autonomy/cmd_vel` and `/safety/estop`. The Pico node subscribes to `/autonomy/tool_command`, E-stop, upper/lower limit switches and measured dig/dump RPM. The old Pico bridge sends `dump,dig,pivot` CSV at 115200 baud; the first two fields are Boolean and pivot is formatted to four decimal places. The guarded node also publishes serial `ENC:<angle>` on `/encoder/angle` without treating it as a lift limit or auger RPM.

The drive node publishes `/drive/encoders`; the tool node publishes `/actuator/status`. Command and E-stop messages expire after 250 ms. Both nodes now start latched, latch on an asserted E-stop and command/feedback faults, and require explicit `/drive_guard/reset` and `/tool_guard/reset` Trigger calls after a fresh E-stop release. Reset invalidates the prior drive command. An independent physical E-stop and device-level watchdog are still required because software on the Jetson cannot stop a driver after computer or ROS failure.

Build with `colcon build --base-paths 01_CURRENT_2026-27/06_Guarded_Drivers --packages-select cdh_actuator_guard`. Run pure tests in this directory with `python3 -m unittest discover -s tests -q`. The launch is `ros2 launch cdh_actuator_guard guarded_drivers.launch.py` and opens no ports by default.

Before enabling a port, check current firmware, exclusive motor ownership, physical E-stop, actual wheel track, top safe speed, channel order, motor and encoder signs, lift direction, both limit switches, and independent RPM feedback. Provide a stable serial-by-id path for each device. The 2025–26 drive launch must not run alongside this package. See the [GNC working interface proposal](https://github.com/TAMU-Lunabotics/GNC-2027/pull/1) until GNC/CDH approve a common baseline.
