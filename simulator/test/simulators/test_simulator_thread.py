import unittest.mock
from datetime import datetime
from unittest.mock import MagicMock

from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.producers.stdout_producer import StdOutProducer
from simulator.src.simulators.simulator_executor import SimulatorExecutor
from simulator.src.simulators.temperature_simulator_strategy import \
    TemperatureSimulatorStrategy


class TestSimulatorThread(unittest.TestCase):
    def test_produce(self):
        mock_producer = MagicMock()
        mock_producer.produce = MagicMock()

        temperature = TemperatureSimulatorStrategy(
            sensor_name='test',
            config=SensorConfig({
                'uuid': '00000000-0000-0000-0000-000000000000',
                'type': 'temperature',
                'begin_date': datetime(2024, 1, 1),
                'points_spacing': 'PT1H',
                'generation_delay': 'PT0S',
                'limit': 3,
                'latitude': 0,
                'longitude': 0,
            }),
        )
