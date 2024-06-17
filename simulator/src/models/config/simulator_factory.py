from .sensor_config import SensorConfig
from ..sensor_type import SensorType
from ...producers.producer_strategy import ProducerStrategy
from ...simulators.air_quality_simulator import AirQualitySimulator
from ...simulators.humidity_simulator import HumiditySimulator
from ...simulators.parking_simulator import ParkingSimulator
from ...simulators.recycling_point_simulator import RecyclingPointSimulator
from ...simulators.simulator import Simulator
from ...simulators.temperature_simulator import TemperatureSimulator
from ...simulators.traffic_simulator import TrafficSimulator
from ...simulators.river_level_simulator import RiverLevelSimulator


def build_simulators(sensors_config: dict[str, any], producer: ProducerStrategy) -> \
        list[Simulator]:
    return [
        SimulatorFactory.generate(name, SensorConfig(config), producer) for name, config
        in sensors_config.items()
    ]


class SimulatorFactory:
    @staticmethod
    def generate(name: str, config: SensorConfig,
                 producer: ProducerStrategy) -> Simulator:
        return _get_simulator(name, config, producer)


def _get_simulator(name: str, config: SensorConfig,  # noqa: PLR0911
                   producer: ProducerStrategy) -> Simulator:
    match config.type:
        case SensorType.AIR_QUALITY:
            return AirQualitySimulator(name, config, producer)
        case SensorType.RECYCLING_POINT:
            return RecyclingPointSimulator(name, config, producer)
        case SensorType.PARKING:
            return ParkingSimulator(name, config, producer)
        case SensorType.TEMPERATURE:
            return TemperatureSimulator(name, config, producer)
        case SensorType.TRAFFIC:
            return TrafficSimulator(name, config, producer)
        case SensorType.HUMIDITY:
            return HumiditySimulator(name, config, producer)
        case SensorType.RIVER_LEVEL:
            return RiverLevelSimulator(name, config, producer)
