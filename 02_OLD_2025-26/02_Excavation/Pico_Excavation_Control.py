

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
import serial
import time

#  BUTTON MAPPING
BTN_A         = 0   # Deposit unclog
BTN_B         = 1   # Lower lift
BTN_X         = 2   # Lift up
BTN_Y         = 3   # Deposit spin
BTN_LB        = 4   # Dig (auger +)
BTN_RB        = 5   # Undig (auger -)
BTN_STOP      = 6   # Back/Select = STOP ALL

DEBOUNCE_SEC  = 0.05  # 50ms debounce between commands


class PicoController(Node):
    def __init__(self):
        super().__init__('pico_controller')

        self.serial = None
        self.connect_pico()

        self.last_cmd = {
            'auger':   None,
            'deposit': None,
            'lift':    None,
        }

        # Track last time each motor got a NEW command
        self.last_send_time = {
            'auger':   0.0,
            'deposit': 0.0,
            'lift':    0.0,
        }

        # Queue size 1 = always process latest message, drop old ones
        self.joy_sub = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            1
        )

        self.get_logger().info('Pico Controller Node Started')
        self.get_logger().info('Listening to /joy topic...')

    # Pico connections makes sure pico is in t ACM1 if not change
    def connect_pico(self):
        pico_port = '/dev/ttyACM1'
        try:
            self.serial = serial.Serial(pico_port, 115200, timeout=1)
            time.sleep(2)
            self.get_logger().info(f'Connected to Pico on {pico_port}')
        except Exception as e:
            self.get_logger().error(f'Failed to open port {pico_port}: {e}')
            self.serial = None

    # sedn command to pico via serial 
    def send_cmd(self, cmd, motor_key):
        now = time.monotonic()

        # Drop if same command already running
        if self.last_cmd[motor_key] == cmd:
            return

        # Drop if sent too recently (debounce)
        if now - self.last_send_time[motor_key] < DEBOUNCE_SEC:
            return

        if self.serial and self.serial.is_open:
            try:
                self.serial.write(f'{cmd}\n'.encode())
                self.last_cmd[motor_key] = cmd
                self.last_send_time[motor_key] = now
                self.get_logger().info(f'Sent: {cmd}')
            except Exception as e:
                self.get_logger().error(f'Serial write error: {e}')
        else:
            self.get_logger().warn('Serial not connected!')

    def send_stop_all(self):
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(b'stop\n')
                self.last_cmd = {'auger': None, 'deposit': None, 'lift': None}
                self.last_send_time = {'auger': 0.0, 'deposit': 0.0, 'lift': 0.0}
                self.get_logger().info('Sent: stop (ALL)')
            except Exception as e:
                self.get_logger().error(f'Serial write error: {e}')

    # joy node callback
    def joy_callback(self, msg: Joy):
        buttons = msg.buttons

        # Stop
        if buttons[BTN_STOP]:
            self.send_stop_all()
            return

        #  Auguer / pwm 2
        if buttons[BTN_LB] and not buttons[BTN_RB]:
            self.send_cmd('dig', 'auger')
        elif buttons[BTN_RB] and not buttons[BTN_LB]:
            self.send_cmd('undig', 'auger')
        else:
            self.send_cmd('stop_auger', 'auger')

        # Dep pwm 3
        if buttons[BTN_Y] and not buttons[BTN_A]:
            self.send_cmd('deposit_spin', 'deposit')
        elif buttons[BTN_A] and not buttons[BTN_Y]:
            self.send_cmd('deposit_unclog', 'deposit')
        else:
            self.send_cmd('stop_deposit', 'deposit')

        # lift PWM1
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
        node.get_logger().info('Shutting down...')
        node.send_stop_all()
    finally:
        if node.serial and node.serial.is_open:
            node.serial.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()