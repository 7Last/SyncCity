import unittest

from simulator.src.models.sensor_type import SensorType


class TestSensorType(unittest.TestCase):
    def test_temperature(self) -> None:
        self.assertEqual(SensorType.TEMPERATURE.value, "temperature")

    def test_traffic(self) -> None:
        self.assertEqual(SensorType.TRAFFIC.value, "traffic")

    def test_recycling_point(self) -> None:
        self.assertEqual(SensorType.RECYCLING_POINT.value, "recycling_point")

    def test_from_str(self) -> None:
        self.assertEqual(SensorType.from_str("temperature"), SensorType.TEMPERATURE)
        self.assertEqual(SensorType.from_str("TRAFFIC"), SensorType.TRAFFIC)
        self.assertEqual(SensorType.from_str("recycling_point"),
                         SensorType.RECYCLING_POINT)
