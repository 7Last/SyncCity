import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.parking_raw_data import ParkingRawData


class TestParkingRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = ParkingRawData(
            sensor_name="traffic",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self._timestamp,
            is_occupied=True,
        )

        self.assertEqual(data.topic, "parking")

    def test_subject(self) -> None:
        data = ParkingRawData(
            sensor_name="parking",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self._timestamp,
            is_occupied=True,
        )

        self.assertEqual(data.value_subject(), "parking-value")
