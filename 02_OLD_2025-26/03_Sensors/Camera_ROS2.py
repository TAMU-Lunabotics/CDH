import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2
from cv_bridge import CvBridge
import cv2
import numpy as np


# Topic Names
RGB_TOPIC   = '/camera/color/image_raw'
DEPTH_TOPIC = '/camera/depth/image_raw'
IR_TOPIC    = '/camera/ir/image_raw'
CLOUD_TOPIC = '/camera/depth/points'

class CameraSubscriberNode(Node):
    def __init__(self):
        super().__init__('camera_subscriber')

        self.bridge = CvBridge()

        # RGB subscriber
        self.create_subscription(
            Image, RGB_TOPIC, self.rgb_callback, 10)

        # Depth subscriber
        self.create_subscription(
            Image, DEPTH_TOPIC, self.depth_callback, 10)

        # IR subscriber
        self.create_subscription(
            Image, IR_TOPIC, self.ir_callback, 10)

        # Pointcloud subscriber
        self.create_subscription(
            PointCloud2, CLOUD_TOPIC, self.cloud_callback, 10)

        self.get_logger().info("Camera subscriber node started")

    def rgb_callback(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        # — do your processing here —
        h, w = frame.shape[:2]
        self.get_logger().debug(f"RGB  → {w}x{h}")

    def depth_callback(self, msg: Image):
        # depth values are in millimeters (16-bit)
        frame = self.bridge.imgmsg_to_cv2(msg, '16UC1')

        # example: read center pixel distance
        h, w = frame.shape
        cx, cy = w // 2, h // 2
        dist_mm = frame[cy, cx]
        dist_m  = dist_mm / 1000.0

        self.get_logger().info(f"Depth → center: {dist_m:.2f} m")

    def ir_callback(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, 'mono16')

        # convert to 8-bit for easier processing
        frame_8bit = cv2.normalize(
            frame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        h, w = frame_8bit.shape
        self.get_logger().debug(f"IR   → {w}x{h}")

    def cloud_callback(self, msg: PointCloud2):
        # basic info — processing pointclouds needs pcl or open3d
        self.get_logger().debug(
            f"Cloud → {msg.width * msg.height} points  "
            f"| frame: {msg.header.frame_id}")


def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriberNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()