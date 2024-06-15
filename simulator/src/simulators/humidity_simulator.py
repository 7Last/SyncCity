import random
from datetime import datetime, timedelta
from math import pi, sin
from typing import Iterable
from uuid import UUID

from .simulator import Simulator
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.humidity_raw_data import HumidityRawData


class HumiditySimulator(Simulator):

    def __init__(self, sensor_name: str, config: SensorConfig) -> None:
        super().__init__(sensor_name, config)
        # self._value = _humidity_value(self._timestamp)
 

    def stream(self) -> Iterable[HumidityRawData]:
        while self._limit != 0 and self._running:
            
            yield HumidityRawData(
                value= _humidity_value(self._timestamp),
                sensor_uuid=self._sensor_uuid,
                sensor_name=self.sensor_name,
                latitude=self._latitude,
                longitude=self._longitude,
                timestamp=self._timestamp,
                group_name=self._group_name,
            )

            if self._limit is not None:
                self._limit -= 1
            self._timestamp += self._points_spacing
            self._event.wait(self._generation_delay.total_seconds())

def _humidity_value(timestamp: datetime) -> float:
    seasonal_coeff = _humidity_seasonal_coefficient(timestamp)
    daily_variation = _humidity_daily_variation(timestamp)
    night_attenuation = _night_attenuation_factor(timestamp)

    hour = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(-3, 3)  # Raffiniamo la variazione casuale
    return (daily_variation * sin(hour * pi / 24) + seasonal_coeff + noise) * night_attenuation

def _humidity_seasonal_coefficient(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 45 + 15 * sin(x * pi / 12 - 1 / 4)  # Aggiustiamo i coefficienti stagionali

def _humidity_daily_variation(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 25 * (sin(x * pi / 12 - (pi - 3) / 2) + 1)  # Modifichiamo la variazione giornaliera

def _night_attenuation_factor(timestamp: datetime) -> float:
    hour = timestamp.hour
    if 0 <= hour < 6 or 20 <= hour < 24:
        return 0.8  # Riduciamo la variazione di umidità durante le ore notturne
    return 1