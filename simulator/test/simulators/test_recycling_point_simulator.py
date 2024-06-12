import unittest
from datetime import timedelta, datetime
from unittest.mock import patch, Mock
from uuid import UUID

from simulator.src.models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from simulator.src.simulators.recycling_point_simulator import RecyclingPointSimulator


class TestRecyclingPointSimulator(unittest.TestCase):
    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            RecyclingPointSimulator(
                sensor_name='',
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                points_spacing=timedelta(seconds=1),
                generation_delay=timedelta(seconds=1),
                latitude=0,
                longitude=0,
            )

    def test_start(self) -> None:
        simulator = RecyclingPointSimulator(
            sensor_name='test',
            sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
            points_spacing=timedelta(seconds=1),
            generation_delay=timedelta(seconds=1),
            latitude=0,
            longitude=0,
        )
        self.assertEqual(simulator._running, False)
        simulator.start()
        self.assertEqual(simulator._running, True)

    def test_stop(self) -> None:
        simulator = RecyclingPointSimulator(
            sensor_name='test',
            sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
            points_spacing=timedelta(seconds=0),
            generation_delay=timedelta(seconds=0),
            latitude=0,
            longitude=0,
        )
        simulator.start()
        self.assertEqual(simulator._running, True)
        simulator.stop()
        self.assertEqual(simulator._running, False)

    @patch('random.uniform')
    @patch('builtins.max')
    def test_stream(self, mock_max: Mock, mock_uniform: Mock) -> None:
        simulator = RecyclingPointSimulator(
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
        mock_max.side_effect = lambda _, __: 0

        simulator.start()
        stream = list(simulator.stream())

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
