import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.humidity_raw_data import HumidityRawData


class TestHumidityRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = HumidityRawData(
            sensor_name="humidity",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self._timestamp,
            value=0,
        )

        self.assertEqual(data.topic, "humidity")

    def test_subject(self) -> None:
        data = HumidityRawData(
            sensor_name="humidity",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self._timestamp,
            value=0,
        )

        self.assertEqual(data.value_subject(), "humidity-value")
