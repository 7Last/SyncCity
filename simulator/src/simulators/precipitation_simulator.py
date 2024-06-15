import random
from datetime import datetime
from typing import Iterable
import timedelta
from threading import Event
from math import pi, sin

from .simulator import Simulator
from ..models.raw_data.precipitation_raw_data import PrecipitationRawData


class PrecipitationSimulator(Simulator):
    def stream(self) -> Iterable[PrecipitationRawData]:
        while self._limit != 0 and self._running:
            yield PrecipitationRawData(
                #TODOO: implement value
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
    # Calculate the day of the year
    day_of_year = timestamp.timetuple().tm_yday
    
    # Calculate the angle for the sinusoidal function
    angle = (2 * pi * day_of_year) / 365
    
    # Calculate the base sinusoidal value
    base_value = sin(angle)
    
    # Modify the value based on latitude
    # Assuming a simple model where equator (latitude 0) has higher precipitation
    # and poles (latitude +/- 90) have lower precipitation
    latitude_factor = 1 - abs(latitude) / 90
    
    # Scale the base value by the latitude factor
    value = base_value * latitude_factor
    
    # Introduce a random factor to simulate daily variations
    random_factor = random.uniform(0.8, 1.2)
    
    # Calculate the final precipitation value
    precipitation_value = value * random_factor
    
    # Ensure the value is non-negative (since precipitation cannot be negative)
    precipitation_value = max(precipitation_value, 0)
    
    return precipitation_value



