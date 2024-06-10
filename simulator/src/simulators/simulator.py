import threading
import zoneinfo
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Iterable
from uuid import UUID
import logging as log

from ..models.raw_data.raw_data import RawData


class Simulator(ABC):

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 points_spacing: timedelta, latitude: float, longitude: float,
                 limit: int = None, generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        """Simulator class that simulates raw data from sensors
        :param generation_delay: time to wait between the generation
        of a point and the next one
        :param points_spacing: how spaced in time are the data points
        :param limit: maximum number of values to generate
        :param begin_date: Date to start generating data, if None, now is assumed
        """

        if not sensor_name or sensor_name == '':
            raise ValueError('sensor_name cannot be empty')

        self.sensor_name = sensor_name
        self.sensor_uuid = sensor_uuid
        self.points_spacing = points_spacing
        self.limit = limit
        self.latitude = latitude
        self.longitude = longitude
        self.running = False
        self.generation_delay = generation_delay
        rome = zoneinfo.ZoneInfo('Europe/Rome')
        self.timestamp = begin_date or datetime.now(tz=rome)
        self._event = threading.Event()

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self._event.set()
        log.debug(f'Emitted event to {self.sensor_name}')
        self.running = False

    @abstractmethod
    def stream(self) -> Iterable[RawData]:
        pass

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, Simulator):
            return False

        return self.sensor_name == other.sensor_name and \
            self.sensor_uuid == other.sensor_uuid and \
            self.points_spacing == other.points_spacing and \
            self.limit == other.limit and \
            self.latitude == other.latitude and \
            self.longitude == other.longitude and \
            self.running == other.running and \
            self.generation_delay == other.generation_delay and \
            self.timestamp == other.timestamp

    def __hash__(self) -> int:
        return hash((
            self.sensor_name,
            self.sensor_uuid,
            self.points_spacing,
            self.limit,
            self.latitude,
            self.longitude,
            self.running,
            self.generation_delay,
            self.timestamp,
        ))

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
