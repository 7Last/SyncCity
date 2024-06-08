import os
import unittest.mock
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

from avro.schema import parse

from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.serializers.avro_serializer import AvroSerializer


class TestAvroSerializer(unittest.TestCase):
    @unittest.mock.patch.dict(
        os.environ, {"SCHEMA_REGISTRY_URL": ""}, clear=True,
    )
    def test_missing_schema_registry(self) -> None:
        with self.assertRaisesRegex(
                Exception,
                "SCHEMA_REGISTRY_URL environment variable must be set",
        ):
            AvroSerializer()

    @unittest.mock.patch.dict(
        os.environ,
        {
            "SCHEMA_REGISTRY_URL": "schema_registry",
            "SCHEMAS_PATH": "",
        },
        clear=True,
    )
    def test_load_avro_schema_missing_schema_path(self) -> None:
        with self.assertRaisesRegex(
                Exception,
                "SCHEMAS_PATH environment variable must be set",
        ):
            AvroSerializer()

    @unittest.skip  # TODO: implement when overwriting schemas is removed
    @unittest.mock.patch("requests.post")
    def test_create_subject_already_exists(self, mock_post: MagicMock) -> None:
        pass

    @unittest.mock.patch.dict(
        os.environ,
        {},
        clear=True,
    )
    def test_load_avro_schema(self) -> None:
        pass

    @unittest.mock.patch(
        "simulator.src.serializers.avro_serializer.load_avro_schemas",
    )
    def test_serialize(self, load_avro_mock: MagicMock) -> None:
        load_avro_mock.return_value = {
            'temperature-value': (1, parse("""{
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
                    }
                ]
            }""")),
        }
        temperature_raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0),
            value=0.0,
        )

        avro_serializer = AvroSerializer()
        serialized = avro_serializer.serialize(temperature_raw_data)
        serialized_magic_byte = serialized[:1]
        serialized_schema_id = serialized[1:5]
        serialized_data = serialized[5:]

        magic_byte = b'\x00'
        schema_id_bytes = b'\x00\x00\x00\x01'
        raw_bytes = b'H123e4567-e89b-12d3-a456-426614174000\x16sensor_name\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0022023-12-31T23:00:00+00:00\x00\x00\x00\x00'  # noqa: E501

        self.assertEqual(serialized_magic_byte, magic_byte)
        self.assertEqual(serialized_schema_id, schema_id_bytes)
        self.assertEqual(serialized_data, raw_bytes)
