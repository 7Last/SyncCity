import asyncio
import random
from ..models.temperature_raw_data import TemperatureRawData
from .producer import Producer


class TemperatureProducer(Producer):

    def __init__(self, sensor_id: str, frequency: int, limit: int):
        super().__init__(sensor_id=sensor_id, frequency=frequency, limit=limit)

    async def stream(self) -> TemperatureRawData:
        while self.limit != 0 and self.running:
            self.limit -= 1
            await asyncio.sleep(self.frequency / 1000)

            lat, lon, alt = random.choice(list(self._City)).value
            yield TemperatureRawData(
                value=self._uniform_value(),
                sensor_id=self.sensor_id,
                latitude=lat,
                longitude=lon,
                altitude=alt,
            )

    def _range(self) -> tuple[float, float]:
        return -10, 40
