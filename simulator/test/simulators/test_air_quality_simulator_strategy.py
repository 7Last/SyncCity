import unittest
from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.air_quality_raw_data import AirQualityRawData
from simulator.src.simulators.air_quality_simulator_strategy import \
    AirQualitySimulatorStrategy


class TestAirQualitySimulatorStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = MagicMock()

    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            AirQualitySimulatorStrategy(sensor_name='', config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'air_quality',
                'points_spacing': 'PT1H',
                'generation_delay': 'PT1H',
                'latitude': 0,
                'longitude': 0,
            }), producer=self.producer)

    def test_start(self) -> None:
        simulator = AirQualitySimulatorStrategy(sensor_name='test',
                                                config=SensorConfig({
                                                    'uuid': '00000000-0000-0000-0000-000000000000',
                                                    'type': 'air_quality',
                                                    'points_spacing': 'PT1S',
                                                    'generation_delay': 'PT1S',
                                                    'latitude': 0,
                                                    'longitude': 0,
                                                }), producer=self.producer)
        simulator.start()
        self.assertEqual(simulator.is_running(), True)
        simulator.stop()

    def test_stop(self) -> None:
        simulator = AirQualitySimulatorStrategy(sensor_name='test',
                                                config=SensorConfig({
                                                    'uuid': '00000000-0000-0000-0000-000000000000',
                                                    'type': 'air_quality',
                                                    'points_spacing': 'PT1S',
                                                    'generation_delay': 'PT1S',
                                                    'latitude': 0,
                                                    'longitude': 0,
                                                }), producer=self.producer)
        simulator.start()
        simulator.stop()
        self.assertEqual(simulator.is_running(), False)

    @unittest.mock.patch("random.uniform", return_value=0)
    def test_data(self, mock_uniform: MagicMock) -> None:
        simulator = AirQualitySimulatorStrategy(sensor_name='test',
                                                config=SensorConfig({
                                                    'uuid': '00000000-0000-0000-0000-000000000000',
                                                    'type': 'air_quality',
                                                    'begin_date': datetime(2024, 1, 1),
                                                    'points_spacing': 'PT1H',
                                                    'generation_delay': 'PT0S',
                                                    'limit': 3,
                                                    'latitude': 0,
                                                    'longitude': 0,
                                                }), producer=self.producer)

        mock_uniform.return_value = 0

        stream = [simulator.simulate() for _ in range(3)]

        expected = [
            AirQualityRawData(
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                no2=227.9631361756616,
                o3=113.9815680878308,
                pm10=56.9907840439154,
                pm25=75.98771205855387,
                so2=227.9631361756616,
            ),
            AirQualityRawData(
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
                no2=230.21252837182544,
                o3=115.10626418591272,
                pm10=57.55313209295636,
                pm25=76.73750945727515,
                so2=230.21252837182544,
            ),
            AirQualityRawData(
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
                no2=232.41734443743354,
                o3=116.20867221871677,
                pm10=58.104336109358385,
                pm25=77.47244814581119,
                so2=232.41734443743354,
            ),
        ]
        self.assertEqual(stream, expected)
