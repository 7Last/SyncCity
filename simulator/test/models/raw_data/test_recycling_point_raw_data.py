import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.recycling_point_raw_data import RecyclingPointRawData


class TestRecyclingPointRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = RecyclingPointRawData(
            sensor_name="traffic",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            filling=0,
        )

        self.assertEqual(data.topic, "recycling_point")

    def test_subject(self) -> None:
        data = RecyclingPointRawData(
            sensor_name="recycling_point",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            filling=0,
        )

        self.assertEqual(data.value_subject(), "recycling_point-value")
