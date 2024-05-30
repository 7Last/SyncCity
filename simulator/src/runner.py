import concurrent.futures as concurrent
import logging as log
import threading

from .producers.producer_strategy import ProducerStrategy
from .simulators.simulator import Simulator


class Runner:
    def __init__(self, *, simulators: list[Simulator], producer: ProducerStrategy)\
            -> None:
        self._simulators = simulators
        self._producer = producer

    def _callback(self, simulator: Simulator) -> None:
        simulator.start()
        thread = threading.current_thread().name
        log.info(f'Starting {simulator.sensor_name} in {thread}')

        try:
            for item in simulator.stream():
                self._producer.produce(item)
        except Exception as e:
            log.exception('Error while producing data', e)

    def run(self) -> None:
        try:
            log.debug("Creating thread pool with %d workers", len(self._simulators))
            with concurrent.ThreadPoolExecutor() as executor:
                executor.map(self._callback, self._simulators)
        except KeyboardInterrupt:
            log.info('Received shutdown signal, gracefully stopping...')
            for simulator in self._simulators:
                log.debug(f'Stopping {simulator.sensor_name}')
                simulator.stop()
        except Exception as e:
            log.exception('Error while running simulator', e)
        finally:
            self._producer.close()
            log.debug('ProducerStrategy closed, exiting.')
