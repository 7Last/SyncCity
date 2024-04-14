import random
import time
from datetime import datetime, timedelta
from math import e, pi, sqrt
from typing import Iterable
from uuid import UUID

from .simulator import Simulator
from ..models.raw_data.traffic_raw_data import TrafficRawData


class TrafficSimulator(Simulator):
    _SPEED_MULTIPLICATIVE_FACTOR = 100
    _VEHICLES_MULTIPLICATIVE_FACTOR = 200

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 latitude: float, longitude: float,
                 points_spacing: timedelta, limit: int = None,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        super().__init__(sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         points_spacing=points_spacing,
                         generation_delay=generation_delay, limit=limit,
                         begin_date=begin_date, latitude=latitude, longitude=longitude)

    def stream(self) -> Iterable[TrafficRawData]:
        while self.limit != 0 and self.running:
            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.frequency
            time.sleep(self.delay.total_seconds())

            speed = self._SPEED_MULTIPLICATIVE_FACTOR * _multimodal_gauss_value(
                x=self.timestamp.hour + self.timestamp.minute / 60,
                modes=[
                    (0, 2.1),
                    (4, 2.2),
                    (13, 3),
                    (21, 3),
                    (24, 3),
                ],
            )

            vehicles = self._VEHICLES_MULTIPLICATIVE_FACTOR * _multimodal_gauss_value(
                x=self.timestamp.hour + self.timestamp.minute / 60,
                modes=[
                    (0, 4),
                    (8.5, 1.8),
                    (13, 2),
                    (17.5, 1.7),
                    (21, 3),
                ],
            )

            yield TrafficRawData(
                vehicles_per_hour=vehicles,
                avg_speed=speed,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
                sensor_uuid=self.sensor_uuid,
            )


def _multimodal_gauss_value(x: float, modes: list[tuple[float, float]]) -> float:
    """Returns generates a random x in a range and calculates its corresponding y
    from a bimodal Gaussian distribution.
    :param modes: list of tuples with the mu and sigma values for each mode
    :param x: Value for x to calculate the probability
    """
    random_factor = random.uniform(0, 0.01)

    # add a vertical shift to the distribution
    shift = 0.1

    def density_func(mu: float, sigma: float) -> float:
        return 1 / (sigma * sqrt(2 * pi)) * e ** (-(x - mu) ** 2 / (2 * sigma ** 2))

    return sum([density_func(mu, sigma) for mu, sigma in modes], random_factor + shift)
