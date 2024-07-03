import unittest.mock
from datetime import datetime, UTC
from uuid import UUID

from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.serializers.json_record_serialization_strategy import \
    JsonRecordSerializationStrategy


class TestJsonRecordSerializationStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self._timestamp = datetime(2021, 1, 1, 0, 0, 0, 0, tzinfo=UTC)

    def test_serialize_key(self) -> None:
        serializer = JsonRecordSerializationStrategy()
        uuid = UUID("00000000-0000-0000-0000-000000000000")

        data = TemperatureRawData(
            sensor_name="temperature",
            sensor_uuid=uuid,
            latitude=0.0,
            longitude=0.0,
            timestamp=self._timestamp,
            value=0.0,
        )

        key = serializer.serialize_key(data)
        uuid_bytes = str(uuid).encode("utf-8")
        self.assertEqual(key, uuid_bytes)

    def test_serialize_value(self) -> None:
        serializer = JsonRecordSerializationStrategy()
        mock_data = unittest.mock.MagicMock(spec=TemperatureRawData)
        mock_data.to_json.return_value = {
            "sensor_name": "temperature",
        }

        value = serializer.serialize_value(mock_data)
        self.assertEqual(value, b'{"sensor_name": "temperature"}')
