import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.raw_data.charging_station_raw_data import \
    ChargingStationRawData
from simulator.src.simulators.charging_station_simulator import ChargingStationSimulator


class TestChargingStationSimulator(unittest.TestCase):
    def setUp(self) -> None:
        self.producer = MagicMock()

    def test_empty_sensor_name(self) -> None:
        with self.assertRaises(ValueError):
            ChargingStationSimulator(
                sensor_name='',
                config=SensorConfig({
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'type': 'charging_station',
                    'points_spacing': 'PT1H',
                    'generation_delay': 'PT1H',
                    'latitude': 0,
                    'longitude': 0,
                }),
                producer=self.producer,
            )

    @patch('random.random', return_value=0)
    @patch('random.choices', side_effect=[[11], ['car'], ['car'], ['car']])
    @patch('random.uniform', side_effect=[3, 50, 2, 80, 1, 20])
    def test_data(self, _: Mock, __: Mock, ___: Mock) -> None:
        simulator = ChargingStationSimulator(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'charging_station',
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
            ChargingStationRawData(
                kwh_supplied=0,
                remaining_charge_time=0,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 0, 0, 0),
                vehicle_type='bike',
                battery_level=100,
                elapsed_time=0,
            ),
            ChargingStationRawData(
                kwh_supplied=0,
                remaining_charge_time=0,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 1, 0, 0),
                vehicle_type='bike',
                battery_level=100,
                elapsed_time=3600,
            ),
            ChargingStationRawData(
                kwh_supplied=0,
                remaining_charge_time=0,
                sensor_uuid=UUID('00000000-0000-0000-0000-000000000000'),
                sensor_name='test',
                latitude=0,
                longitude=0,
                timestamp=datetime(2024, 1, 1, 2, 0, 0),
                vehicle_type='bike',
                battery_level=100,
                elapsed_time=7200,
            ),
        ]

        self.assertEqual(stream, expected)
