import unittest
import isodate.isoerror
from datetime import datetime, timedelta
from uuid import UUID

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.models.sensor_type import SensorType


class TestSensorConfig(unittest.TestCase):
    def test_valid_config(self) -> None:
        config = SensorConfig({
            "_sensor_uuid": "00000000-0000-0000-0000-000000000000",
            "_limit": 10,
            "begin_date": datetime(2024, 1, 1, 0, 0, 0),
            "_latitude": 0.0,
            "_longitude": 0.0,
            "type": "TRAFFIC",
            "_generation_delay": "PT1H",
            "_points_spacing": "PT1H",
        })
        self.assertEqual(config.sensor_uuid, UUID("00000000-0000-0000-0000-000000000000"))
        self.assertEqual(config.limit, 10)
        self.assertEqual(config.begin_date, datetime(2024, 1, 1, 0, 0, 0))
        self.assertEqual(config.latitude, 0.0)
        self.assertEqual(config.longitude, 0.0)
        self.assertEqual(config.type, SensorType.TRAFFIC)
        self.assertEqual(config.generation_delay, timedelta(hours=1))
        self.assertEqual(config.points_spacing, timedelta(hours=1))

    def test_invalid_type(self) -> None:
        config = {
            "_sensor_uuid": "00000000-0000-0000-0000-000000000000",
            "_limit": 10,
            "begin_date": "2024-01-01T00:00:00",
            "_latitude": 0.0,
            "_longitude": 0.0,
            "type": "INVALID",
            "_generation_delay": "PT1H",
            "_points_spacing": "PT1H",
        }
        with self.assertRaises(KeyError):
            SensorConfig(config)

    def test_missing_type(self) -> None:
        config = {
            "_sensor_uuid": "00000000-0000-0000-0000-000000000000",
            "_limit": 10,
            "begin_date": "2024-01-01T00:00:00",
            "_latitude": 0.0,
            "_longitude": 0.0,
            "_generation_delay": "PT1H",
            "_points_spacing": "PT1H",
        }
        with self.assertRaisesRegex(
                Exception,
                'type must not be empty',
        ):
            SensorConfig(config)

    def test_invalid_points_spacing(self) -> None:
        config = {
            "_sensor_uuid": "00000000-0000-0000-0000-000000000000",
            "_limit": 10,
            "begin_date": "2024-01-01T00:00:00",
            "_latitude": 0.0,
            "_longitude": 0.0,
            "type": "TRAFFIC",
            "_generation_delay": "PT1H",
            "_points_spacing": "INVALID",
        }

        with self.assertRaises(isodate.isoerror.ISO8601Error):
            SensorConfig(config)

    def test_invalid_generation_delay(self) -> None:
        config = {
            "_sensor_uuid": "00000000-0000-0000-0000-000000000000",
            "_limit": 10,
            "begin_date": "2024-01-01T00:00:00",
            "_latitude": 0.0,
            "_longitude": 0.0,
            "type": "TRAFFIC",
            "_generation_delay": "INVALID",
            "_points_spacing": "PT1H",
        }

        with self.assertRaises(isodate.isoerror.ISO8601Error):
            SensorConfig(config)
