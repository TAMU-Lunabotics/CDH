import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32MultiArray
import sys

sys.path.append('/home/lunabotics/TAMU_SEDS_Lunabotics/roboclaw')
from roboclaw_3 import Roboclaw

ADDRESS = 0x80

class TankDriveNode(Node):
    def __init__(self):
        super().__init__('tank_drive')

        self.rc = Roboclaw("/dev/ttyTHS1", 38400)
        if not self.rc.Open():
            self.get_logger().error("Failed to open RoboClaw!")
            return

        self.get_logger().info("RoboClaw connected!")

        # joystick subscriber
        self.sub = self.create_subscription(
            Joy, 'joy', self.joy_callback, 10)

        # encoder publisher
        self.enc_pub = self.create_publisher(Int32MultiArray, 'encoders', 10)

        # read encoders at 10Hz
        self.create_timer(0.1, self.publish_encoders)

    def joy_callback(self, msg: Joy):
        left  = msg.axes[1]
        right = msg.axes[4]

        left_speed  = int(left  * 127)
        right_speed = int(right * 127)

        self.drive(left_speed, right_speed)
        self.get_logger().info(f'L: {left_speed}  R: {right_speed}')

    def drive(self, left: int, right: int):
        if left >= 0:
            self.rc.ForwardM1(ADDRESS, left)
        else:
            self.rc.BackwardM1(ADDRESS, -left)

        if right >= 0:
            self.rc.ForwardM2(ADDRESS, right)
        else:
            self.rc.BackwardM2(ADDRESS, -right)

    def publish_encoders(self):
        # roboclaw_3 returns (status, value) tuples
        enc1 = self.rc.ReadEncM1(ADDRESS)
        enc2 = self.rc.ReadEncM2(ADDRESS)

        # enc1 = (1, value) on success, (0,) on failure
        if enc1[0] and enc2[0]:
            msg = Int32MultiArray()
            msg.data = [enc1[1], enc2[1]]
            self.enc_pub.publish(msg)
            self.get_logger().debug(f'Enc1: {enc1[1]}  Enc2: {enc2[1]}')
        else:
            self.get_logger().warn('Encoder read failed')

    def stop(self):
        self.rc.ForwardM1(ADDRESS, 0)
        self.rc.ForwardM2(ADDRESS, 0)

    def destroy_node(self):
        self.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = TankDriveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()