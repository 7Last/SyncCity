import unittest
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.charging_station_raw_data import \
    ChargingStationRawData


class TestChargingStationRawData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.timestamp = datetime(2024, 1, 1, 0, 0, 0)

    def test_topic(self) -> None:
        data = ChargingStationRawData(
            sensor_name="charging_station",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self._timestamp,
            kwh_supplied=0,
            remaining_charge_time=0,
            vehicle_type="car",
            battery_level=0,
            elapsed_time=0,
        )

        self.assertEqual(data.topic, "charging_station")

    def test_subject(self) -> None:
        data = ChargingStationRawData(
            sensor_name="charging_station",
            sensor_uuid=UUID("00000000-0000-0000-0000-000000000000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self._timestamp,
            kwh_supplied=0,
            remaining_charge_time=0,
            vehicle_type="car",
            battery_level=0,
            elapsed_time=0,
        )

        self.assertEqual(data.value_subject(), "charging_station-value")
