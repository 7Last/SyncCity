import random
from datetime import datetime, timedelta
from typing import Iterable

from .simulator import Simulator
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.charging_station_raw_data import ChargingStationRawData


class ChargingStationSimulator(Simulator):
    def __init__(self, sensor_name: str, config: SensorConfig) -> None:
        super().__init__(sensor_name, config)
        self._is_occupied = self._generate_occupancy()

    def stream(self) -> Iterable[ChargingStationRawData]:
        while self._limit != 0 and self._running:

            yield ChargingStationRawData(
                is_occupied=self._is_occupied,
                latitude=self._latitude,
                longitude=self._longitude,
                timestamp=self._timestamp,
                sensor_uuid=self._sensor_uuid,
                sensor_name=self.sensor_name,
                group_name=self._group_name,
            )

            if self._limit is not None:
                self._limit -= 1
            self._timestamp = self._generate_next_occupancy_change()
            # Change the occupancy status
            self._is_occupied = not self._is_occupied
            self._event.wait(self._generation_delay.total_seconds())

    def _generate_occupancy(self) -> bool:
        """
        Generate a realistic occupancy value (0 or 1) based on the time of day.
        Assume higher occupancy during business hours and lower during night hours.
        """
        hour = self._timestamp.hour
        if 8 <= hour < 18:  # Peak business hours
            return random.random() < 0.7  # 70% chance occupied
        if 18 <= hour < 22:  # Evening hours
            return random.random() < 0.5  # 50% chance occupied
        # Night hours
        return random.random() < 0.2  # 20% chance occupied

    def _generate_next_occupancy_change(self) -> datetime:
        """
        Generate the next timestamp when the occupancy will change.
        Assume that:
            - from 7 to 9 AM the occupancy will change every 10 minutes to 1 hour
            - from 9 AM to 6 PM the occupancy will change every 30 minutes to 6 hours
            - from 6 PM to 10 PM the occupancy will change every 30 minutes to 2 hour
            - from 10 PM to 7 AM the occupancy will change every 1 hour to 9 hours
        """
        hour = self._timestamp.hour
        if 7 <= hour < 9:
            return self._timestamp + _random_timedelta(10, 60)
        if 9 <= hour < 18:
            return self._timestamp + _random_timedelta(30, 360)
        if 18 <= hour < 22:
            return self._timestamp + _random_timedelta(30, 120)

        return self._timestamp + _random_timedelta(60, 540)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _random_timedelta(min_minutes: int, max_minutes: int) -> timedelta:
    minutes = random.randint(min_minutes, max_minutes)
    return timedelta(minutes=minutes)
