"""Latched driver inhibit requiring a deliberate manual reset."""
import math


class SafetyLatch:
    def __init__(self, timeout=.25):
        self.timeout = timeout
        self.reason = 'startup'

    @property
    def armed(self):
        return not self.reason

    def trip(self, reason):
        self.reason = reason or 'unspecified_fault'

    def reset(self, now, estop, estop_time):
        if (not math.isfinite(now) or not math.isfinite(estop_time) or
            estop or estop_time > now+.1 or now-estop_time > self.timeout):
            return False
        self.reason = ''
        return True
