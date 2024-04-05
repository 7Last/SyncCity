import asyncio
import random
from ..models.temperature_raw_data import TemperatureRawData
from .producer import Producer
from datetime import datetime, timedelta


class TemperatureProducer(Producer):

    def __init__(self, sensor_id: str, frequency: timedelta, begin_date: datetime = None, limit: int = None):
        super().__init__(sensor_id=sensor_id, frequency=frequency, begin_date=begin_date, limit=limit)

    async def stream(self) -> TemperatureRawData:
        while self.limit != 0 and self.running:
            self.limit -= 1
            self.timestamp = self.timestamp + self.frequency
            await asyncio.sleep(self.frequency.total_seconds())

            lat, lon, alt = random.choice(list(self._City)).value
            yield TemperatureRawData(
                value=random.uniform(-10, 30),
                sensor_id=self.sensor_id,
                latitude=lat,
                longitude=lon,
                altitude=alt,
                timestamp=self.timestamp
            )
