import random
from datetime import datetime
from typing import Iterable

from math import pi, sin

from .simulator import Simulator
from ..models.raw_data.air_quality_raw_data import AirQualityRawData


class AirQualitySimulator(Simulator):

    def stream(self) -> Iterable[AirQualityRawData]:
        o3_coefficient = random.uniform(-50, 50)
        pm25_coefficient = random.uniform(-50, 50)
        pm10_coefficient = random.uniform(-50, 50)
        no2_coefficient = random.uniform(-50, 50)
        so2_coefficient = random.uniform(-50, 50)

        while self.limit != 0 and self.running:
            yield AirQualityRawData(
                o3=_sinusoidal_value(self.timestamp, o3_coefficient) / 2,
                pm25=_sinusoidal_value(self.timestamp, pm25_coefficient) / 3,
                pm10=_sinusoidal_value(self.timestamp, pm10_coefficient) / 4,
                no2=_sinusoidal_value(self.timestamp, no2_coefficient),
                so2=_sinusoidal_value(self.timestamp, so2_coefficient),
                latitude=self.latitude,
                longitude=self.longitude,
                sensor_uuid=self.sensor_uuid,
                timestamp=self.timestamp,
                sensor_name=self.sensor_name,
                group_name=self.group_name,
            )

            if self.limit is not None:
                self.limit -= 1
            self.timestamp += self.points_spacing
            self._event.wait(self.generation_delay.total_seconds())

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _sinusoidal_value(timestamp: datetime, coefficient: float) -> float:
    daily_variation = _daily_variation(timestamp)
    weekly_variation = _weekly_variation(timestamp)
    seasonal_variation = _seasonal_variation(timestamp)
    return daily_variation + weekly_variation + seasonal_variation + coefficient


def _daily_variation(timestamp: datetime) -> float:
    x = timestamp.hour + timestamp.minute / 60
    noise = random.uniform(-20, 20)
    return 20 * sin(x * pi / 24) + 80 + noise


def _weekly_variation(timestamp: datetime) -> float:
    x = timestamp.weekday() + (timestamp.hour + timestamp.minute / 60) / 24
    noise = random.uniform(-20, 20)
    return -20 * sin(x * pi / 7) + 10 + noise


def _seasonal_variation(timestamp: datetime) -> float:
    day_of_year = timestamp.timetuple().tm_yday
    x = day_of_year + (timestamp.hour + timestamp.minute / 60) / 24
    noise = random.uniform(-20, 20)
    return -80 * sin(x * pi / 182.5 + 105) + 60 + noise
