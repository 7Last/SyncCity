import random
from datetime import datetime, timedelta
from math import pi, sin
from typing import Iterable
from uuid import UUID

from .simulator import Simulator
from ..models.raw_data.humidity_raw_data import HumidityRawData


class HumiditySimulator(Simulator):

    def __init__(self, *, sensor_name: str, sensor_uuid: UUID,
                 points_spacing: timedelta, latitude: float, longitude: float,
                 generation_delay: timedelta = timedelta(seconds=1),
                 begin_date: datetime = None,
                 limit: int = None) -> None:
        super().__init__(sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         points_spacing=points_spacing, latitude=latitude,
                         generation_delay=generation_delay, longitude=longitude,
                         begin_date=begin_date, limit=limit)

    def stream(self) -> Iterable[HumidityRawData]:
        while self.limit != 0 and self.running:
            yield HumidityRawData(
                value=_humidity_value(self.timestamp),
                sensor_uuid=self.sensor_uuid,
                sensor_name=self.sensor_name,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
            )

            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.points_spacing
            self._event.wait(self.generation_delay.total_seconds())


def _humidity_value(timestamp: datetime) -> float:
    seasonal_coeff = _humidity_seasonal_coefficient(timestamp)
    daily_variation = _humidity_daily_variation(timestamp)

    hour = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(-5, 5)
    return daily_variation * sin(hour * pi / 24) + seasonal_coeff + noise


def _humidity_seasonal_coefficient(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 50 + 10 * sin(x * pi / 12 - 1 / 4)


def _humidity_daily_variation(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 20 * (sin(x * pi / 12 - (pi - 3) / 2) + 1)
