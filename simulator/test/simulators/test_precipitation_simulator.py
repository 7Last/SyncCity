import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.precipitation_raw_data import PrecipitationRawData
from simulator.src.simulators.precipitation_simulator import PrecipitationSimulator


class TestPrecipitationSimulator(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = MagicMock()

    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            PrecipitationSimulator(
                sensor_name='',
                config=SensorConfig({
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'precipitation',
                    'points_spacing': 'PT1H',
                    'generation_delay': 'PT1H',
                    'latitude': 0,
                    'longitude': 0,
                }),
                producer=self.producer,
            )

    def test_start(self) -> None:
        simulator = PrecipitationSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'precipitation',
                'points_spacing': 'PT1H',
                'generation_delay': 'PT1H',
                'latitude': 0,
                'longitude': 0,
            }),
            producer=self.producer,
        )
        simulator.start()
        self.assertEqual(simulator.is_running(), True)
        simulator.stop()

    def test_stop(self) -> None:
        simulator = PrecipitationSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'precipitation',
                'points_spacing': 'PT1H',
                'generation_delay': 'PT1H',
                'latitude': 0,
                'longitude': 0,
            }),
            producer=self.producer,
        )
        simulator.start()
        simulator.stop()
        self.assertEqual(simulator.is_running(), False)

    @patch('random.uniform', return_value=0)
    def test_stream(self, _: Mock) -> None:
        simulator = PrecipitationSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'precipitation',
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
            PrecipitationSimulator(
                value=1.9505748517128412, #non so che valore mettere
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
            ),
            PrecipitationSimulator(
                value=1.9505748517128412,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
            ),
            PrecipitationSimulator(
                value=1.9505748517128412,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
            ),
        ]

        self.assertEqual(stream, expected)
