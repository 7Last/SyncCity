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
                sensor_name=self.sensor_name,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
            )


def _sinusoidal_value(timestamp: datetime) -> float:
    seasonal_coeff = _seasonal_coefficient(timestamp)
    thermal_excursion = _thermal_excursion(timestamp)

    hour = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(-2, 2)
    return thermal_excursion * sin(hour * pi / 24) + seasonal_coeff + noise


def _seasonal_coefficient(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 13 * sin(x * pi / 12 - 1 / 4) + 3


def _thermal_excursion(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 8 * (sin(x * pi / 12 - (pi - 3) / 2) + 1)
