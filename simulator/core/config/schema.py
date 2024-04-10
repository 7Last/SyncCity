from enum import Enum
from typing import Dict
from datetime import timedelta
import logging as log

import isodate

from ..simulators.simulator import Simulator
from ..simulators.traffic_simulator import TrafficSimulator
from ..simulators.temperature_simulator import TemperatureSimulator


class SensorType(Enum):
    TEMPERATURE = "temperature"
    TRAFFIC = "traffic"

    @staticmethod
    def from_str(key: str):
        return SensorType[key.upper()]


class SensorConfigSchema:
    def __init__(self, config: Dict) -> None:
        """
        Represents the schema for the sensor configuration
        :param config: dictionary with the configuration for a single sensor
        """
        self.limit = config.get('limit') or None
        self.begin_date = config.get('begin_date') or None
        self.latitude = config.get('latitude')
        self.longitude = config.get('longitude')

        generation_delay = config.get('generation_delay') or None
        points_spacing = config.get('points_spacing')

        try:
            self.type = SensorType.from_str(config.get('type'))
        except Exception as e:
            log.fatal(
                'Invalid points_spacing value. Must be specified following ISO8601',
                e,
            )
            raise

        try:
            self.points_spacing: timedelta = isodate.parse_duration(points_spacing)
        except Exception as e:
            log.fatal(
                'Invalid points_spacing value. Must be specified following ISO8601',
                e,
            )
            raise

        try:
            self.generation_delay: timedelta = isodate.parse_duration(generation_delay)
        except Exception as e:
            log.fatal(
                'Invalid generation_delay value. Must be specified following ISO8601',
                e,
            )
            raise

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


class ConfigSchema:
    def __init__(self, config: Dict) -> None:
        """
        Represents the schema for the toml configuration file
        :param config: dictionary with the configuration
        """
        self.sensors: Dict[str, SensorConfigSchema] = {
            sensor_id: SensorConfigSchema(sensor)
            for sensor_id, sensor in config['sensors'].items()
        }

        # kafka: Dict[str, str]

    def simulators_generator(self):
        for sensor_id, config in self.sensors.items():
            yield _simulator_factory(sensor_id, config)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _simulator_factory(sensor_id: str, config: SensorConfigSchema) -> Simulator:
    match config.type:
        case SensorType.TEMPERATURE:
            return TemperatureSimulator(
                sensor_id=sensor_id,
                generation_delay=config.generation_delay,
                points_spacing=config.points_spacing,
                latitude=config.latitude,
                longitude=config.longitude,
                begin_date=config.begin_date,
                limit=config.limit,
            )
        case SensorType.TRAFFIC:
            return TrafficSimulator(
                sensor_id=sensor_id,
                generation_delay=config.generation_delay,
                points_spacing=config.points_spacing,
                latitude=config.latitude,
                longitude=config.longitude,
                begin_date=config.begin_date,
                limit=config.limit,
            )
        case _:
            raise NotImplementedError(f'No factory for {type}')
