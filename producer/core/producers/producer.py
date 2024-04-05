from abc import ABC, abstractmethod
from enum import Enum
from ..models.raw_data import RawData
from datetime import datetime, timedelta


class Producer(ABC):
    class _City(Enum):
        """
        Enum with cities and their latitude, longitude and altitude above sea level.
        Used to simulate sensors located in different cities.
        """
        MUNICH = (48.1549958, 11.4594356, 520)
        INNSBRUCK = (47.2692124, 11.4041024, 580)
        PADUA = (45.4064349, 11.8767611, 12)
        MESTRE = (45.4909825, 12.2459022, 3)
        ZURICH = (47.3768866, 8.541694, 400)

    def __init__(self, sensor_id: str, frequency: timedelta, limit: int = None, begin_date: datetime = None):
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
        self.running = False
        self.timestamp = begin_date or datetime.now()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    @abstractmethod
    async def stream(self) -> RawData:
        pass
