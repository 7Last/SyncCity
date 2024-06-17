import unittest
from datetime import datetime
from unittest.mock import patch, Mock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.simulators.temperature_simulator import TemperatureSimulator


class TestTemperatureSimulator(unittest.TestCase):
    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            TemperatureSimulator(
                sensor_name='',
                config=SensorConfig({
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'temperature',
                    'points_spacing': 'PT1S',
                    'generation_delay': 'PT1S',
                    'latitude': 0,
                    'longitude': 0,
                }),
            )

    def test_start(self) -> None:
        simulator = TemperatureSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'temperature',
                'points_spacing': 'PT1S',
                'generation_delay': 'PT1S',
                'latitude': 0,
                'longitude': 0,
            }),
        )
        self.assertEqual(simulator._running, False)
        simulator.start()
        self.assertEqual(simulator._running, True)

    def test_stop(self) -> None:
        simulator = TemperatureSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'temperature',
                'points_spacing': 'PT1S',
                'generation_delay': 'PT1S',
                'latitude': 0,
                'longitude': 0,
            }),
        )
        simulator.start()
        self.assertEqual(simulator._running, True)
        simulator.stop()
        self.assertEqual(simulator._running, False)

    @patch('random.uniform')
    def test_stream(self, mock_uniform: Mock) -> None:
        simulator = TemperatureSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'temperature',
                'begin_date': datetime(2024, 1, 1),
                'points_spacing': 'PT1H',
                'generation_delay': 'PT0S',
                'limit': 3,
                'latitude': 0,
                'longitude': 0,
            }),
        )
        mock_uniform.return_value = 0
        simulator.start()
        stream = list(simulator.data())

        expected = [
            TemperatureRawData(
                value=3.153388482065103,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
            ),
            TemperatureRawData(
                value=4.395834736867558,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
            ),
            TemperatureRawData(
                value=5.617022391779162,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
            ),
        ]

        self.assertEqual(stream, expected)
