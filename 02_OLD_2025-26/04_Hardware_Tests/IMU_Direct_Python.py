"""
ISM330DLC IMU Reader — Jetson (I2C)
Reads raw accelerometer and gyroscope data and prints to terminal.
"""

import smbus2
import struct
import time

I2C_BUS = 7
IMU_ADDR = 0x6A

WHO_AM_I = 0x0F
CTRL1_XL = 0x10
CTRL2_G = 0x11
CTRL3_C = 0x12

OUTX_L_G = 0x22
OUTX_L_XL = 0x28


class ISM330DLC:
    def __init__(self, bus=I2C_BUS, address=IMU_ADDR):
        self.bus = smbus2.SMBus(bus)
        self.address = address
        self._verify_who_am_i()
        self._configure()

    def _verify_who_am_i(self):
        chip_id = self.bus.read_byte_data(self.address, WHO_AM_I)
        if chip_id != 0x6B:
            raise RuntimeError(
                f"WHO_AM_I mismatch: expected 0x6B, got 0x{chip_id:02X}. Check wiring and I2C address."
            )
        print(f"IMU detected (WHO_AM_I = 0x{chip_id:02X})")

    def _configure(self):
        ctrl3 = self.bus.read_byte_data(self.address, CTRL3_C)
        self.bus.write_byte_data(self.address, CTRL3_C, ctrl3 | 0x44)

        self.bus.write_byte_data(self.address, CTRL1_XL, 0x40)
        self.bus.write_byte_data(self.address, CTRL2_G, 0x40)

        time.sleep(0.1)
        print("IMU configured: 104 Hz ODR | Accel ±2g | Gyro ±250 dps")

    def _read_raw_xyz(self, start_reg):
        data = self.bus.read_i2c_block_data(self.address, start_reg, 6)
        x, y, z = struct.unpack("<hhh", bytes(data))
        return x, y, z

    def read_accel_raw(self):
        return self._read_raw_xyz(OUTX_L_XL)

    def read_gyro_raw(self):
        return self._read_raw_xyz(OUTX_L_G)

    def close(self):
        self.bus.close()


def main():
    imu = ISM330DLC()

    print("\nReading raw IMU data — Ctrl+C to stop\n")
    print(f"{'ACCEL (raw)':>36s}  |  {'GYRO (raw)':>36s}")
    print(f"{'X':>12s}{'Y':>12s}{'Z':>12s}  |  {'X':>12s}{'Y':>12s}{'Z':>12s}")
    print("-" * 78)

    try:
        while True:
            ax, ay, az = imu.read_accel_raw()
            gx, gy, gz = imu.read_gyro_raw()
            print(f"{ax:>12d}{ay:>12d}{az:>12d}  |  {gx:>12d}{gy:>12d}{gz:>12d}")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        imu.close()


if __name__ == "__main__":
    main()