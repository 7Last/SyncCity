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

    # @unittest.mock.patch("requests.post")
    # def test_create_subject_success(self, mock_post: MagicMock) -> None:
    #     mock_post.return_value.status_code = 200
    #     mock_post.return_value.json.return_value = {"id": 1}
    #
    #     schema_id = _create_subject(
    #         "schema_registry",
    #         "subject",
    #         {"schema": "schema", "schemaType": "AVRO"},
    #     )
    #     self.assertEqual(schema_id, 1)
    #     mock_post.assert_called_once()

    @unittest.skip  # TODO: implement when overwriting schemas is removed
    @unittest.mock.patch("requests.post")
    def test_create_subject_already_exists(self, mock_post: MagicMock) -> None:
        pass

    # @unittest.mock.patch("requests.post")
    # def test_create_subject_error(self, mock_post: MagicMock) -> None:
    #     mock_post.return_value.status_code = 404
    #     mock_post.return_value.json.return_value = {"error": "error"}
    #
    #     with self.assertRaisesRegex(
    #             Exception,
    #             "Error creating schema subject: {'error': 'error'}",
    #     ):
    #         _create_subject("schema_registry",
    #                         "subject",
    #                         {"schema": "schema", "schemaType": "AVRO"},
    #                         )
    #     mock_post.assert_called_once()

    @unittest.mock.patch.dict(
        os.environ,
        {},
        clear=True,
    )
    def test_load_avro_schema(self):
        pass

    def test_serialize(self):
        pass

    # @unittest.mock.patch("builtins.open", create=True, new_callable=mock_open)
    # @unittest.mock.patch("os.listdir")
    # def test_my_method(self, mock_listdir, mock_open_file):
    #     mock_listdir.return_value = ["1.avsc"]
    #     mock_open_file.side_effect = [
    #         unittest.mock.mock_open(read_data="A").return_value,
    #     ]
    #     _create_all_schemas("schema_registry", "path")
    # def test_my_method(self):
    #     with (
    #         unittest.mock.patch("builtins.open", create=True,
    #                             new_callable=mock_open) as mock_open_file,
    #         unittest.mock.patch("os.listdir") as mock_listdir,
    #         unittest.mock.patch(
    #             "simulator.src.serializers._create_subject") as mock_create_subj,
    #     ):
    #         schema = """ {
    #           "type": "record",
    #           "name": "Test",
    #           "fields": []
    #         }
    #         """
    #         mock_listdir.return_value = ["schema-1.avsc", "schema-2.avsc"]
    #         mock_open_file.side_effect = [
    #             unittest.mock.mock_open(read_data=schema).return_value,
    #         ]
    #         mock_create_subj.side_effect = \
    #             lambda url, subject, payload: 1 if subject == "schema1" else 2
    #         _create_all_schemas("schema_registry", "path")
