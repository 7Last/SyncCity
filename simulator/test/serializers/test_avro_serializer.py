import os
import unittest.mock
from unittest.mock import MagicMock

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
        with self.assertRaisesRegex(Exception,
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

    def test_serialize(self) -> None:
        pass
