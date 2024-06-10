import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData


class TestTemperatureRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = TemperatureRawData(
            sensor_name="temperature",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            value=0.0,
        )

        self.assertEqual(data.topic, "temperature")

    def test_subject(self) -> None:
        data = TemperatureRawData(
            sensor_name="temperature",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            value=0.0,
        )

        self.assertEqual(data.value_subject(), "temperature-value")
