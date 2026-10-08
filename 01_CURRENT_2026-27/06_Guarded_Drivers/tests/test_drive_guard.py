import unittest
from cdh_actuator_guard.drive_guard import DriveGuard


class DriveGuardTests(unittest.TestCase):
    def setUp(self):
        self.g = DriveGuard(0.7, 0.5, left_sign=1, right_sign=-1)

    def test_disallows_uncalibrated_signs(self):
        with self.assertRaises(ValueError):
            DriveGuard(0.7, 0.5)

    def test_forward_and_turn_signs(self):
        self.g.accept(.25, 0, 1)
        self.assertEqual(self.g.output(1.1, False, 1.1), (64, -64))
        self.g.accept(0, .5, 2)
        left, right = self.g.output(2.1, False, 2.1)
        self.assertLess(left, 0)
        self.assertLess(right, 0)  # right_sign reverses positive wheel velocity

    def test_command_and_estop_expire(self):
        self.g.accept(.25, 0, 1)
        self.assertEqual(self.g.output(1.3, False, 1.3), (0, 0))
        self.assertEqual(self.g.output(1.1, False, .5), (0, 0))
        self.assertEqual(self.g.output(1.1, True, 1.1), (0, 0))

    def test_invalid_command_cannot_resume_previous_motion(self):
        self.g.accept(.25,0,1)
        with self.assertRaises(ValueError):
            self.g.accept(100,0,1.1)
        self.g.invalidate()
        self.assertEqual(self.g.output(1.2,False,1.2),(0,0))


if __name__ == '__main__':
    unittest.main()
