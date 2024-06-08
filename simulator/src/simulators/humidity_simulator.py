import random, math
from datetime import datetime, timedelta
from typing import Iterable
from uuid import UUID

from .simulator import Simulator
from ..models.raw_data.humidity_raw_data import HumidityRawData


class HumiditySimulator(Simulator):

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 latitude: float, longitude: float,
                 points_spacing: timedelta, limit: int = None,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        super().__init__(sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         points_spacing=points_spacing,
                         generation_delay=generation_delay, limit=limit,
                         begin_date=begin_date, latitude=latitude, longitude=longitude)
        # last value
        self.last_value = self._initial_humidity(latitude, longitude, self.timestamp)
        # previous value's timestamp
        self.prev_timestamp = self.timestamp
        # noise rate
        self.noise_limit = random.uniform(-5, 5)

    def _initial_humidity(self, latitude: float, longitude: float, timestamp: datetime) -> float:
        # Determine initial humidity based on location and time of year
        base_humidity = 50  # Assume a base humidity value

        # Seasonal variation
        seasonal_variation = math.sin(2 * math.pi * (timestamp.timetuple().tm_yday / 365.25))
        
        # Geographic influence (simplified: closer to equator or sea, higher humidity)
        equator_distance = abs(latitude) / 90  # Normalize latitude (0 at equator, 1 at poles)
        longitude_influence = abs(longitude) / 180  # Simplified influence of longitude
        
        geographic_influence = (1 - equator_distance) * 20 + longitude_influence * 5

        return base_humidity + 20 * seasonal_variation + geographic_influence + random.uniform(-10, 10)


    def _update_humidity(self, last_value: float, timestamp: datetime) -> float:
        # Change in humidity based on time of day and season
        hour_variation = 10 * math.sin(2 * math.pi * (timestamp.hour / 24))
        seasonal_variation = 20 * math.sin(2 * math.pi * (timestamp.timetuple().tm_yday / 365.25))

        # Random noise to simulate realistic changes
        noise = random.uniform(self.noise_limit / 2, self.noise_limit)
        
        new_value = last_value + hour_variation + seasonal_variation + noise
        return max(0, min(100, new_value))  # Humidity should be between 0 and 100

    def stream(self) -> Iterable[HumidityRawData]:
        while True:
            self.prev_timestamp += self.points_spacing
            self.last_value = self._update_humidity(self.last_value, self.prev_timestamp)
            yield HumidityRawData(
                timestamp=self.prev_timestamp,
                sensor_name=self.sensor_name,
                sensor_uuid=self.sensor_uuid,
                humidity=self.last_value
            )
