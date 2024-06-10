import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.air_quality_raw_data import AirQualityRawData


class TestAirQualityRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = AirQualityRawData(
            sensor_name="air_quality",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            pm25=0,
            pm10=0,
            so2=0,
            no2=0,
            o3=0,
        )

        self.assertEqual(data.topic, "air_quality")

    def test_subject(self) -> None:
        data = AirQualityRawData(
            sensor_name="air_quality",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            pm25=0,
            pm10=0,
            so2=0,
            no2=0,
            o3=0,
        )

        self.assertEqual(data.value_subject(), "air_quality-value")
