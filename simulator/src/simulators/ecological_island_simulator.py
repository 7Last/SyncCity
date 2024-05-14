import random
import time
from datetime import datetime, timedelta
from math import e, pi, sqrt
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
        self.last_value = 0

    def stream(self) -> Iterable[EcologicalIslandRawData]:
        while self.limit != 0 and self.running:
            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.frequency
            time.sleep(self.delay.total_seconds())

            yield EcologicalIslandRawData(
                starting_filling=10,
                filling_speed=_filling_speed(),
                filling_value=self._filling_value(filling_speed=_filling_speed()),
                latitude=self.latitude,
                longitude=self.longitude,
                timestamp=self.timestamp,
                sensor_uuid=self.sensor_uuid,
                sensor_name=self.sensor_name,
            )

    def get_last_value(self) -> float:
        return self.last_value

    def _filling_value(self, filling_speed) -> float:
        filling = EcologicalIslandSimulator.get_last_value(self) + filling_speed
        if filling > 100:
            filling = 0
        self.last_value = filling
        return filling


def _filling_speed() -> float:
    return random.uniform(0, 5)
