import unittest
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.parking_raw_data import ParkingRawData
from simulator.src.simulators.parking_simulator import ParkingSimulator


class TestParkingSimulator(unittest.TestCase):
    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            ParkingSimulator(
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

    def test_start(self) -> None:
        simulator = ParkingSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'recycling_point',
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
        simulator = ParkingSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'recycling_point',
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

    @unittest.mock.patch(
        'random.random',
        side_effect=[0.1, 0.6, 0.3],
    )
    @unittest.mock.patch(
        'simulator.src.simulators.parking_simulator.ParkingSimulator._generate_next_occupancy_change',
    )
    def test_stream(self, mock_next_change: MagicMock, _) -> None:
        simulator = ParkingSimulator(
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

        mock_next_change.side_effect = [
            datetime(2024, 1, 1, 4),
            datetime(2024, 1, 1, 5),
            datetime(2024, 1, 1, 6),
        ]

        simulator.start()
        stream = list(simulator.stream())

        expected = [
            ParkingRawData(
                is_occupied=True,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
            ),
            ParkingRawData(
                is_occupied=False,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 4, 0, 0),
            ),
            ParkingRawData(
                is_occupied=True,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 5, 0, 0),
            ),
        ]

        self.assertEqual(stream, expected)
