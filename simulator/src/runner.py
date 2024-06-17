import logging as log
import threading
from typing import Dict

from .models.config.simulator_factory import build_simulators
from .producers.producer_strategy import ProducerStrategy


class Runner:
    def __init__(self, config: Dict[str, any], producer: ProducerStrategy) -> None:
        self._simulators = build_simulators(config, producer)
        self._stop_event = threading.Event()

    def _stop(self) -> None:
        self._stop_event.set()
        log.debug("Stopping simulator threads")
        for simulator in self._simulators:
            simulator.stop()
        log.info("Simulators stopped.")

    def run(self) -> None:
        try:
            for simulator in self._simulators:
                log.debug(f"Starting simulator: {simulator.sensor_name}")
                simulator.start()

            self._stop_event.wait()  # Keep the main thread alive
        except KeyboardInterrupt:
            log.info("KeyboardInterrupt received")
            self._stop()
        except Exception as e:
            log.error(f"An error occurred: {e}")
            self._stop()
