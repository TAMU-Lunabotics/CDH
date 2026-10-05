import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import sys

sys.path.append('/home/lunabotics/TAMU_SEDS_Lunabotics/roboclaw')
from roboclaw_3 import Roboclaw

ADDRESS = 0x80


MAX_SPEED = 127
MIN_SPEED = -127


class AutoTankDriveNode(Node):
    def __init__(self):
        super().__init__('auto_tank_drive')

        self.rc = Roboclaw("/dev/ttyACM0", 38400)
        if not self.rc.Open():
            self.get_logger().error("Failed to open RoboClaw!")
            return

        self.get_logger().info("RoboClaw connected!")

        
        # TOPIC NAME — change here if needed
        AUTO_DRIVE_TOPIC = 'auto_drive'
        

        # subscriber — expects Int32MultiArray: [left, right]
        self.sub = self.create_subscription(
            Int32MultiArray,
            AUTO_DRIVE_TOPIC,           # ← topic name used here
            self.drive_callback,
            10)

        # encoder publisher
        self.enc_pub = self.create_publisher(
            Int32MultiArray, 'encoders', 10)

        self.create_timer(0.1, self.publish_encoders)

        self.get_logger().info(
            f"Listening on '{AUTO_DRIVE_TOPIC}' | "
            f"Speed range: [{MIN_SPEED}, {MAX_SPEED}]")

    def drive_callback(self, msg: Int32MultiArray):
        if len(msg.data) < 2:
            self.get_logger().warn(
                "Expected [right, left] in msg.data, got fewer values")
            return

        left  = -int(msg.data[0])
        right = -int(msg.data[1])

        # clamp to valid range
        right  = max(MIN_SPEED, min(MAX_SPEED, right))
        left = max(MIN_SPEED, min(MAX_SPEED, left))

        self.drive(right, left)
        self.get_logger().info(f'CMD → L: {-left}  R: {-right}')

    def drive(self, left: int, right: int):
        # left motor
        if left >= 0:
            self.rc.ForwardM1(ADDRESS, left)
        else:
            self.rc.BackwardM1(ADDRESS, -left)

        # right motor
        if right >= 0:
            self.rc.ForwardM2(ADDRESS, right)
        else:
            self.rc.BackwardM2(ADDRESS, -right)

    def publish_encoders(self):
        enc1 = self.rc.ReadEncM1(ADDRESS)
        enc2 = self.rc.ReadEncM2(ADDRESS)

        if enc1[0] and enc2[0]:
            msg = Int32MultiArray()
            msg.data = [enc1[1], -enc2[1]]
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
    node = AutoTankDriveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()