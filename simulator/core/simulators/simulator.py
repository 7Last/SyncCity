from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from ..models.raw_data.raw_data import RawData


class Simulator(ABC):

    def __init__(self, *, sensor_id: str,
                 points_spacing: timedelta, latitude: float,
                 longitude: float, limit: int = None,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        """Simulator class that simulates raw data from sensors
        :param sensor_id: sensor identifier
        :param generation_delay: time to wait between the generation
        of a point and the next one
        :param points_spacing: how spaced in time are the data points
        :param latitude: latitude of the sensor
        :param longitude: longitude of the sensor
        :param points_spacing: how spaced in time are the data points
        :param limit: maximum number of values to generate
        :param begin_date: Date to start generating data, if None, now is assumed
        """

        if not sensor_id or sensor_id == '':
            raise ValueError('sensor_id cannot be empty')

        self.sensor_id = sensor_id
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
    async def stream(self) -> RawData:
        pass
