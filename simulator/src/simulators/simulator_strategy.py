import logging as log
import zoneinfo
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.raw_data import RawData


class SimulatorStrategy(ABC):

    def __init__(self, sensor_name: str, config: SensorConfig) -> None:
        log.info(f'Creating simulator for {sensor_name}')

        if not sensor_name or sensor_name == '':
            raise ValueError('sensor_name cannot be empty')

        self._sensor_name = sensor_name
        self._sensor_uuid = config.sensor_uuid()
        self._group_name = config.group_name()
        self._points_spacing = config.points_spacing()
        self._limit = config.limit()
        self._latitude = config.latitude()
        self._longitude = config.longitude()
        self._generation_delay = config.generation_delay()
        rome = zoneinfo.ZoneInfo('Europe/Rome')
        self._timestamp = config.begin_date() or datetime.now(tz=rome)

    def sensor_name(self) -> str:
        return self._sensor_name

    @property
    def limit(self) -> int:
        return self._limit

    @limit.setter
    def limit(self, limit: int) -> None:
        self._limit = limit

    @property
    def generation_delay(self) -> timedelta:
        return self._generation_delay

    @abstractmethod
    def simulate(self) -> RawData:
        pass

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, SimulatorStrategy):
            return False

        return super().__eq__(other) and \
            self._sensor_name == other._sensor_name and \
            self._sensor_uuid == other._sensor_uuid and \
            self._points_spacing == other._points_spacing and \
            self._limit == other._limit and \
            self._latitude == other._latitude and \
            self._longitude == other._longitude and \
            self._generation_delay == other._generation_delay and \
            self._timestamp == other._timestamp

    def __hash__(self) -> int:
        return hash((
            self._sensor_name,
            self._sensor_uuid,
            self._points_spacing,
            self._limit,
            self._latitude,
            self._longitude,
            self._generation_delay,
            self._timestamp,
        ))

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
