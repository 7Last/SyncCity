import random
from datetime import datetime

from math import pi, sin

from .simulator_strategy import SimulatorStrategy
from ..models.raw_data.humidity_raw_data import HumidityRawData


class HumiditySimulatorStrategy(SimulatorStrategy):
    def simulate(self) -> HumidityRawData:
        data = HumidityRawData(
            value=self.__humidity_value(self._timestamp, self._latitude),
            sensor_uuid=self._sensor_uuid,
            sensor_name=self._sensor_name,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def __humidity_value(self, timestamp: datetime, latitude: float) -> float:
        seasonal_coeff = self.__seasonal_coefficient(timestamp, latitude)
        daily_variation = self.__daily_variation(timestamp)
        night_attenuation = self.__night_attenuation_factor(timestamp)

        hour = timestamp.hour + timestamp.minute / 60
        noise = random.uniform(-3, 3)
        humidity = (daily_variation * sin(
            hour * pi / 24) + seasonal_coeff + noise) * night_attenuation
        return min(humidity, 100)

    def __seasonal_coefficient(self, timestamp: datetime, latitude: float) -> float:
        x = timestamp.month + (timestamp.day - 1) / 30
        equator_distance_factor = self.__equator_distance_factor(latitude)
        # Change the seasonal coefficients based on the latitude
        return (45 + 15 * sin(
            x * pi / 12 - 1 / 4)) * equator_distance_factor

    def __daily_variation(self, timestamp: datetime) -> float:
        x = timestamp.month + (timestamp.day - 1) / 30
        return 25 * (sin(x * pi / 12 - (pi - 3) / 2) + 1)

    def __night_attenuation_factor(self, timestamp: datetime) -> float:
        hour = timestamp.hour
        # Reducing the humidity variation during the night hours
        if 0 <= hour < 6 or 20 <= hour < 24:
            return 0.8
        return 1

    def __equator_distance_factor(self, latitude: float) -> float:
        # Reduce the impact of the latitude moving away from the equator
        return 1 - abs(latitude) / 90
