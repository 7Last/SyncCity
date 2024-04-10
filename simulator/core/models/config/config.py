from typing import Dict

from ..sensor_type import SensorType
from .sensor_config import SensorConfig
from ...simulators.simulator import Simulator
from ...simulators.traffic_simulator import TrafficSimulator
from ...simulators.temperature_simulator import TemperatureSimulator


class Config:
    def __init__(self, config: Dict) -> None:
        """
        Represents the schema for the toml configuration file
        :param config: dictionary with the configuration
        """
        self.sensors: Dict[str, SensorConfig] = {
            sensor_id: SensorConfig(sensor)
            for sensor_id, sensor in config['sensors'].items()
        }

        # TODO: add kafka config

    def simulators_generator(self) -> Simulator:
        for sensor_id, config in self.sensors.items():
            yield _simulator_factory(sensor_id, config)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _simulator_factory(sensor_id: str, config: SensorConfig) -> Simulator:
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
