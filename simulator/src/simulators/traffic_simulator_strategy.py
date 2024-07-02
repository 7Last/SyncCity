import random

from math import e, pi, sqrt

from .simulator_strategy import SimulatorStrategy
from ..models.raw_data.traffic_raw_data import TrafficRawData


class TrafficSimulatorStrategy(SimulatorStrategy):
    _SPEED_MULTIPLICATIVE_FACTOR = 100
    _VEHICLES_MULTIPLICATIVE_FACTOR = 200

    def data(self) -> TrafficRawData:
        speed = self._SPEED_MULTIPLICATIVE_FACTOR * _multimodal_gauss_value(
            x=self._timestamp.hour + self._timestamp.minute / 60,
            modes=[
                (0, 2.1),
                (4, 2.2),
                (13, 3),
                (21, 3),
                (24, 3),
            ],
        )

        vehicles = self._VEHICLES_MULTIPLICATIVE_FACTOR * _multimodal_gauss_value(
            x=self._timestamp.hour + self._timestamp.minute / 60,
            modes=[
                (0, 4),
                (8.5, 1.8),
                (13, 2),
                (17.5, 1.7),
                (21, 3),
            ],
        )

        data = TrafficRawData(
            vehicles=int(vehicles),
            avg_speed=speed,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            sensor_uuid=self._sensor_uuid,
            sensor_name=self.sensor_name,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _multimodal_gauss_value(x: float, modes: list[tuple[float, float]]) -> float:
    """Returns generates a random x in a range and calculates its corresponding y
    from a bimodal Gaussian distribution.
    :param modes: list of tuples with the mu and sigma values for each mode
    :param x: Value for x to calculate the probability
    """
    random_factor = random.uniform(0, 0.1)

    # add a vertical shift to the distribution
    shift = 0.1

    def density_func(mu: float, sigma: float) -> float:
        return 1 / (sigma * sqrt(2 * pi)) * e ** (-(x - mu) ** 2 / (2 * sigma ** 2))

    return sum([density_func(mu, sigma) for mu, sigma in modes], random_factor + shift)
