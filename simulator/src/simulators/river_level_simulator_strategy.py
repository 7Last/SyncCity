import random
from datetime import datetime

from math import pi, sin

from .simulator_strategy import SimulatorStrategy
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.river_level_raw_data import RiverLevelRawData
from ..producers.producer_strategy import ProducerStrategy


class RiverLevelSimulatorStrategy(SimulatorStrategy):
    _DAILY_VARIATION = 0.5
    _SEASONAL_VARIATION = 1.5
    _BASE_LEVEL = 5.0
    _RANDOM_VARIABILITY = 0.1

    # Seasonal coefficients based on the month
    _SEASONAL_COEFFICIENTS = {
        1: 0.8,
        2: 0.85,
        3: 1.0,
        4: 1.2,
        5: 1.5,
        6: 1.7,
        7: 1.6,
        8: 1.5,
        9: 1.3,
        10: 1.1,
        11: 0.9,
        12: 0.85,
    }

    def __init__(self, sensor_name: str, config: SensorConfig,
                 producer: ProducerStrategy) -> None:
        super().__init__(sensor_name, config, producer)
        self._latitude_factor = (sin(config.latitude / 90.0 * pi / 2)) ** 2

    def data(self) -> RiverLevelRawData:
        data = RiverLevelRawData(
            value=self._sinusoidal_value(self._timestamp),
            sensor_uuid=self._sensor_uuid,
            sensor_name=self.sensor_name,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'

    def _sinusoidal_value(self, timestamp: datetime) -> float:
        # Yearly variation
        day_of_year = timestamp.timetuple().tm_yday
        seasonal_variation = self._SEASONAL_VARIATION * sin(
            2 * pi * day_of_year / 365.25)

        # Coefficiente stagionale basato sul mese
        month = timestamp.month
        seasonal_coefficient = self._SEASONAL_COEFFICIENTS.get(month, 1.0)

        # Daily variation
        seconds = timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second
        daily_variation = self._DAILY_VARIATION * sin(2 * pi * seconds / 86400)

        random_factor = random.gauss(1, self._RANDOM_VARIABILITY)

        return 500 * (
                self._BASE_LEVEL + seasonal_variation + daily_variation * self._latitude_factor   # noqa: E501
        ) * seasonal_coefficient * random_factor
