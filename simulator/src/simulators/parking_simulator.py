import random
from typing import Iterable

from .simulator import Simulator
from ..models.raw_data.parking_raw_data import ParkingRawData


class ParkingSimulator(Simulator):
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
                group_name=self.group_name,
            )

            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.points_spacing
            self._event.wait(self.generation_delay.total_seconds())

    def _generate_occupancy(self) -> bool:
        """
        Generate a realistic occupancy value (0 or 1) based on the time of day.
        Assume higher occupancy during business hours and lower during night hours.
        """
        hour = self.timestamp.hour
        if 8 <= hour < 18:  # Peak business hours
            return random.random() < 0.7  # 70% chance occupied
        if 18 <= hour < 22:  # Evening hours
            return random.random() < 0.5  # 50% chance occupied
        # Night hours
        return random.random() < 0.2  # 20% chance occupied

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
