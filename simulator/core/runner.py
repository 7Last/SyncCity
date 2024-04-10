import signal
import logging as log
import threading
import concurrent.futures

from .simulators.simulator import Simulator


class Runner:

    def __init__(self, simulators: list[Simulator]) -> None:
        self.simulators = simulators
        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, _, __) -> None:  # noqa: ANN001
        log.info('Received shutdown signal, gracefully stopping...')
        for simulator in self.simulators:
            simulator.stop()

    @staticmethod
    def _callback(simulator: Simulator) -> None:
        simulator.start()
        log.info(
            f'Starting {simulator.sensor_id} '
            f'in thread {threading.current_thread().name}',
        )

        for item in simulator.stream():
            print(threading.current_thread().name, item.serialize())

    def run(self) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self._callback, self.simulators)
