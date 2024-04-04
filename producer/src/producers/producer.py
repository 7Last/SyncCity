from abc import ABC, abstractmethod
from enum import Enum
import random


class Producer(ABC):

    class _Cities(Enum):
        """
        Enum with cities and their latitude, longitude and altitude above sea level.
        Used to simulate sensors located in different cities.
        """
        MUNICH = (48.1549958, 11.4594356, 520)
        MILAN = (45.4628246, 9.095332, 120)
        ZURICH = (47.3768866, 8.541694, 400)
        INNSBRUCK = (47.2692124, 11.4041024, 580)

    def __init__(self, sensor_id: str, frequency: int = 1000, limit: int = None):
        """
        Producer class that simulates raw data from sensors
        :param sensor_id: sensor identifier
        :param frequency: frequency in milliseconds to generate new data
        :param limit: maximum number of values to generate
        """
        self.sensor_id = sensor_id
        self.frequency = frequency
        self.limit = limit

    def stop(self):
        """
        Stop the producer
        """
        self.limit = 0

    def _gauss_value(self) -> float:
        mu = sum(self._range()) / 2
        # random.gauss is not thread safe without a lock
        return random.gauss(mu=mu, sigma=10)

    def _uniform_value(self) -> float:
        return random.uniform(*self._range())

    @abstractmethod
    async def produce(self):
        pass

    @abstractmethod
    def _range(self):
        """
        Range of acceptable values for the sensor
        :return: minimum and maximum values
        """
        pass
