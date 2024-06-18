import random
from datetime import datetime
from typing import Iterable
# from datetime import timedelta
# from threading import Event
from math import pi, sin

from .simulator import Simulator
from ..models.raw_data.precipitation_raw_data import PrecipitationRawData


class PrecipitationSimulator(Simulator):
    def data(self) -> Iterable[PrecipitationRawData]:
        while self._limit != 0 and self._running:
            yield PrecipitationRawData(
                value=_sinusoidal_value(self._timestamp, self._latitude),
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


def _sinusoidal_value(timestamp: datetime, latitude: float) -> float:
    # Calculate day of year
    day_of_year = timestamp.timetuple().tm_yday

    # Calculate angles for seasonal and annual variations (adjusted for rain range)
    angle_seasonal = (2 * pi * day_of_year) / 365 * (15 / 2)  # Scales for 0-15 range
    angle_annual = (2 * pi * day_of_year) / (365.25 * 10) * (15 / 2)

    # Calculate base value with seasonal and annual variations, scaled for rain range
    base_value = sin(angle_seasonal) + 0.1 * sin(angle_annual)

    # Modify value based on latitude (consider adjusting factors for desired effect)
    latitude_factor = 1 - abs(latitude) / (90 / (15 / 2))  # Scales for 0-15 range

    # Scale base value by latitude factor
    value = base_value * latitude_factor

    # Introduce random factor for daily variations (consider adjusting range)
    random_factor = random.uniform(0.8, 1.2)

    # Calculate final precipitation value (scaled for 0-15 cm)
    precipitation_value = value * random_factor * 15

    # Simulate no rain with a probability based on absolute base value
    no_rain_probability = 1 - abs(base_value)
    if random.random() < no_rain_probability:
        precipitation_value = 0

    # Simulate extreme weather events with low probability (consider adjusting factor)
    if random.random() < 0.02:  # 2% chance of extreme weather event
        extreme_weather_factor = random.uniform(1.5, 2.5)
        precipitation_value *= extreme_weather_factor

    # Ensure non-negative value
    precipitation_value = max(precipitation_value, 0)

    return precipitation_value