from math import pi, sin
from datetime import datetime, timedelta
import random
import asyncio

from .producer import Producer
from ..models.temperature_raw_data import TemperatureRawData


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


class TemperatureProducer(Producer):

    def __init__(self, *, sensor_id: str, frequency: timedelta,
                 latitude: float, longitude: float, begin_date: datetime = None,
                 limit: int = None) -> None:
        super().__init__(sensor_id=sensor_id, frequency=frequency, latitude=latitude,
                         longitude=longitude, begin_date=begin_date, limit=limit)

    async def stream(self) -> TemperatureRawData:
        while self.limit != 0 and self.running:
            self.limit -= 1
            self.timestamp += self.frequency
            await asyncio.sleep(self.frequency.total_seconds())

            yield TemperatureRawData(
                value=_sinusoidal_value(self.timestamp),
                sensor_id=self.sensor_id,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
            )
