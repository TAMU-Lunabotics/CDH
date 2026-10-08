import unittest
from cdh_actuator_guard.tool_guard import ToolGuard,pico_packet


class ToolGuardTests(unittest.TestCase):
    def setUp(self):
        self.g = ToolGuard(1,.15)

    def test_requires_calibration(self):
        with self.assertRaises(ValueError):
            ToolGuard()

    def test_recovered_pico_packet_and_rejects_unsafe_values(self):
        self.assertEqual(pico_packet((0,1,0)),b'0,1,0.0000\n')
        self.assertEqual(pico_packet((1,0,-.1)),b'1,0,-0.1000\n')
        self.assertEqual(pico_packet((0,0,.15)),b'0,0,0.1500\n')
        for invalid in ((.5,0,0),(0,1.2,0),(0,1,float('nan')),
                        (0,1,1.1),(1,1,0)):
            with self.subTest(invalid=invalid),self.assertRaises(ValueError):
                pico_packet(invalid)

    def test_lower_dig_raise_dump_interlocks(self):
        self.g.accept('lower',1)
        self.assertEqual(self.g.output(1.1,False,1.1,True,1.1,False,1.1),
                         ((0,0,.15),'lowering'))
        self.assertEqual(self.g.output(1.2,False,1.2,False,1.2,False,1.2),
                         ((0,0,.15),'lowering'))
        self.g.accept('dig',2)
        self.assertEqual(self.g.output(2.1,False,2.1,False,2.1,True,2.1,
                                       dig_rpm=10,dig_time=2.1),
                         ((0,1,0),'digging'))
        self.g.accept('raise',3)
        self.assertEqual(self.g.output(3.1,False,3.1,False,3.1,True,3.1),
                         ((0,0,-.15),'raising'))
        self.g.accept('dump',4)
        self.assertEqual(self.g.output(4.1,False,4.1,True,4.1,False,4.1,
                                       dump_rpm=10,dump_time=4.1),
                         ((1,0,0),'dumping'))

    def test_missing_feedback_and_timeout_stop(self):
        self.g.accept('dig',1)
        self.assertEqual(self.g.output(1.1,False,1.1,True,1.1,False,1.1)[1],
                         'fault')
        self.assertEqual(self.g.output(1.5,False,1.5,False,1.5,True,1.5),
                         ((0,0,0),'fault'))
        self.assertEqual(self.g.output(1.1,True,1.1,False,1.1,True,1.1),
                         ((0,0,0),'fault'))


if __name__ == '__main__':
    unittest.main()
