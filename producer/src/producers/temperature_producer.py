import asyncio
import random
import logging as log

from .models.temperature_raw_data import TemperatureRawData
from .producer import Producer


class TemperatureProducer(Producer):

    def __init__(self, sensor_id: str, frequency: int, limit: int):
        super().__init__(sensor_id=sensor_id, frequency=frequency, limit=limit)

    async def produce(self) -> TemperatureRawData:
        while True and (self.limit is None or self.limit > 0):
            self.limit -= 1
            await asyncio.sleep(self.frequency / 1000)

            lat, lon, alt = random.choice(list(self._Cities)).value

            yield TemperatureRawData(
                value=self._uniform_value(),
                sensor_id=self.sensor_id,
                latitude=lat,
                longitude=lon,
                altitude=alt,
            )

    def _range(self):
        return -10, 40
