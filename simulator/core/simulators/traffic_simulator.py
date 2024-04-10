from math import e, pi, sqrt
from typing import Iterable
from datetime import datetime, timedelta
import time
import random

from .simulator import Simulator
from ..models.raw_data.traffic_raw_data import TrafficRawData


class TrafficSimulator(Simulator):
    _MULTIPLICATIVE_FACTOR = 400
    _MAX_SPEED = 80

    def __init__(self, *, latitude: float, longitude: float, sensor_id: str,
                 points_spacing: timedelta, limit: int = None,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        super().__init__(sensor_id=sensor_id, points_spacing=points_spacing,
                         generation_delay=generation_delay, limit=limit,
                         begin_date=begin_date, latitude=latitude, longitude=longitude)

    def stream(self) -> Iterable[TrafficRawData]:
        while self.limit != 0 and self.running:
            self.limit -= 1
            self.timestamp += self.frequency
            time.sleep(self.delay.total_seconds())

            probability = _multimodal_normal_gauss_value(
                x=self.timestamp.hour + self.timestamp.minute / 60,
                modes=[
                    (8.5, 0.425),  # 8:30 AM
                    (12.5, 1.88),  # 12:30 PM
                    (18, 0.38),  # 6 PM
                ],
                max_x=18,
            )

            # speed per unit depends on vehicles_per_minute, many vehicles -> low speed
            # few vehicles -> high speed
            vehicles_per_minute = round(self._MULTIPLICATIVE_FACTOR * probability)

            yield TrafficRawData(
                vehicles_per_minute=vehicles_per_minute,
                avg_speed_per_minute=round(self._MAX_SPEED - vehicles_per_minute, 2),
                latitude=self.latitude,
                longitude=self.longitude,
                sensor_id=self.sensor_id,
                timestamp=self.timestamp,
            )


def _multimodal_normal_gauss_value(x: float, modes: list[tuple[float, float]],
                                   max_x: float) -> float:
    """Returns generates a random x in a range and calculates its corresponding y
    from a bimodal Gaussian distribution.
    :param modes: list of tuples with the mu and sigma values for each mode
    :param x: Value for x to calculate the probability
    :param max_x: Maximum value for x
    :return: Tuple with time and probability
    """
    random_factor = random.uniform(0, 0.05)

    # add a vertical shift to the distribution
    shift = 0.1

    def density_func(mu: float, sigma: float) -> float:
        return 1 / (sigma * sqrt(2 * pi)) * e ** (-(x - mu) ** 2 / (2 * sigma ** 2))

    y = sum([density_func(mu, sigma) for mu, sigma in modes], random_factor + shift)

    return y / max_x
