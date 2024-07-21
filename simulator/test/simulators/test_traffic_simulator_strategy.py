import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.traffic_raw_data import TrafficRawData
from simulator.src.simulators.traffic_simulator_strategy import TrafficSimulatorStrategy


class TestTrafficSimulatorStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = MagicMock()

    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            TrafficSimulatorStrategy(
                sensor_name='',
                config=SensorConfig({
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'traffic',
                    'points_spacing': 'PT1H',
                    'generation_delay': 'PT1H',
                    'latitude': 0,
                    'longitude': 0,
                }),

            )

    @patch('random.uniform', return_value=0)
    def test_data(self, _: Mock) -> None:
        simulator = TrafficSimulatorStrategy(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'traffic',
                'limit': 3,
                'points_spacing': 'PT1H',
                'generation_delay': 'PT0S',
                'begin_date': datetime(2024, 1, 1),
                'latitude': 0,
                'longitude': 0,
            }),

        )

        stream = [simulator.simulate() for _ in range(3)]

        expected = [
            TrafficRawData(
                avg_speed=32.470887891211184,
                vehicles=39,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
            ),
            TrafficRawData(
                avg_speed=34.12195312644378,
                vehicles=39,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
            ),
            TrafficRawData(
                avg_speed=34.08242621271829,
                vehicles=37,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
            ),
        ]

        self.assertEqual(stream, expected)
