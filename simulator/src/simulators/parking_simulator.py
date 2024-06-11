import random
from datetime import datetime, timedelta
from typing import Iterable
from uuid import UUID

from .simulator import Simulator
from ..models.raw_data.parking_raw_data import ParkingRawData


class ParkingSimulator(Simulator):
    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 latitude: float, longitude: float,
                 points_spacing: timedelta, limit: int = None,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        super().__init__(sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         points_spacing=points_spacing,
                         generation_delay=generation_delay, limit=limit,
                         begin_date=begin_date, latitude=latitude, longitude=longitude)

    def stream(self) -> Iterable[ParkingRawData]:
        while self.limit != 0 and self.running:
            is_occupied = self._generate_occupancy()
            
            yield ParkingRawData(
                is_occupied=is_occupied,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
                sensor_uuid=self.sensor_uuid,
                sensor_name=self.sensor_name,
            )

            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.points_spacing
            self._event.wait(self.generation_delay.total_seconds())

    def _generate_occupancy(self) -> int:
        """
        Generate a realistic occupancy value (0 or 1) based on the time of day.
        Assume higher occupancy during business hours and lower during night hours.
        """
        hour = self.timestamp.hour
        if 8 <= hour < 18:  # Peak business hours
            return 1 if random.random() < 0.7 else 0  # 70% chance occupied
        elif 18 <= hour < 22:  # Evening hours
            return 1 if random.random() < 0.5 else 0  # 50% chance occupied
        else:  # Night hours
            return 1 if random.random() < 0.2 else 0  # 20% chance occupied

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
