import unittest

from simulator.src.models.sensor_type import SensorType


class TestStringMethods(unittest.TestCase):

    def test_sensor_type(self):
        type = SensorType.TRAFFIC
        self.assertEqual(type, SensorType.TRAFFIC)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()
