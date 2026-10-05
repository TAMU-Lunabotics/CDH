#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
import serial
import time
import threading

BTN_A         = 0
BTN_B         = 1
BTN_X         = 2
BTN_Y         = 3
BTN_LB        = 4
BTN_RB        = 5
BTN_STOP      = 6
DEBOUNCE_SEC  = 0.05

class PicoController(Node):
    def __init__(self):
        super().__init__('pico_controller')

        self.serial = None
        self.serial_lock = threading.Lock()
        self.connect_pico()

        self.last_cmd = {'auger': None, 'deposit': None, 'lift': None}
        self.last_send_time = {'auger': 0.0, 'deposit': 0.0, 'lift': 0.0}

        # Encoder publisher
        self.encoder_pub = self.create_publisher(Float32, '/auger_angle', 10)

        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_callback, 1)

        # Read encoder from serial at 20hz
        self.create_timer(0.05, self.read_encoder)

        self.get_logger().info('Pico Controller Started')

    def connect_pico(self):
        pico_port = '/dev/ttyACM1'
        try:
            self.serial = serial.Serial(pico_port, 115200, timeout=1)
            time.sleep(2)
            self.get_logger().info(f'Connected on {pico_port}')
        except Exception as e:
            self.get_logger().error(f'Failed: {e}')
            self.serial = None

    def send_cmd(self, cmd, motor_key):
        now = time.monotonic()
        if self.last_cmd[motor_key] == cmd:
            return
        if now - self.last_send_time[motor_key] < DEBOUNCE_SEC:
            return
        if self.serial and self.serial.is_open:
            with self.serial_lock:
                try:
                    self.serial.write(f'{cmd}\n'.encode())
                    self.last_cmd[motor_key] = cmd
                    self.last_send_time[motor_key] = now
                    self.get_logger().info(f'Sent: {cmd}')
                except Exception as e:
                    self.get_logger().error(f'Write error: {e}')

    def send_stop_all(self):
        if self.serial and self.serial.is_open:
            with self.serial_lock:
                try:
                    self.serial.write(b'stop\n')
                    self.last_cmd = {'auger': None, 'deposit': None, 'lift': None}
                    self.last_send_time = {'auger': 0.0, 'deposit': 0.0, 'lift': 0.0}
                except Exception as e:
                    self.get_logger().error(f'Write error: {e}')

    # read encoder
    def read_encoder(self):
        if self.serial and self.serial.is_open:
            with self.serial_lock:
                try:
                    while self.serial.in_waiting:
                        line = self.serial.readline().decode().strip()
                        if line.startswith("ENC:"):
                            val = line.split(":")[1]
                            if val != "NO_SIGNAL":
                                angle = float(val)
                                msg = Float32()
                                msg.data = angle
                                self.encoder_pub.publish(msg)
                                self.get_logger().info(f'Auger angle: {angle:.2f} deg')
                            else:
                                self.get_logger().warn('Encoder: no signal')
                except Exception as e:
                    self.get_logger().error(f'Encoder read error: {e}')

    def joy_callback(self, msg: Joy):
        buttons = msg.buttons
        if buttons[BTN_STOP]:
            self.send_stop_all()
            return
        if buttons[BTN_LB] and not buttons[BTN_RB]:
            self.send_cmd('dig', 'auger')
        elif buttons[BTN_RB] and not buttons[BTN_LB]:
            self.send_cmd('undig', 'auger')
        else:
            self.send_cmd('stop_auger', 'auger')
        if buttons[BTN_Y] and not buttons[BTN_A]:
            self.send_cmd('deposit_spin', 'deposit')
        elif buttons[BTN_A] and not buttons[BTN_Y]:
            self.send_cmd('deposit_unclog', 'deposit')
        else:
            self.send_cmd('stop_deposit', 'deposit')
        if buttons[BTN_X] and not buttons[BTN_B]:
            self.send_cmd('lift', 'lift')
        elif buttons[BTN_B] and not buttons[BTN_X]:
            self.send_cmd('lower', 'lift')
        else:
            self.send_cmd('stop_lift', 'lift')

def main(args=None):
    rclpy.init(args=args)
    node = PicoController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.send_stop_all()
    finally:
        if node.serial and node.serial.is_open:
            node.serial.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
