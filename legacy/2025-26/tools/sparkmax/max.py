import can
import struct
import time

DEVICE_ID   = 1
CAN_CHANNEL = 'can1'
DUTY_CYCLE  = 0.5
RUN_TIME    = 5

# Exact roboRIO heartbeat per FRC CAN spec
# CAN ID 0x01011840 = NI Manufacturer, RobotController type, API ID 0x061
ROBORIO_HEARTBEAT_ID = 0x01011840

# Duty cycle frame
DUTY_CYCLE_ID = 0x02050081  # Device Type=2, Mfr=5, APIClass=0, APIIndex=2, DevID=1

def send_heartbeat(bus, enabled=True):
    # Byte 0 bit 0 = robot enabled, bit 4 = teleop mode
    data = bytearray(8)
    data[0] = 0x11 if enabled else 0x00  # enabled + teleop
    msg = can.Message(arbitration_id=ROBORIO_HEARTBEAT_ID,
                      data=bytes(data), is_extended_id=True)
    bus.send(msg)

def send_duty_cycle(bus, duty_cycle):
    data = struct.pack('<f', duty_cycle) + b'\x00\x00\x00\x00'
    msg  = can.Message(arbitration_id=DUTY_CYCLE_ID,
                       data=data, is_extended_id=True)
    bus.send(msg)

bus = can.interface.Bus(channel=CAN_CHANNEL, interface='socketcan')

print("Sending roboRIO heartbeat to enable SPARK MAX...")
for i in range(50):  # 1 second of heartbeat
    send_heartbeat(bus, enabled=True)
    time.sleep(0.02)

print(f"Running motor at {DUTY_CYCLE*100}%...")
start = time.time()
while time.time() - start < RUN_TIME:
    send_heartbeat(bus, enabled=True)
    send_duty_cycle(bus, DUTY_CYCLE)
    time.sleep(0.02)

print("Stopping...")
for i in range(20):
    send_heartbeat(bus, enabled=True)
    send_duty_cycle(bus, 0.0)
    time.sleep(0.02)

bus.shutdown()
print("Done.")