import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.river_level_raw_data import RiverLevelRawData
from simulator.src.simulators.river_level_simulator import RiverLevelSimulator


class TestRiverLevelSimulator(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = MagicMock()

    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            RiverLevelSimulator(
                sensor_name='',
                config=SensorConfig({
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'river_level',
                    'points_spacing': 'PT1H',
                    'generation_delay': 'PT1H',
                    'latitude': 0,
                    'longitude': 0,
                }),
                producer=self.producer,
            )

    def test_start(self) -> None:
        simulator = RiverLevelSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'river_level',
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
        simulator = RiverLevelSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'river_level',
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

    @patch('random.gauss', side_effect=[0.8, 0.9, 0.5])
    def test_stream(self, _: Mock) -> None:
        simulator = RiverLevelSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'river_level',
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
            RiverLevelRawData(
                value=2010.3209452509564,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
            ),
            RiverLevelRawData(
                value=2261.611063407326,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
            ),
            RiverLevelRawData(
                value=1256.4505907818477,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
            ),
        ]

        self.assertEqual(stream, expected)