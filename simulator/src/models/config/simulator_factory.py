from typing import Iterable, Dict

from .sensor_config import SensorConfig
from ..sensor_type import SensorType
from ...simulators.simulator import Simulator
from ...simulators.temperature_simulator import TemperatureSimulator
from ...simulators.traffic_simulator import TrafficSimulator
from ...simulators.ecological_island_simulator import EcologicalIslandSimulator


def simulators_generator(sensors: Dict[str, any]) -> Iterable[Simulator]:
    """
    Generates the _simulators based on the configuration
    """
    for sensor_name, config in sensors.items():
        sensor_config = SensorConfig(config=config)
        yield _simulator_factory(sensor_name, sensor_config)


def _simulator_factory(sensor_name: str, config: SensorConfig) -> Simulator:
    """
    Factory method to create the _simulators based on the configuration
    """
    match config.type:
        case SensorType.TEMPERATURE:
            return TemperatureSimulator(
                sensor_name=sensor_name,
                sensor_uuid=config.uuid,
                generation_delay=config.generation_delay,
                points_spacing=config.points_spacing,
                latitude=config.latitude,
                longitude=config.longitude,
                begin_date=config.begin_date,
                limit=config.limit,
            )
        case SensorType.TRAFFIC:
            return TrafficSimulator(
                sensor_name=sensor_name,
                sensor_uuid=config.uuid,
                generation_delay=config.generation_delay,
                points_spacing=config.points_spacing,
                latitude=config.latitude,
                longitude=config.longitude,
                begin_date=config.begin_date,
                limit=config.limit,
            )
        case SensorType.ECOLOGICAL_ISLAND:
            return EcologicalIslandSimulator(
                sensor_name=sensor_name,
                sensor_uuid=config.uuid,
                generation_delay=config.generation_delay,
                points_spacing=config.points_spacing,
                latitude=config.latitude,
                longitude=config.longitude,
                begin_date=config.begin_date,
                limit=config.limit,
            )
        case _:
            raise NotImplementedError(f'No factory for {type}')
