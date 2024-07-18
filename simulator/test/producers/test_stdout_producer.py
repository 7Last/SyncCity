import unittest
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.producers.stdout_producer import StdOutProducer


class TestStdOutProducer(unittest.TestCase):

    @unittest.mock.patch("simulator.src.serializers.serialization_strategy.SerializationStrategy")
    @unittest.mock.patch("builtins.print")
    def test_produce_serialized_called(self, mock_print: MagicMock,
                                       mock_serialization_strategy: MagicMock) -> None:
        mock_serialization_strategy.serialize.return_value = "serialized"
        mock_print.side_effect = lambda x: x
        stdout_producer = StdOutProducer(mock_serialization_strategy)

        raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0),
            value=0.0,
        )

        stdout_producer.produce(raw_data)
        mock_print.assert_called_once_with("serialized")
