import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from simulator.src.simulators.recycling_point_simulator_strategy import RecyclingPointSimulatorStrategy


class TestRecyclingPointSimulatorStrategy(unittest.TestCase):

    def setUp(self) -> None:
        self.producer = MagicMock()

    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            RecyclingPointSimulatorStrategy(
                sensor_name='',
                config=SensorConfig({
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'recycling_point',
                    'points_spacing': 'PT1H',
                    'generation_delay': 'PT1H',
                    'latitude': 0,
                    'longitude': 0,
                }),

            )

    @patch('random.uniform', return_value=0)
    @patch('builtins.max', return_value=0)
    def test_data(self, _: Mock, __: Mock) -> None:
        simulator = RecyclingPointSimulatorStrategy(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'recycling_point',
                'begin_date': datetime(2024, 1, 1),
                'points_spacing': 'PT1H',
                'generation_delay': 'PT0S',
                'limit': 3,
                'latitude': 0,
                'longitude': 0,
            }),

        )

        stream = [simulator.simulate() for _ in range(3)]

        expected = [
            RecyclingPointRawData(
                filling=0,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
            ),
            RecyclingPointRawData(
                filling=0,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
            ),
            RecyclingPointRawData(
                filling=0,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
            ),
        ]

        self.assertEqual(stream, expected)
