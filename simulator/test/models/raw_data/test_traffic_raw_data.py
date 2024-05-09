import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.traffic_raw_data import TrafficRawData


class TestTrafficRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = TrafficRawData(
            sensor_name="traffic",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            vehicles_per_hour=0,
            avg_speed=0,
        )

        self.assertEqual(data.topic, "traffic")

    def test_subject(self) -> None:
        data = TrafficRawData(
            sensor_name="traffic",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            vehicles_per_hour=0,
            avg_speed=0,
        )

        self.assertEqual(data.subject, "traffic-value")
