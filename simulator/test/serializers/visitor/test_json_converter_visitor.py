import unittest
from datetime import datetime, UTC
from uuid import UUID

from simulator.src.models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.models.raw_data.traffic_raw_data import TrafficRawData
from simulator.src.serializers.visitor.json_converter_visitor import \
    JsonConverterVisitor


class TestJsonConverterVisitor(unittest.TestCase):
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
        temperature_raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )
        visitor = JsonConverterVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "value": 0.0,
        }
        self.assertEqual(visitor.visit_temperature_raw_data(temperature_raw_data),
                         expected)

    def test_serialize_temperature_raw_data_without_group(self) -> None:
        temperature_raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )
        visitor = JsonConverterVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": None,
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "value": 0.0,
        }
        self.assertEqual(visitor.visit_temperature_raw_data(temperature_raw_data),
                         expected)

    def test_serialize_traffic_raw_data(self) -> None:
        traffic_raw_data = TrafficRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            vehicles=0,
            avg_speed=0.0,
        )
        visitor = JsonConverterVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "vehicles": 0,
            "avg_speed": 0.0,
        }
        self.assertEqual(visitor.visit_traffic_raw_data(traffic_raw_data),
                         expected)

    def test_serialize_recycling_point_raw_data(self) -> None:
        recycling_point_raw_data = RecyclingPointRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            filling=0.0,
        )
        visitor = JsonConverterVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "filling": 0.0,
        }
        self.assertEqual(
            visitor.visit_recycling_point_raw_data(recycling_point_raw_data),
            expected)
