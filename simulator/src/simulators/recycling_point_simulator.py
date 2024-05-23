import random
from datetime import datetime, timedelta
from typing import Iterable, List, Tuple
from uuid import UUID

from .simulator import Simulator
from ..models.raw_data.recycling_point_raw_data import RecyclingPointRawData


class RecyclingPointSimulator(Simulator):

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 latitude: float, longitude: float,
                 points_spacing: timedelta, limit: int = None,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        super().__init__(sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         points_spacing=points_spacing,
                         generation_delay=generation_delay, limit=limit,
                         begin_date=begin_date, latitude=latitude, longitude=longitude)
        # last value
        self.last_value = random.uniform(0, 30)
        # previous value's timestamp
        self.prev_timestamp = self.timestamp
        # filling rate
        self.fill_rate = 0
        # emptying days and hours per week
        self.emptying_hours = _generate_emptying_hours()
        # noise rate
        self.noise_limit = random.uniform(-5, 5)
        # chance for partial emptying
        self.partial_emptying_chance = random.uniform(0.0, 0.15)
        # max percentage of value to leave after partial emptying
        self.partial_emptying_max_percentage = random.uniform(0.05, 0.3)

    def stream(self) -> Iterable[RecyclingPointRawData]:
        while self.limit != 0 and self.running:
            self.last_value = self._filling_value()

            yield RecyclingPointRawData(
                filling_value=self.last_value,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
                sensor_uuid=self.sensor_uuid,
                sensor_name=self.sensor_name,
            )

            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.frequency
            self._event.wait(self.delay.total_seconds())

    def _calculate_fill_rate(self) -> None:
        time_passed = self.timestamp - self.prev_timestamp
        fill_rate_per_hour = random.uniform(0.8, 1.2)  # 1.0416666666672
        fill_rate_per_second = fill_rate_per_hour / 3600
        self.fill_rate = fill_rate_per_second * time_passed.total_seconds()

    def _filling_value(self) -> float:
        # update fill rate
        self._calculate_fill_rate()

        # update previuos timestamp
        self.prev_timestamp = self.timestamp

        # check if it is time to empty
        if (self.timestamp.weekday(), self.timestamp.hour) in self.emptying_hours:
            # 10% chance for partial emptying
            if random.random() < self.partial_emptying_chance:
                # leave up to 30% of current value
                self.last_value *= random.uniform(
                    0.0, self.partial_emptying_max_percentage)
            else:
                self.last_value = 0.0  # complete emptying
            return self.last_value

        # calculate new value
        new_value = self.last_value + self.fill_rate

        # adding some noise
        noise = random.uniform(-self.noise_limit, self.noise_limit)
        new_value = max(self.last_value, new_value + noise)

        # check value over 100
        new_value = min(new_value, 100.0)

        # update last value
        self.last_value = new_value

        return new_value


def _generate_emptying_hours() -> List[Tuple[int, int]]:
    # Possible emptying schedules with hours between 4 AM and 8 AM
    def random_hour() -> int:
        return random.randint(4, 8)  # Hours between 4 and 8 AM

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
