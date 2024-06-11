from typing import Iterable, Dict

from .sensor_config import SensorConfig
from ..sensor_type import SensorType
from ...simulators.air_quality_simulator import AirQualitySimulator
from ...simulators.simulator import Simulator
from ...simulators.temperature_simulator import TemperatureSimulator
from ...simulators.traffic_simulator import TrafficSimulator
from ...simulators.recycling_point_simulator import RecyclingPointSimulator
from ...simulators.humidity_simulator import HumiditySimulator


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
        case SensorType.RECYCLING_POINT:
            return RecyclingPointSimulator(
                sensor_name=sensor_name,
                sensor_uuid=config.uuid,
                generation_delay=config.generation_delay,
                points_spacing=config.points_spacing,
                latitude=config.latitude,
                longitude=config.longitude,
                begin_date=config.begin_date,
                limit=config.limit,
            )
        case SensorType.HUMIDITY:
            return HumiditySimulator(
                sensor_name=sensor_name,
                sensor_uuid=config.uuid,
                generation_delay=config.generation_delay,
                points_spacing=config.points_spacing,
                latitude=config.latitude,
                longitude=config.longitude,
                begin_date=config.begin_date,
                limit=config.limit,
            )
        case SensorType.AIR_QUALITY:
            return AirQualitySimulator(
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
