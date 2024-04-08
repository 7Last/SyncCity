from math import e, pi, sqrt
from datetime import datetime, timedelta
import random
import asyncio

from .producer import Producer
from ..models.traffic_raw_data import TrafficRawData


class TrafficProducer(Producer):
    def __init__(self, *, latitude: float, longitude: float, sensor_id: str,
                 frequency: timedelta, limit: int = None,
                 begin_date: datetime = None) -> None:
        super().__init__(sensor_id=sensor_id, frequency=frequency, limit=limit,
                         begin_date=begin_date, latitude=latitude, longitude=longitude)

    async def stream(self) -> TrafficRawData:
        while self.limit != 0 and self.running:
            self.limit -= 1
            self.timestamp = self.timestamp + self.frequency
            await asyncio.sleep(self.frequency.total_seconds())

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
                vehicles_per_unit=round(1000 * probability),
                avg_speed_per_unit=random.randrange(5, 50),  # km/h
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
    random_factor = random.uniform(0, 0.1)

    # add a vertical shift to the distribution
    vertical_shift = 0.3

    def density_func(mu: float, sigma: float) -> float:
        return 1 / (sigma * sqrt(2 * pi)) * e ** (-(x - mu) ** 2 / (2 * sigma ** 2))

    y = (sum([density_func(mu, sigma) for mu, sigma in modes], random_factor) +
         vertical_shift)

    return y / max_x
