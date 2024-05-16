import random
import time
from datetime import datetime, timedelta
from typing import Iterable
from uuid import UUID

from .simulator import Simulator
from ..models.raw_data.ecological_island_raw_data import EcologicalIslandRawData


class EcologicalIslandSimulator(Simulator):

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 latitude: float, longitude: float,
                 points_spacing: timedelta, limit: int = None,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None) -> None:
        super().__init__(sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         points_spacing=points_spacing,
                         generation_delay=generation_delay, limit=limit,
                         begin_date=begin_date, latitude=latitude, longitude=longitude)
        # parameters setted to generate a single value per hour
        self.last_value = random.uniform(0, 50)  # Initial value
        self.fill_rate = 1  # Adjusted average fill rate per hour
        self.noise_level = 1  # Adjusted noise level per hour
        self.hours_per_week = 7 * 24  # Total hours in a week
        self.emptying_hours = [2 * 24 + 8, 5 * 24 + 8]  # Emptying on Wednesday 08:00 and Saturday 08:00
        self.call_count = 0  # To count the number of times _filling_value is called

    def stream(self) -> Iterable[EcologicalIslandRawData]:
        while self.limit != 0 and self.running:
            self.last_value = self._filling_value()

            yield EcologicalIslandRawData(
                filling_value=self.last_value,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
                sensor_uuid=self.sensor_uuid,
                sensor_name=self.sensor_name,
            )

            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.frequency
            time.sleep(self.delay.total_seconds())

#    def _filling_value(self) -> float:
#        increment = random.gauss(3, 1.5)
#        filling = self.last_value + increment
#        return 0 if filling > 100 else filling

    def _filling_value(self) -> float:
        self.call_count += 1
        previous_value = self.last_value

        # Check if it's time to empty the island
        current_hour = self.call_count % self.hours_per_week
        if current_hour in self.emptying_hours:
            if random.random() < 0.1:  # 10% chance for partial emptying
                self.last_value *= random.uniform(0.0, 0.3)  # leave up to 30% of current value
            else:
                self.last_value = 0.0  # complete emptying
            return self.last_value
        
        # Simulate filling
        increment = self.fill_rate * random.uniform(0.5, 1.5)
        
        # Add noise
        noise = self.noise_level * random.uniform(-1, 1)
        
        # Update last value
        self.last_value += increment + noise
        
        # Ensure the value stays within 0 to 100 range
        self.last_value = max(0, min(self.last_value, 100))
        
        return max(previous_value, self.last_value)
