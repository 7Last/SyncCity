from datetime import datetime, timedelta
import random
import asyncio

from .producer import Producer
from ..models.temperature_raw_data import TemperatureRawData


class TemperatureProducer(Producer):

    def __init__(self, *, sensor_id: str, frequency: timedelta,
                 latitude: float, longitude: float, begin_date: datetime = None,
                 limit: int = None) -> None:
        super().__init__(sensor_id=sensor_id, frequency=frequency, latitude=latitude,
                         longitude=longitude, begin_date=begin_date, limit=limit)

    async def stream(self) -> TemperatureRawData:
        while self.limit != 0 and self.running:
            self.limit -= 1
            self.timestamp = self.timestamp + self.frequency
            await asyncio.sleep(self.frequency.total_seconds())

            yield TemperatureRawData(
                value=random.uniform(-10, 30),
                sensor_id=self.sensor_id,
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
            )
