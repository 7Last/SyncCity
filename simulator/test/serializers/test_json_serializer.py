import unittest
from datetime import datetime, UTC
from uuid import UUID

from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.serializers.json_serializer import JsonSerializer


class TestJsonSerializer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.datetime = datetime(
            year=2024,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=UTC,
        )

    def test_serialize_temperature_raw_data(self) -> None:
        json_serializer = JsonSerializer()
        temperature_raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )

        serialized = json_serializer.serialize(temperature_raw_data)




    def test_serialize_traffic_raw_data(self) -> None:
        pass

    def test_serialize_recycling_point_raw_data(self) -> None:
        pass
