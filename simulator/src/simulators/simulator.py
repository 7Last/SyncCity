from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from uuid import UUID

from ..models.raw_data.raw_data import RawData
from typing import Iterable


class Simulator(ABC):

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 points_spacing: timedelta, latitude: float, longitude: float,
                 limit: int = None, generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        """Simulator class that simulates raw data from sensors
        :param generation_delay: time to wait between the generation
        of a point and the next one
        :param points_spacing: how spaced in time are the data points
        :param points_spacing: how spaced in time are the data points
        :param limit: maximum number of values to generate
        :param begin_date: Date to start generating data, if None, now is assumed
        """

        if not sensor_name or sensor_name == '':
            raise ValueError('sensor_name cannot be empty')

        self.sensor_name = sensor_name
        self.sensor_uuid = sensor_uuid
        self.frequency = points_spacing
        self.limit = limit
        self.latitude = latitude
        self.longitude = longitude
        self.running = False
        self.delay = generation_delay
        self.timestamp = begin_date or datetime.now()

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    @abstractmethod
    def stream(self) -> Iterable[RawData]:
        pass
