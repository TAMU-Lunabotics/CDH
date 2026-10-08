"""Optional direct RoboClaw driver. Default disarmed; stop on stale input."""
import importlib
import math
import sys
from .drive_guard import DriveGuard


def main(args=None):
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    from std_msgs.msg import Bool, Int32MultiArray

    class RoboClawNode(Node):
        def __init__(self):
            super().__init__('lunabotics_roboclaw_guarded')
            for name, value in (
                ('hardware_enable', False), ('serial_port', ''),
                ('roboclaw_library_dir', ''), ('baud', 38400), ('address', 128),
                ('wheel_track_m', 0.0), ('full_power_speed_mps', 0.0),
                ('left_sign', 0), ('right_sign', 0), ('swap_channels', False),
                ('encoder_left_sign', 0), ('encoder_right_sign', 0)):
                self.declare_parameter(name, value)
            p = lambda key: self.get_parameter(key).value
            self.guard = None
            self.device = None
            self.estop = True
            self.estop_time = -1e9
            self.address = int(p('address'))
            self.swap = bool(p('swap_channels'))
            self.encoder_left_sign = int(p('encoder_left_sign'))
            self.encoder_right_sign = int(p('encoder_right_sign'))
            if bool(p('hardware_enable')):
                try:
                    self.guard = DriveGuard(float(p('wheel_track_m')),
                        float(p('full_power_speed_mps')),
                        int(p('left_sign')), int(p('right_sign')))
                    if self.encoder_left_sign not in (-1,1) or self.encoder_right_sign not in (-1,1):
                        raise ValueError('calibrate both encoder signs before enabling')
                    if not p('serial_port') or not p('roboclaw_library_dir'):
                        raise ValueError('explicit serial port and driver location required')
                    sys.path.insert(0, str(p('roboclaw_library_dir')))
                    roboclaw = importlib.import_module('roboclaw_3')
                    self.device = roboclaw.Roboclaw(str(p('serial_port')), int(p('baud')))
                    if not self.device.Open():
                        raise RuntimeError('RoboClaw serial open failed')
                    self._write(0, 0)
                except Exception as exc:
                    self.guard = None
                    self.device = None
                    self.get_logger().error(f'Hardware inhibited: {exc}')
            else:
                self.get_logger().warn('RoboClaw driver disarmed; no serial port opened')
            self.create_subscription(Twist, '/autonomy/cmd_vel', self.command, 10)
            self.create_subscription(Bool, '/safety/estop', self.on_estop, 10)
            self.encoders = self.create_publisher(Int32MultiArray, '/drive/encoders', 10)
            self.create_timer(0.05, self.step)

        def now(self):
            return self.get_clock().now().nanoseconds * 1e-9

        def command(self, msg):
            if self.guard:
                try:
                    self.guard.accept(float(msg.linear.x), float(msg.angular.z), self.now())
                except ValueError:
                    self._write(0, 0)
                    self.guard.invalidate()

        def on_estop(self, msg):
            self.estop, self.estop_time = bool(msg.data), self.now()
            if self.estop:
                self._write(0, 0)

        def _write(self, left, right):
            if self.device is None:
                return
            if self.swap:
                left, right = right, left
            try:
                for motor, value in (('M1', left), ('M2', right)):
                    op = 'Forward' if value >= 0 else 'Backward'
                    getattr(self.device, op+motor)(self.address, abs(value))
            except Exception as exc:
                self.get_logger().error(f'RoboClaw write failed: {exc}')
                self.guard = None

        def step(self):
            if self.device is None:
                return
            left, right = (self.guard.output(self.now(), self.estop, self.estop_time)
                           if self.guard else (0, 0))
            self._write(left, right)
            try:
                one, two = self.device.ReadEncM1(self.address), self.device.ReadEncM2(self.address)
                if one[0] and two[0]:
                    left,right = int(one[1]),int(two[1])
                    if self.swap:
                        left,right = right,left
                    msg = Int32MultiArray()
                    msg.data = [self.encoder_left_sign*left,
                                self.encoder_right_sign*right]
                    self.encoders.publish(msg)
            except Exception as exc:
                self.get_logger().error(f'RoboClaw encoder failure: {exc}', throttle_duration_sec=3.0)

        def destroy_node(self):
            self._write(0, 0)
            super().destroy_node()

    rclpy.init(args=args)
    node = RoboClawNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
