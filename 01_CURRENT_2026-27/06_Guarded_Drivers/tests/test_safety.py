import unittest
from cdh_actuator_guard.safety import SafetyLatch


class SafetyTests(unittest.TestCase):
    def test_estop_release_alone_does_not_rearm(self):
        latch = SafetyLatch()
        self.assertFalse(latch.armed)
        self.assertFalse(latch.reset(1,True,1))
        self.assertTrue(latch.reset(1.1,False,1.1))
        latch.trip('estop')
        self.assertFalse(latch.armed)
        self.assertEqual(latch.reason,'estop')
        self.assertFalse(latch.reset(2,False,1))
        self.assertTrue(latch.reset(2,False,2))

    def test_rejects_future_estop_stamp(self):
        latch = SafetyLatch()
        self.assertFalse(latch.reset(1,False,2))


if __name__ == '__main__':
    unittest.main()
