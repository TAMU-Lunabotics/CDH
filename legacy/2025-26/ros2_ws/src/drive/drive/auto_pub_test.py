import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray




AUTO_DRIVE_TOPIC = 'auto_drive'


class AutoDriveTestPublisher(Node):
    def __init__(self):
        super().__init__('auto_drive_test_publisher')

        self.pub = self.create_publisher(
            Int32MultiArray, AUTO_DRIVE_TOPIC, 10)   # ← topic name used here

        self.get_logger().info(
            f"Publishing to '{AUTO_DRIVE_TOPIC}'\n"
            "Enter: right left   (e.g.  64 64  or  -127 127)\n"
            "       'stop'       → sends 0 0\n"
            "       'q'          → quit\n")

    def run(self):
        while rclpy.ok():
            try:
                raw = input("left right > ").strip().lower()
            except EOFError:
                break

            if raw == 'q':
                break

            if raw == 'stop':
                left, right = 0, 0

            else:
                parts = raw.split()
                if len(parts) != 2:
                    print("  ✗  Enter two integers, e.g:  64 -64")
                    continue

                try:
                    left  = int(parts[0])
                    right = int(parts[1])
                except ValueError:
                    print("  ✗  Values must be integers")
                    continue

                # warn but still clamp
                if not (-127 <= left <= 127) or not (-127 <= right <= 127):
                    print(f"  ⚠  Values clamped to [-127, 127]")
                    left  = max(-127, min(127, left))
                    right = max(-127, min(127, right))

            msg = Int32MultiArray()
            msg.data = [left, right]
            self.pub.publish(msg)
            print(f"  Sent → L: {left}  R: {right}")


def main(args=None):
    rclpy.init(args=args)
    node = AutoDriveTestPublisher()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        # send stop before quitting
        stop_msg = Int32MultiArray()
        stop_msg.data = [0, 0]
        node.pub.publish(stop_msg)
        print("\nStop sent. Shutting down.")
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()