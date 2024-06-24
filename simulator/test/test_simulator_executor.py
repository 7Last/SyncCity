import unittest.mock
from unittest.mock import MagicMock

from simulator.src.producers.stdout_producer import StdOutProducer
from simulator.src.simulator_executor import SimulatorExecutor
from simulator.src.simulators.temperature_simulator import TemperatureSimulator


class TestSimulatorExecutor(unittest.TestCase):

    @unittest.mock.patch(
        "simulator.src.simulator_executor.build_simulators",
    )
    @unittest.mock.patch(
        "simulator.src.simulator_executor.threading.Event",
    )
    def test_run(self, _: MagicMock,
                 mock_build_simulators: MagicMock) -> None:  # noqa: PLR6301
        simulator_mock = MagicMock(spec=TemperatureSimulator)
        simulator_mock.start = MagicMock()
        simulator_mock.sensor_name = "test"

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
    def test_stop_all(self, _: MagicMock, __: MagicMock) -> None:
        simulator_mock = MagicMock(spec=TemperatureSimulator)
        simulator_mock.stop = MagicMock()

        mock_producer = MagicMock(spec=StdOutProducer)

        executor = SimulatorExecutor({}, mock_producer)
        executor._simulators = [simulator_mock]

        executor._stop_all()
        simulator_mock.stop.assert_called_once()
