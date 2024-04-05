from abc import ABC, abstractmethod
from enum import Enum
from ..models.raw_data import RawData
from datetime import datetime, timedelta


class Producer(ABC):

    def __init__(self, sensor_id: str, frequency: timedelta, latitude: float, longitude: float, limit: int = None,
                 begin_date: datetime = None):
        """
        Producer class that simulates raw data from sensors
        :param sensor_id: sensor identifier
        :param frequency:
        :param limit: maximum number of values to generate
        :param begin_date: Date to start generating data, if None, it will start from now

        """

        self.sensor_id = sensor_id
        self.frequency = frequency
        self.limit = limit
        self.latitude = latitude
        self.longitude = longitude
        self.running = False
        self.timestamp = begin_date or datetime.now()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    @abstractmethod
    async def stream(self) -> RawData:
        pass
