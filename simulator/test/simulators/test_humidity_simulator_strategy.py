import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.humidity_raw_data import HumidityRawData
from simulator.src.simulators.humidity_simulator_strategy import HumiditySimulatorStrategy


class TestHumiditySimulatorStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = MagicMock()

    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            HumiditySimulatorStrategy(
                sensor_name='',
                config=SensorConfig({
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'humidity',
                    'points_spacing': 'PT1H',
                    'generation_delay': 'PT1H',
                    'latitude': 0,
                    'longitude': 0,
                }),
                producer=self.producer,
            )

    @patch('random.uniform', return_value=0)
    def test_data(self, _: Mock) -> None:
        simulator = HumiditySimulatorStrategy(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'humidity',
                'limit': 3,
                'points_spacing': 'PT1H',
                'generation_delay': 'PT0S',
                'begin_date': datetime(2024, 1, 1),
                'latitude': 0,
                'longitude': 0,
            }),
            producer=self.producer,
        )

        stream = [simulator.data() for _ in range(3)]

        expected = [
            HumidityRawData(
                value=36.141589368060096,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
            ),
            HumidityRawData(
                value=39.24770500506624,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
            ),
            HumidityRawData(
                value=42.30067414234525,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
            ),
        ]

        self.assertEqual(stream, expected)
