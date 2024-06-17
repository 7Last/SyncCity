import logging as log
import threading
import zoneinfo
from abc import ABC, abstractmethod
from datetime import datetime

from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.raw_data import RawData
from ..producers.producer_strategy import ProducerStrategy


class Simulator(ABC, threading.Thread):

    def __init__(self, sensor_name: str, config: SensorConfig,
                 producer: ProducerStrategy) -> None:
        log.info(f'Creating simulator for {sensor_name}')

        if not sensor_name or sensor_name == '':
            raise ValueError('sensor_name cannot be empty')

        self.sensor_name = sensor_name
        self._sensor_uuid = config.sensor_uuid
        self._group_name = config.group_name
        self._points_spacing = config.points_spacing
        self._limit = config.limit
        self._latitude = config.latitude
        self._longitude = config.longitude
        self._generation_delay = config.generation_delay
        rome = zoneinfo.ZoneInfo('Europe/Rome')
        self._timestamp = config.begin_date or datetime.now(tz=rome)
        self._producer = producer
        self._event = threading.Event()
        super().__init__(name=sensor_name)

    def run(self) -> None:
        while not self._event.is_set() and (self._limit is None or self._limit > 0):
            data = self.data()
            self._producer.produce(data)
            log.debug(f'Produced data for {self.sensor_name}')
            if self._limit is not None:
                self._limit -= 1
            self._event.wait(self._generation_delay.total_seconds())

    def is_running(self) -> bool:
        return not self._event.is_set()

    def stop(self) -> None:
        self._event.set()
        log.debug(f'Stopped simulator {self.sensor_name}')

    @abstractmethod
    def data(self) -> RawData:
        pass

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, Simulator):
            return False

        return super().__eq__(other) and \
            self.sensor_name == other.sensor_name and \
            self._sensor_uuid == other._sensor_uuid and \
            self._points_spacing == other._points_spacing and \
            self._limit == other._limit and \
            self._latitude == other._latitude and \
            self._longitude == other._longitude and \
            self._generation_delay == other._generation_delay and \
            self._timestamp == other._timestamp

    def __hash__(self) -> int:
        return hash((
            self.sensor_name,
            self._sensor_uuid,
            self._points_spacing,
            self._limit,
            self._latitude,
            self._longitude,
            self._generation_delay,
            self._timestamp,
        ))

    def __str__(self) -> str:
        return f'self.__class__.__name__ {self.__dict__}'
