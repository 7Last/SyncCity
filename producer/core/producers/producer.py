from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from ..models.raw_data import RawData

class Producer(ABC):

    def __init__(self, *, sensor_id: str, frequency: timedelta, latitude: float,
                 longitude: float, limit: int = None,
                 begin_date: datetime = None) -> None:
        """Producer class that simulates raw data from sensors
        :param sensor_id: sensor identifier
        :param frequency:
        :param limit: maximum number of values to generate
        :param begin_date: Date to start generating data, if None, now is assumed

        """
        self.sensor_id = sensor_id
        self.frequency = frequency
        self.limit = limit
        self.latitude = latitude
        self.longitude = longitude
        self.running = False
        self.timestamp = begin_date or datetime.now()

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    @abstractmethod
    async def stream(self) -> RawData:
        pass
