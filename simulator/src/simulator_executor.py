import logging as log
import threading
from typing import Dict

from .producers.producer_strategy import ProducerStrategy
from .simulator_factory import build_simulators
from .simulators.simulator_strategy import SimulatorStrategy


class SimulatorExecutor:
    def __init__(self, config: Dict[str, any], producer: ProducerStrategy) -> None:
        self.__simulators: list[SimulatorStrategy] = build_simulators(config, producer)
        self._stop_event = threading.Event()

    def _stop_all(self) -> None:
        self._stop_event.set()
        log.debug("Stopping simulator threads")
        for simulator in self.__simulators:
            simulator.stop()
        log.info("Simulators stopped.")

    def run(self) -> None:
        try:
            for simulator in self.__simulators:
                log.debug(f"Starting simulator:{simulator.sensor_name()}")
                simulator.start()

            self._stop_event.wait()  # Keep the main thread alive
        except KeyboardInterrupt:
            log.info("KeyboardInterrupt received")
            self._stop_all()
        except Exception as e:
            log.error(f"An error occurred: {e}")
            self._stop_all()
