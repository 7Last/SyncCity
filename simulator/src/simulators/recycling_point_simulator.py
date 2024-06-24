import random
from typing import List, Tuple

from .simulator import Simulator
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from ..producers.producer_strategy import ProducerStrategy


class RecyclingPointSimulator(Simulator):

    def __init__(self, sensor_name: str, config: SensorConfig,
                 producer: ProducerStrategy) -> None:
        super().__init__(sensor_name, config, producer)

        self._last_value = random.uniform(0, 30)
        self._prev_timestamp = self._timestamp
        self._fill_rate = 0
        self._emptying_hours = _generate_emptying_hours()
        self._noise_limit = random.uniform(-5, 5)
        self._partial_emptying_chance = random.uniform(0.0, 0.15)
        # max percentage of value to leave after partial emptying
        self._partial_emptying_max_percentage = random.uniform(0.05, 0.3)

    def data(self) -> RecyclingPointRawData:
        data = RecyclingPointRawData(
            filling=self._last_value,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            sensor_uuid=self._sensor_uuid,
            sensor_name=self.sensor_name,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def _calculate_fill_rate(self) -> None:
        elapsed_time = self._timestamp - self._prev_timestamp
        fill_rate_per_hour = random.uniform(0.8, 1.2)
        fill_rate_per_second = fill_rate_per_hour / 3600
        self._fill_rate = fill_rate_per_second * elapsed_time.total_seconds()

    def _filling(self) -> float:
        # update fill rate
        self._calculate_fill_rate()

        # update previous timestamp
        self._prev_timestamp = self._timestamp

        # check if it is time to empty
        if (self._timestamp.weekday(), self._timestamp.hour) in self._emptying_hours:
            # 10% chance for partial emptying
            if random.random() < self._partial_emptying_chance:
                # leave up to 30% of current value
                self._last_value *= random.uniform(
                    0.0, self._partial_emptying_max_percentage)
            else:
                self._last_value = 0.0  # complete emptying
            return self._last_value

        # calculate new value
        new_value = self._last_value + self._fill_rate

        # adding some noise
        noise = random.uniform(-self._noise_limit, self._noise_limit)
        new_value = max(self._last_value, new_value + noise)

        # check value over 100
        new_value = min(new_value, 100.0)

        # update last value
        self._last_value = new_value

        return new_value

    def __str__(self) -> str:
        return 'self.__class__.__name__ self.__dict__'


def _generate_emptying_hours() -> List[Tuple[int, int]]:
    # Possible emptying schedules with hours between 4 AM and 8 AM
    def random_hour() -> int:
        return random.randint(4, 8)

    schedules = [
        # Monday, Friday
        [(0, random_hour()), (4, random_hour())],
        # Tuesday, Saturday
        [(1, random_hour()), (5, random_hour())],
        # Monday, Wednesday, Saturday
        [(0, random_hour()), (2, random_hour()), (5, random_hour())],
        # Monday, Thursday, Saturday
        [(0, random_hour()), (3, random_hour()), (5, random_hour())],
    ]
    return random.choice(schedules)
