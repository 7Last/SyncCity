import unittest.mock
from datetime import datetime, UTC
from uuid import UUID

from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.serializers.strategy.json_record_serialization_strategy import \
    JsonRecordSerializationStrategy
from simulator.src.serializers.visitor.converter_visitor import ConverterVisitor


class TestJsonRecordSerializationStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.timestamp = datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=UTC)

    def test_serialize_key(self) -> None:
        serializer = JsonRecordSerializationStrategy()

        data = TemperatureRawData(
            sensor_name="temperature",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            value=0.0,
        )

        key = serializer.serialize_key(data)
        uuid_bytes = UUID("00000000-0000-0000-0000-000000000000").bytes
        self.assertEqual(key, uuid_bytes)

    def test_serialize_value(self) -> None:
        # create mock for ConverterVisitor
        mock = unittest.mock.MagicMock(spec=ConverterVisitor)
        mock.visit_temperature_raw_data.return_value = {
            "sensor_name": "temperature",
        }

        serializer = JsonRecordSerializationStrategy(mock)
        data = TemperatureRawData(
            sensor_name="temperature",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.timestamp,
            value=0.0,
        )

        value = serializer.serialize_value(data)
        self.assertEqual(value, b'{"sensor_name": "temperature"}')
