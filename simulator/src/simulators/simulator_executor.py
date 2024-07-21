import logging as log
import threading
from typing import Dict

from .simulator_thread import SimulatorThread
from ..producers.producer_strategy import ProducerStrategy
from .simulator_factory import build_simulators


class SimulatorExecutor:
    def __init__(self, config: Dict[str, any], producer: ProducerStrategy) -> None:
        self.__simulator_threads: list[SimulatorThread] = [
            SimulatorThread(simulator, producer)
            for simulator in build_simulators(config)
        ]
        self.__stop_event = threading.Event()

    def stop_all(self) -> None:
        self.__stop_event.set()
        log.debug("Stopping simulator threads")
        for simulator in self.__simulator_threads:
            simulator.stop()
        log.info("Simulators stopped.")

    def run(self) -> None:
        try:
            for simulator in self.__simulator_threads:
                log.debug(f"Starting simulator:{simulator.name}")
                simulator.start()

            self.__stop_event.wait()  # Keep the main thread alive
        except KeyboardInterrupt:
            log.info("KeyboardInterrupt received")
            self.stop_all()
        except Exception as e:
            log.error(f"An error occurred: {e}")
            self.stop_all()
