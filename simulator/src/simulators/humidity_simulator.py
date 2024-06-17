import random
from datetime import datetime

from math import pi, sin

from .simulator import Simulator
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.humidity_raw_data import HumidityRawData
from ..producers.producer_strategy import ProducerStrategy


class HumiditySimulator(Simulator):

    def __init__(self, sensor_name: str, config: SensorConfig,
                 producer: ProducerStrategy) -> None:
        super().__init__(sensor_name, config, producer)

    def data(self) -> HumidityRawData:
        data = HumidityRawData(
            value=_humidity_value(self._timestamp, self._latitude),
            sensor_uuid=self._sensor_uuid,
            sensor_name=self.sensor_name,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data


def _humidity_value(timestamp: datetime, latitude: float) -> float:
    seasonal_coeff = _humidity_seasonal_coefficient(timestamp, latitude)
    daily_variation = _humidity_daily_variation(timestamp)
    night_attenuation = _night_attenuation_factor(timestamp)

    hour = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(-3, 3)  # Raffiniamo la variazione casuale
    humidity = (daily_variation * sin(
        hour * pi / 24) + seasonal_coeff + noise) * night_attenuation
    return min(humidity, 100)  # Assicuriamo che l'umidità non superi il 100%


def _humidity_seasonal_coefficient(timestamp: datetime, latitude: float) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    equator_distance_factor = _equator_distance_factor(latitude)
    return (45 + 15 * sin(
        x * pi / 12 - 1 / 4)) * equator_distance_factor  # Modifichiamo i coefficienti stagionali in base alla latitudine


def _humidity_daily_variation(timestamp: datetime) -> float:
    x = timestamp.month + (timestamp.day - 1) / 30
    return 25 * (sin(x * pi / 12 - (
            pi - 3) / 2) + 1)  # Modifichiamo la variazione giornaliera


def _night_attenuation_factor(timestamp: datetime) -> float:
    hour = timestamp.hour
    if 0 <= hour < 6 or 20 <= hour < 24:
        return 0.8  # Riduciamo la variazione di umidità durante le ore notturne
    return 1


def _equator_distance_factor(latitude: float) -> float:
    return 1 - abs(
        latitude) / 90  # Riduciamo l'impatto della latitudine all'aumentare della distanza dall'equatore
