import random
import time
from datetime import datetime, timedelta
from math import pi, sin
from typing import Iterable
from uuid import UUID

from .simulator import Simulator
from ..models.raw_data.temperature_raw_data import TemperatureRawData


class TemperatureSimulator(Simulator):

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 points_spacing: timedelta, latitude: float, longitude: float,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None,
                 limit: int = None) -> None:
        super().__init__(sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         points_spacing=points_spacing, latitude=latitude,
                         generation_delay=generation_delay, longitude=longitude,
                         begin_date=begin_date, limit=limit)

    def stream(self) -> Iterable[TemperatureRawData]:
        while self.limit != 0 and self.running:
            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.frequency
            time.sleep(self.delay.total_seconds())

            yield TemperatureRawData(
                value=_sinusoidal_value(self.timestamp),
                sensor_uuid=self.sensor_uuid,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
            )


def _sinusoidal_value(timestamp: datetime) -> float:
    season_coefficient = 0
    thermal_excursion = 0
    match timestamp.month:
        case 1 | 2 | 12:  # winter
            season_coefficient = 5
            thermal_excursion = 10
        case 3 | 4 | 5:  # spring
            season_coefficient = 10
            thermal_excursion = 15
        case 6 | 7 | 8:  # summer
            season_coefficient = 22
            thermal_excursion = 20
        case 9 | 10 | 11:  # autumn
            season_coefficient = 7
            thermal_excursion = 15

    x = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(0, 0.4)
    return thermal_excursion * sin(x * pi / 24) + season_coefficient + noise
