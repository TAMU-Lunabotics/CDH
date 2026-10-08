"""Unit-testable command expiry and differential power mapping."""
import math


class DriveGuard:
    def __init__(self, wheel_track_m, max_ground_speed_mps,
                 left_sign=0, right_sign=0, timeout=0.25):
        if wheel_track_m <= 0 or max_ground_speed_mps <= 0 or timeout <= 0:
            raise ValueError('positive measured track, speed and timeout required')
        if left_sign not in (-1, 1) or right_sign not in (-1, 1):
            raise ValueError('supervised left and right sign calibration required')
        self.track = wheel_track_m
        self.speed = max_ground_speed_mps
        self.left_sign, self.right_sign = left_sign, right_sign
        self.timeout = timeout
        self.last_time = -1e9
        self.linear = 0.0
        self.angular = 0.0

    def accept(self, linear, angular, now):
        if not all(math.isfinite(x) for x in (linear, angular, now)):
            raise ValueError('nonfinite command')
        if abs(linear) > self.speed or abs(angular) > 2*self.speed/self.track:
            raise ValueError('command exceeds calibrated drive envelope')
        self.linear, self.angular, self.last_time = linear, angular, now

    def invalidate(self):
        self.linear, self.angular, self.last_time = 0.0, 0.0, -1e9

    def output(self, now, estop, estop_time):
        if (estop or now - self.last_time > self.timeout or
            now - estop_time > self.timeout or
            self.last_time > now + 0.1 or estop_time > now + 0.1):
            return 0, 0
        left = self.linear - self.angular * self.track / 2
        right = self.linear + self.angular * self.track / 2
        scale = max(1.0, abs(left)/self.speed, abs(right)/self.speed)
        return (round(127 * self.left_sign * left / (self.speed * scale)),
                round(127 * self.right_sign * right / (self.speed * scale)))
