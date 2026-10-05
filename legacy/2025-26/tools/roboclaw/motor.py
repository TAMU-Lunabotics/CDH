from roboclaw_3 import Roboclaw
import time

# Setup
rc = Roboclaw("/dev/ttyACM0", 38400)
rc.Open()

ADDRESS = 0x80  # default RoboClaw address

# Read version to confirm connection
version = rc.ReadVersion(ADDRESS)
print("RoboClaw version:", version)

# Drive both motors forward at half speed (64 out of 127)
print("Driving forward...")
rc.ForwardM1(ADDRESS, 64)
#rc.ForwardM2(ADDRESS, 64)

time.sleep(3.0)  # drive for 3 seconds

# Stop
print("Stopping...")
rc.ForwardM1(ADDRESS, 0)
#rc.ForwardM2(ADDRESS, 0)