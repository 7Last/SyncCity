import unittest
from datetime import timedelta, datetime
from unittest.mock import patch, Mock
from uuid import UUID

from simulator.src.models.raw_data.air_quality_raw_data import AirQualityRawData
from simulator.src.simulators.air_quality_simulator import AirQualitySimulator


class TestAirQualitySimulator(unittest.TestCase):
    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            AirQualitySimulator(
                sensor_name='',
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                points_spacing=timedelta(seconds=1),
                generation_delay=timedelta(seconds=1),
                latitude=0,
                longitude=0,
            )

    def test_start(self) -> None:
        simulator = AirQualitySimulator(
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
        simulator = AirQualitySimulator(
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
        simulator = AirQualitySimulator(
            sensor_name='test',
            sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
            points_spacing=timedelta(hours=1),
            generation_delay=timedelta(seconds=0),
            begin_date=datetime(2024, 1, 1, 0, 0, 0),
            limit=3,
            latitude=0,
            longitude=0,
        )
        mock_uniform.side_effect = lambda a, b: a

        simulator.start()
        stream = list(simulator.stream())

        expected = [
            AirQualityRawData(
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                o3=113.9815680878308,
                pm25=75.98771205855387,
                pm10=56.9907840439154,
                no2=227.9631361756616,
                so2=227.9631361756616,
            ),
            AirQualityRawData(
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
                o3=115.10626418591272,
                pm25=76.73750945727515,
                pm10=57.55313209295636,
                no2=230.21252837182544,
                so2=230.21252837182544,
            ),
            AirQualityRawData(
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
                o3=116.20867221871677,
                pm25=77.47244814581119,
                pm10=58.104336109358385,
                no2=232.41734443743354,
                so2=232.41734443743354,
            ),
        ]

        # self.assertEqual(stream, expected)
