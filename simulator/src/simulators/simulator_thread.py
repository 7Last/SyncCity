import logging as log
import threading
import zoneinfo
from abc import ABC, abstractmethod
from datetime import datetime

from .simulator_strategy import SimulatorStrategy
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.raw_data import RawData
from ..producers.producer_strategy import ProducerStrategy


class SimulatorThread(threading.Thread):
    def __init__(self, simulator: SimulatorStrategy, producer: ProducerStrategy) -> None:
        self.__simulator = simulator
        self.__producer = producer
        self.__event = threading.Event()
        super().__init__(name=simulator.sensor_name())

    def run(self) -> None:
        while not self.__event.is_set() and (self.__simulator.limit is None or self.__simulator.limit > 0):
            self.__producer.produce(self.__simulator.simulate())
            log.debug(f'Produced data for {self.__simulator.sensor_name()}')
            if self.__simulator.limit is not None:
                self.__simulator.limit -= 1
            self.__event.wait(self.__simulator.generation_delay.total_seconds())

    def is_running(self) -> bool:
        return not self.__event.is_set()

    def stop(self) -> None:
        self.__event.set()
        log.debug(f'Stopped simulator {self.__simulator.sensor_name()}')