import unittest

from simulator.src.models.sensor_type import SensorType


class TestSensorType(unittest.TestCase):
    def test_temperature(self) -> None:
        self.assertEqual(SensorType.TEMPERATURE.value, "temperature")

    def test_traffic(self) -> None:
        self.assertEqual(SensorType.TRAFFIC.value, "traffic")

    def test_recycling_point(self) -> None:
        self.assertEqual(SensorType.RECYCLING_POINT.value, "recycling_point")

    def test_parking(self) -> None:
        self.assertEqual(SensorType.PARKING.value, "parking")

    def test_air_quality(self) -> None:
        self.assertEqual(SensorType.AIR_QUALITY.value, "air_quality")

    def test_charging_station(self) -> None:
        self.assertEqual(SensorType.CHARGING_STATION.value, "charging_station")

    def test_humidity(self) -> None:
        self.assertEqual(SensorType.HUMIDITY.value, "humidity")

    def test_precipitation(self) -> None:
        self.assertEqual(SensorType.PRECIPITATION.value, "precipitation")

    def test_river_level(self) -> None:
        self.assertEqual(SensorType.RIVER_LEVEL.value, "river_level")

    def test_from_str(self) -> None:
        self.assertEqual(SensorType.from_str("temperature"), SensorType.TEMPERATURE)
        self.assertEqual(SensorType.from_str("TRAFFIC"), SensorType.TRAFFIC)
        self.assertEqual(SensorType.from_str("recycling_point"),
                         SensorType.RECYCLING_POINT)
        self.assertEqual(SensorType.from_str("PaRkInG"), SensorType.PARKING)
        self.assertEqual(SensorType.from_str("Air_Quality"), SensorType.AIR_QUALITY)
        self.assertEqual(SensorType.from_str("charging_station"),
                         SensorType.CHARGING_STATION)
        self.assertEqual(SensorType.from_str("HumidIty"), SensorType.HUMIDITY)
        self.assertEqual(SensorType.from_str("precipitation"), SensorType.PRECIPITATION)
        self.assertEqual(SensorType.from_str("RIVER_level"), SensorType.RIVER_LEVEL)
