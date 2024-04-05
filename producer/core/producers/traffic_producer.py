import asyncio
import random
from ..models.traffic_raw_data import TrafficRawData
from .producer import Producer
from math import e, pi, sqrt
from datetime import time, timedelta, datetime


class TrafficProducer(Producer):
    def __init__(self, sensor_id: str, frequency: timedelta, limit: int = None, begin_date: datetime = None):
        super().__init__(sensor_id=sensor_id, frequency=frequency, limit=limit, begin_date=begin_date)

    async def stream(self) -> TrafficRawData:
        while self.limit != 0 and self.running:
            self.limit -= 1
            self.timestamp = self.timestamp + self.frequency
            await asyncio.sleep(self.frequency.total_seconds())

            lat, lon, alt = random.choice(list(self._City)).value

            probability = _multimodal_normal_gauss_value(
                x=self.timestamp.hour + self.timestamp.minute / 60,
                modes=[
                    (8.5, 0.425),  # 8:30 AM
                    (12.5, 0.38),  # 12:30 PM
                    (18, 0.38),  # 6 PM
                ],
                max_x=18,
            )

            yield TrafficRawData(
                # vehicles_per_unit=round(100 * 50 * probability),  # between 0 and 50 vehicles pass in 5 minutes
                vehicles_per_unit=0,
                avg_speed=random.randrange(5, 50),  # km/h
                latitude=lat,
                longitude=lon,
                altitude=alt,
                sensor_id=self.sensor_id,
                timestamp=self.timestamp,
            )


def _multimodal_normal_gauss_value(x: float, modes: list[tuple[float, float]], max_x: float) -> tuple[time, float]:
    """
    Returns generates a random x in a range and calculates its corresponding y from a bimodal Gaussian distribution.
    :param modes: list of tuples with the mu and sigma values for each mode
    :param x: Value for x to calculate the probability
    :param max_x: Maximum value for x
    :return: Tuple with time and probability
    """

    random_factor = random.uniform(0, 0.1)

    # add a vertical shift to the distribution
    vertical_shift = 0.3

    density_func = lambda mu, sigma: (1 / (sigma * sqrt(2 * pi)) * e ** (-(x - mu) ** 2 / (2 * sigma ** 2)))
    y = sum([density_func(mu, sigma) for mu, sigma in modes], random_factor) + vertical_shift

    return y / max_x
