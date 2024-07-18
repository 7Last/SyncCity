import random
from datetime import datetime

from math import pi, sin

from .simulator_strategy import SimulatorStrategy
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.air_quality_raw_data import AirQualityRawData
from ..producers.producer_strategy import ProducerStrategy


class AirQualitySimulatorStrategy(SimulatorStrategy):

    def __init__(self, sensor_name: str, config: SensorConfig) -> None:
        super().__init__(sensor_name, config)
        self.__o3_coefficient = random.uniform(-50, 50)
        self.__pm25_coefficient = random.uniform(-50, 50)
        self.__pm10_coefficient = random.uniform(-50, 50)
        self.__no2_coefficient = random.uniform(-50, 50)
        self.__so2_coefficient = random.uniform(-50, 50)

    def simulate(self) -> AirQualityRawData:
        data = AirQualityRawData(
            o3=self.__sinusoidal_value(self._timestamp, self.__o3_coefficient) / 2,
            pm25=self.__sinusoidal_value(self._timestamp, self.__pm25_coefficient) / 3,
            pm10=self.__sinusoidal_value(self._timestamp, self.__pm10_coefficient) / 4,
            no2=self.__sinusoidal_value(self._timestamp, self.__no2_coefficient),
            so2=self.__sinusoidal_value(self._timestamp, self.__so2_coefficient),
            latitude=self._latitude,
            longitude=self._longitude,
            sensor_uuid=self._sensor_uuid,
            timestamp=self._timestamp,
            sensor_name=self._sensor_name,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'

    def __sinusoidal_value(self, timestamp: datetime, coefficient: float) -> float:
        daily_variation = self.__daily_variation(timestamp)
        weekly_variation = self.__weekly_variation(timestamp)
        seasonal_variation = self.__seasonal_variation(timestamp)
        return daily_variation + weekly_variation + seasonal_variation + coefficient

    def __daily_variation(self, timestamp: datetime) -> float:
        x = timestamp.hour + timestamp.minute / 60
        noise = random.uniform(-20, 20)
        return 20 * sin(x * pi / 24) + 80 + noise

    def __weekly_variation(self, timestamp: datetime) -> float:
        x = timestamp.weekday() + (timestamp.hour + timestamp.minute / 60) / 24
        noise = random.uniform(-20, 20)
        return -20 * sin(x * pi / 7) + 10 + noise

    def __seasonal_variation(self, timestamp: datetime) -> float:
        day_of_year = timestamp.timetuple().tm_yday
        x = day_of_year + (timestamp.hour + timestamp.minute / 60) / 24
        noise = random.uniform(-20, 20)
        return -80 * sin(x * pi / 182.5 + 105) + 60 + noise
