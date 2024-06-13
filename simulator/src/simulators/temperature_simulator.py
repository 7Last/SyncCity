import random
from datetime import datetime
from typing import Iterable

from math import pi, sin

from .simulator import Simulator
from ..models.raw_data.temperature_raw_data import TemperatureRawData


class TemperatureSimulator(Simulator):
    def stream(self) -> Iterable[TemperatureRawData]:
        while self._limit != 0 and self._running:
            yield TemperatureRawData(
                value=_sinusoidal_value(self._timestamp),
                sensor_uuid=self._sensor_uuid,
                sensor_name=self.sensor_name,
                latitude=self._latitude,
                longitude=self._longitude,
                timestamp=self._timestamp,
                group_name=self._group_name,
            )

            if self._limit is not None:
                self._limit -= 1
            self._timestamp += self._points_spacing
            self._event.wait(self._generation_delay.total_seconds())

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _sinusoidal_value(timestamp: datetime) -> float:
    seasonal_coefficient = _seasonal_coefficient(timestamp)
    thermal_excursion = _daily_thermal_excursion(timestamp)

    hour = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(-2, 2)
    return thermal_excursion * sin(hour * pi / 24) + seasonal_coefficient + noise


def _seasonal_coefficient(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 13 * sin(x * pi / 12 - 1 / 4) + 3


def _daily_thermal_excursion(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 8 * (sin(x * pi / 12 - (pi - 3) / 2) + 1)
