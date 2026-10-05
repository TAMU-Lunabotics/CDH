# Run this standalone first to confirm wiring works

import sys
sys.path.append('/home/lunabotics/TAMU_SEDS_Lunabotics/roboclaw')
from roboclaw_3 import Roboclaw

for baud in [2400, 9600, 19200, 38400, 57600, 115200]:
    try:
        rc = Roboclaw("/dev/ttyTHS1", baud)
        rc.Open()
        result = rc.ReadVersion(0x80)
        print(f"Baud {baud}: {result}")
        rc._port.close()
    except Exception as e:
        print(f"Baud {baud}: ERROR {e}")

# Should print: (1, b'USB Roboclaw 2x15a v4.x.x\n') or similar
# If it prints (0,) — check wiring or baud rate