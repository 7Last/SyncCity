import os
import unittest.mock
import zoneinfo
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.serializers.strategy.avro_record_serialization_strategy import \
    AvroRecordSerializationStrategy


class TestAvroSerializer(unittest.TestCase):
    @unittest.mock.patch.dict(
        os.environ, {"SCHEMA_REGISTRY_URL": ""}, clear=True,
    )
    def test_load_avro_schema_missing_schema_registry(self) -> None:
        with self.assertRaisesRegex(
                Exception,
                "SCHEMA_REGISTRY_URL environment variable must be set",
        ):
            AvroRecordSerializationStrategy()

    @unittest.mock.patch.dict(
        os.environ, {"SCHEMA_REGISTRY_URL": "http://schema-registry.com"}, clear=True,
    )
    @unittest.mock.patch('simulator.src.serializers.strategy.avro_record_serialization_strategy.SchemaRegistry')
    @unittest.mock.patch('pathlib.Path.read_text')
    def test_serialize(self, mock_path_read_text: MagicMock,
                       registry_mock: MagicMock, ) -> None:
        mock_path_read_text.return_value = """{
                "type": "record",
                "name": "Temperature",
                "fields": [
                    {
                        "name": "sensor_uuid",
                        "type": "string"
                    },
                    {
                        "name": "sensor_name",
                        "type": "string"
                    },
                    {
                        "name": "latitude",
                        "type": "double"
                    },
                    {
                        "name": "longitude",
                        "type": "double"
                    },
                    {
                        "name": "timestamp",
                        "type": "string"
                    },
                    {
                        "name": "value",
                        "type": "float"
                    },
                    {
                        "name": "group_name",
                        "type": [
                            "null",
                            "string"
                        ]
                    }
                ]
            }"""
        registry_mock.register_schema.return_value = 1

        temperature_raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0,
                               tzinfo=zoneinfo.ZoneInfo("Europe/Rome")),
            value=0.0,
        )

        avro_serializer = AvroRecordSerializationStrategy()
        serialized = avro_serializer.serialize_value(temperature_raw_data)

        magic_byte = b'\x00'
        schema_id_bytes = b'\x00\x00\x00\x01'
        raw_bytes = (b'H123e4567-e89b-12d3-a456-426614174000\x16sensor_name\x00\x00'
                     b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0022023'
                     b'-12-31T23:00:00+00:00\x00\x00\x00\x00\x00')

        expected = magic_byte + schema_id_bytes + raw_bytes
        self.assertEqual(serialized, expected)