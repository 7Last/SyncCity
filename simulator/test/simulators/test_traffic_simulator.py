import unittest
from datetime import timedelta, datetime
from unittest.mock import patch, Mock
from uuid import UUID

from simulator.src.models.raw_data.traffic_raw_data import TrafficRawData
from simulator.src.simulators.traffic_simulator import TrafficSimulator


class TestTrafficSimulator(unittest.TestCase):
    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            TrafficSimulator(
                sensor_name='',
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                points_spacing=timedelta(seconds=1),
                generation_delay=timedelta(seconds=1),
                latitude=0,
                longitude=0,
            )

    def test_start(self) -> None:
        simulator = TrafficSimulator(
            sensor_name='test',
            sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
            points_spacing=timedelta(seconds=1),
            generation_delay=timedelta(seconds=1),
            latitude=0,
            longitude=0,
        )
        self.assertEqual(simulator.running, False)
        simulator.start()
        self.assertEqual(simulator.running, True)

    def test_stop(self) -> None:
        simulator = TrafficSimulator(
            sensor_name='test',
            sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
            points_spacing=timedelta(seconds=0),
            generation_delay=timedelta(seconds=0),
            latitude=0,
            longitude=0,
        )
        simulator.start()
        self.assertEqual(simulator.running, True)
        simulator.stop()
        self.assertEqual(simulator.running, False)

    @patch('random.uniform')
    def test_stream(self, mock_uniform: Mock) -> None:
        simulator = TrafficSimulator(
            sensor_name='test',
            sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
            points_spacing=timedelta(hours=1),
            generation_delay=timedelta(seconds=0),
            begin_date=datetime(2024, 1, 1, 0, 0, 0),
            limit=3,
            latitude=0,
            longitude=0,
        )
        mock_uniform.return_value = 0
        simulator.start()
        stream = list(simulator.stream())

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
