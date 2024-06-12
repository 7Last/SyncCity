import unittest
from datetime import timedelta, datetime
from uuid import UUID

from simulator.src.models.config.simulator_factory import simulators_generator
from simulator.src.simulators.temperature_simulator import TemperatureSimulator
from simulator.src.simulators.traffic_simulator import TrafficSimulator


class TestSimulatorFactory(unittest.TestCase):
    def test_simulator_generator(self) -> None:
        sensors = {
            "sensor1": {
                "type": "temperature",
                "_sensor_uuid": "366a08e8-57aa-4592-a89a-c292f26848c8",
                "_generation_delay": "PT1S",
                "_points_spacing": "PT2S",
                "_latitude": 0,
                "_longitude": 0,
                "begin_date": datetime(2022, 1, 1),
            },
            "sensor2": {
                "type": "traffic",
                "_sensor_uuid": "456a08e8-57aa-4592-a89a-c292f26848c8",
                "_generation_delay": "PT6S",
                "_points_spacing": "PT7S",
                "_latitude": 0,
                "_longitude": 0,
                "begin_date": datetime(2022, 2, 2),
            },
        }

        simulators = sorted(simulators_generator(sensors), key=lambda x: x.sensor_name)
        expected = [
            TemperatureSimulator(
                sensor_name="sensor1",
                sensor_uuid=UUID("366a08e8-57aa-4592-a89a-c292f26848c8"),
                generation_delay=timedelta(seconds=1),
                points_spacing=timedelta(seconds=2),
                latitude=0,
                longitude=0,
                begin_date=datetime(2022, 1, 1),
            ),
            TrafficSimulator(
                sensor_name="sensor2",
                sensor_uuid=UUID("456a08e8-57aa-4592-a89a-c292f26848c8"),
                generation_delay=timedelta(seconds=6),
                points_spacing=timedelta(seconds=7),
                latitude=0,
                longitude=0,
                begin_date=datetime(2022, 2, 2),
            ),
        ]

        self.assertEqual(simulators, expected)

    def test_not_implemented_error(self) -> None:
        sensors = {
            "sensor1": {
                "type": "not_implemented",
                "_sensor_uuid": "366a08e8-57aa-4592-a89a-c292f26848c8",
                "_generation_delay": "PT1S",
                "_points_spacing": "PT2S",
                "_latitude": 0,
                "_longitude": 0,
                "begin_date": "2022-01-01T00:00:00",
            },
        }

        with self.assertRaises(KeyError):
            list(simulators_generator(sensors))
