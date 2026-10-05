from roboclaw_3 import Roboclaw
import time

rc = Roboclaw("/dev/ttyACM0", 38400)
rc.Open()

ADDRESS = 0x80
rc.ResetEncoders(ADDRESS)

# Spin motor slowly and watch encoder count
rc.ForwardM1(ADDRESS, 30)
time.sleep(0.5)
rc.ForwardM1(ADDRESS, 0)

enc = rc.ReadEncM1(ADDRESS)
print("Encoder count:", enc)   # should be non-zero