import serial
import struct
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# RoboClaw default address
ADDRESS = 0x80

# Commands
CMD_READ_ENC1 = 16  # 0x10
CMD_READ_ENC2 = 17  # 0x11

def calc_crc(data):
    crc = 0
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
        crc &= 0xFFFF
    return crc

def read_encoder(command):
    ser.write(bytes([ADDRESS, command]))
    response = ser.read(7)  # 4 bytes value + 1 status + 2 CRC

    if len(response) == 7:
        # Verify CRC
        data = bytes([ADDRESS, command]) + response[:5]
        crc_received = struct.unpack('>H', response[5:7])[0]
        crc_calc = calc_crc(data)

        if crc_received == crc_calc:
            value = struct.unpack('>i', response[0:4])[0]
            status = response[4]
            return value, status
        else:
            print("CRC mismatch — bad data")
            return None, None
    else:
        print(f"Incomplete response: got {len(response)} bytes")
        return None, None

while True:
    enc1, status1 = read_encoder(CMD_READ_ENC1)
    enc2, status2 = read_encoder(CMD_READ_ENC2)

    if enc1 is not None and enc2 is not None:
        print(f"Encoder 1: {enc1}  (status: {status1})")
        print(f"Encoder 2: {enc2}  (status: {status2})")
        print("-" * 35)

    time.sleep(0.1)  # 10Hz read rate, adjust as needed