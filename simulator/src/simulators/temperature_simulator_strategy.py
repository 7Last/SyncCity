import random
from datetime import datetime

from math import pi, sin

from .simulator_strategy import SimulatorStrategy
from ..models.raw_data.temperature_raw_data import TemperatureRawData


class TemperatureSimulatorStrategy(SimulatorStrategy):
    def simulate(self) -> TemperatureRawData:
        data = TemperatureRawData(
            value=self.__sinusoidal_value(self._timestamp),
            sensor_uuid=self._sensor_uuid,
            sensor_name=self._sensor_name,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'

    def __sinusoidal_value(self, timestamp: datetime) -> float:
        seasonal_coefficient = self.__seasonal_coefficient(timestamp)
        thermal_excursion = self.__daily_thermal_excursion(timestamp)

        hour = timestamp.hour + timestamp.minute / 60
        noise = random.uniform(-2, 2)
        return thermal_excursion * sin(hour * pi / 24) + seasonal_coefficient + noise

    def __seasonal_coefficient(self, timestamp: datetime) -> float:
        x = timestamp.month + (timestamp.day - 1) / 30
        return 13 * sin(x * pi / 12 - 1 / 4) + 3

    def __daily_thermal_excursion(self, timestamp: datetime) -> float:
        x = timestamp.month + (timestamp.day - 1) / 30
        return 8 * (sin(x * pi / 12 - (pi - 3) / 2) + 1)
