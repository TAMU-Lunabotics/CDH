"""Guarded Pico interface matching recovered auto_pico.py's CSV protocol.

The recovered bridge is a deleted build copy; verify the deployed firmware
and independent limit/RPM feedback before opening the serial port.
"""
import math
from .tool_guard import ToolGuard,pico_packet
from .safety import SafetyLatch


def main(args=None):
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Bool,Float32,String
    from std_srvs.srv import Trigger

    class PicoNode(Node):
        def __init__(self):
            super().__init__('lunabotics_pico_guarded')
            for name,value in (('hardware_enable',False),('protocol_confirmed',False),
                ('serial_port',''),('lift_down_sign',0),('lift_speed',0.0),
                ('min_rpm',1.0)):
                self.declare_parameter(name,value)
            p = lambda name: self.get_parameter(name).value
            self.guard,self.serial = None,None
            self.latch = SafetyLatch()
            self.estop,self.estop_time = True,-1e9
            self.upper,self.upper_time = False,-1e9
            self.lower,self.lower_time = False,-1e9
            self.dig_rpm,self.dig_time = 0.0,-1e9
            self.dump_rpm,self.dump_time = 0.0,-1e9
            if p('hardware_enable') and p('protocol_confirmed'):
                try:
                    self.guard = ToolGuard(int(p('lift_down_sign')),
                        float(p('lift_speed')),min_rpm=float(p('min_rpm')))
                    if not p('serial_port'):
                        raise ValueError('explicit stable Pico serial path required')
                    import serial
                    self.serial = serial.Serial(str(p('serial_port')),115200,timeout=.05)
                    self._packet((0,0,0))
                except Exception as exc:
                    self.guard = None
                    if self.serial:
                        self.serial.close()
                        self.serial = None
                    self.get_logger().error(f'Pico inhibited: {exc}')
            else:
                self.get_logger().warn('Pico port closed: protocol and hardware disabled')
            self.status = self.create_publisher(String,'/actuator/status',10)
            self.create_service(Trigger,'/tool_guard/reset',self.reset)
            self.angle = self.create_publisher(Float32,'/encoder/angle',10)
            self.create_subscription(String,'/autonomy/tool_command',self.command,10)
            self.create_subscription(Bool,'/safety/estop',self.on_estop,10)
            self.create_subscription(Bool,'/actuator/upper_limit',self.on_upper,10)
            self.create_subscription(Bool,'/actuator/lower_limit',self.on_lower,10)
            self.create_subscription(Float32,'/actuator/dig_rpm',self.on_dig_rpm,10)
            self.create_subscription(Float32,'/actuator/dump_rpm',self.on_dump_rpm,10)
            self.create_timer(.05,self.step)

        def reset(self,request,response):
            if self.guard and self.serial and self.latch.reset(self.now(),
                    self.estop,self.estop_time):
                self.guard.accept('stop',self.now())
                response.success,response.message = True,'inhibit cleared; fresh command required'
            else:
                response.success,response.message = False,'hardware or safety input not ready'
            return response

        def now(self):
            return self.get_clock().now().nanoseconds*1e-9

        def command(self,msg):
            if self.guard:
                try:
                    self.guard.accept(msg.data,self.now())
                except ValueError:
                    self._packet((0,0,0))
                    self.latch.trip('invalid_command')
                    self.guard = None

        def on_estop(self,msg):
            self.estop,self.estop_time = bool(msg.data),self.now()
            if self.estop:
                self.latch.trip('estop')
                self._packet((0,0,0))

        def on_upper(self,msg):
            self.upper,self.upper_time = bool(msg.data),self.now()

        def on_lower(self,msg):
            self.lower,self.lower_time = bool(msg.data),self.now()

        def on_dig_rpm(self,msg):
            self.dig_rpm,self.dig_time = float(msg.data),self.now()

        def on_dump_rpm(self,msg):
            self.dump_rpm,self.dump_time = float(msg.data),self.now()

        def _packet(self,speeds):
            if self.serial is None:
                return
            try:
                self.serial.write(pico_packet(speeds))
            except Exception as exc:
                self.get_logger().error(f'Pico write failed: {exc}')
                self.latch.trip('serial_write_failed')
                self.guard = None

        def read_telemetry(self):
            if self.serial is None:
                return
            try:
                for _ in range(20):
                    if not self.serial.in_waiting:
                        break
                    line = self.serial.readline().decode('ascii','replace').strip()
                    if line.startswith('ENC:') and line[4:] != 'NO_SIGNAL':
                        try:
                            value = float(line[4:])
                            if math.isfinite(value):
                                out = Float32()
                                out.data = value
                                self.angle.publish(out)
                        except ValueError:
                            pass
                    elif line.startswith('ERR:'):
                        self.get_logger().error(f'Pico error: {line[4:]}')
                        self.latch.trip('pico_error')
                        self.guard = None
                        self._packet((0,0,0))
            except Exception as exc:
                self.get_logger().error(f'Pico read failed: {exc}')
                self.latch.trip('serial_read_failed')
                self.guard = None

        def step(self):
            self.read_telemetry()
            packet,state = ((0,0,0),'fault')
            if self.guard and self.serial and self.latch.armed:
                packet,state = self.guard.output(self.now(),self.estop,self.estop_time,
                    self.upper,self.upper_time,self.lower,self.lower_time,
                    self.dig_rpm,self.dig_time,self.dump_rpm,self.dump_time)
                if state == 'fault':
                    self.latch.trip('tool_feedback_or_timeout')
                    packet = (0,0,0)
            self._packet(packet)
            status = String()
            status.data = state
            self.status.publish(status)

        def destroy_node(self):
            self._packet((0,0,0))
            if self.serial:
                self.serial.close()
            super().destroy_node()

    rclpy.init(args=args)
    node = PicoNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
