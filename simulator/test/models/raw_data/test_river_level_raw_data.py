import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.river_level_raw_data import RiverLevelRawData


class TestRiverLevelRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = RiverLevelRawData(
            sensor_name="river_level",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            value=0,
        )

        self.assertEqual(data.topic, "river_level")

    def test_subject(self) -> None:
        data = RiverLevelRawData(
            sensor_name="river_level",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            value=0,
        )

        self.assertEqual(data.value_subject(), "river_level-value")
