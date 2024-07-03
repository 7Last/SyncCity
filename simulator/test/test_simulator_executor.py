import unittest.mock
from unittest.mock import MagicMock

from simulator.src.producers.stdout_producer import StdOutProducer
from simulator.src.simulator_executor import SimulatorExecutor
from simulator.src.simulators.temperature_simulator_strategy import \
    TemperatureSimulatorStrategy


class TestSimulatorExecutor(unittest.TestCase):

    @unittest.mock.patch(
        "simulator.src.simulator_executor.build_simulators",
    )
    @unittest.mock.patch(
        "simulator.src.simulator_executor.threading.Event",
    )
    def test_run(self, _: MagicMock,
                 mock_build_simulators: MagicMock) -> None:
        simulator_mock = MagicMock(spec=TemperatureSimulatorStrategy)
        simulator_mock.start = MagicMock()
        simulator_mock.sensor_name.return_value = "test"

        mock_build_simulators.return_value = [simulator_mock]

        mock_producer = MagicMock(spec=StdOutProducer)

        executor = SimulatorExecutor({}, mock_producer)
        executor.run()
        simulator_mock.start.assert_called_once()

    @unittest.mock.patch(
        "simulator.src.simulator_executor.build_simulators",
    )
    @unittest.mock.patch(
        "simulator.src.simulator_executor.threading.Event",
    )
    def test_stop_all(self, _: MagicMock, build_simulators_mock: MagicMock) -> None:
        simulator_mock = MagicMock(spec=TemperatureSimulatorStrategy)
        simulator_mock.stop = MagicMock()
        simulator_mock.start = MagicMock()

        build_simulators_mock.return_value = [simulator_mock]

        mock_producer = MagicMock(spec=StdOutProducer)
        executor = SimulatorExecutor({}, mock_producer)

        executor.stop_all()
        simulator_mock.stop.assert_called_once()
