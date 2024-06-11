import random
from datetime import datetime
from typing import Iterable

from math import pi, sin

from .simulator import Simulator
from ..models.raw_data.temperature_raw_data import TemperatureRawData


class TemperatureSimulator(Simulator):
    def stream(self) -> Iterable[TemperatureRawData]:
        while self.limit != 0 and self.running:
            yield TemperatureRawData(
                value=_sinusoidal_value(self.timestamp),
                sensor_uuid=self.sensor_uuid,
                sensor_name=self.sensor_name,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
                group_name=self.group_name,
            )

            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.points_spacing
            self._event.wait(self.generation_delay.total_seconds())

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _sinusoidal_value(timestamp: datetime) -> float:
    seasonal_coeff = _seasonal_coefficient(timestamp)
    thermal_excursion = _thermal_excursion(timestamp)

    hour = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(-2, 2)
    return thermal_excursion * sin(hour * pi / 24) + seasonal_coeff + noise


def _seasonal_coefficient(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 13 * sin(x * pi / 12 - 1 / 4) + 3


def _thermal_excursion(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 8 * (sin(x * pi / 12 - (pi - 3) / 2) + 1)
