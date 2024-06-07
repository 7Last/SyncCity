import unittest.mock
from datetime import datetime, UTC
from unittest.mock import MagicMock

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

    @unittest.mock.patch("simulator.src.models.raw_data.raw_data.RawData")
    def test_serialize_raw_data(self, mock_raw_data: MagicMock) -> None:  # noqa: PLR6301
        mock_raw_data.accept.return_value = {}
        json_serializer = JsonSerializer()
        json_serializer.serialize(mock_raw_data)
        mock_raw_data.accept.assert_called_once()
