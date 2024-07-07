import unittest
from datetime import datetime
from unittest.mock import MagicMock

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.simulators.simulator_factory import build_simulators
from simulator.src.simulators.temperature_simulator_strategy import \
    TemperatureSimulatorStrategy
from simulator.src.simulators.traffic_simulator_strategy import TrafficSimulatorStrategy


class TestSimulatorFactory(unittest.TestCase):
    def test_simulator_generator(self) -> None:
        mock_producer = MagicMock()

        config = {
            "sensor1": {
                "type": "temperature",
                "uuid": "366a08e8-57aa-4592-a89a-c292f26848c8",
                "generation_delay": "PT1S",
                "points_spacing": "PT2S",
                "latitude": 1,
                "longitude": 1,
                "begin_date": datetime(2022, 1, 1),
            },
            "sensor2": {
                "type": "traffic",
                "uuid": "456a08e8-57aa-4592-a89a-c292f26848c8",
                "generation_delay": "PT6S",
                "points_spacing": "PT7S",
                "latitude": 0,
                "longitude": 0,
                "begin_date": datetime(2022, 2, 2),
            },
        }

        simulators = sorted(build_simulators(config, mock_producer),
                            key=lambda x: x.sensor_name())
        expected = [
            TemperatureSimulatorStrategy(
                sensor_name="sensor1",
                config=SensorConfig(
                    {
                        "uuid": "366a08e8-57aa-4592-a89a-c292f26848c8",
                        "begin_date": datetime(2022, 1, 1),
                        "latitude": 1,
                        "longitude": 1,
                        "type": "temperature",
                        "generation_delay": "PT1S",
                        "points_spacing": "PT2S",
                    },
                ),
                producer=mock_producer,
            ),
            TrafficSimulatorStrategy(
                sensor_name="sensor2",
                config=SensorConfig(
                    {
                        "uuid": "456a08e8-57aa-4592-a89a-c292f26848c8",
                        "begin_date": datetime(2022, 2, 2),
                        "latitude": 0,
                        "longitude": 0,
                        "type": "traffic",
                        "generation_delay": "PT6S",
                        "points_spacing": "PT7S",
                    },
                ),
                producer=mock_producer,
            ),
        ]

        self.assertEqual(simulators, expected)

    def test_not_implemented_error(self) -> None:
        mock_producer = MagicMock()
        sensors = {
            "sensor1": {
                "type": "not_implemented",
                "uuid": "366a08e8-57aa-4592-a89a-c292f26848c8",
                "generation_delay": "PT1S",
                "points_spacing": "PT2S",
                "latitude": 0,
                "longitude": 0,
                "begin_date": "2022-01-01T00:00:00",
            },
        }

        with self.assertRaises(KeyError):
            list(build_simulators(sensors, mock_producer))
