from .sensor_config import SensorConfig
from ..sensor_type import SensorType
from ...simulators.air_quality_simulator import AirQualitySimulator
from ...simulators.parking_simulator import ParkingSimulator
from ...simulators.recycling_point_simulator import RecyclingPointSimulator
from ...simulators.simulator import Simulator
from ...simulators.temperature_simulator import TemperatureSimulator
from ...simulators.traffic_simulator import TrafficSimulator
from ...simulators.river_level_simulator import RiverLevelSimulator

def build_simulators(sensors_config: dict[str, any]) -> list[Simulator]:
    return [
        SimulatorFactory.generate(name, SensorConfig(config)) for name, config
        in sensors_config.items()
    ]


class SimulatorFactory:
    @staticmethod
    def generate(name: str, config: SensorConfig) -> Simulator:
        return _get_simulator(name, config)


def _get_simulator(name: str, config: SensorConfig) -> Simulator:  # noqa: PLR0911
    match config.type:
        case SensorType.AIR_QUALITY:
            return AirQualitySimulator(name, config)
        case SensorType.RECYCLING_POINT:
            return RecyclingPointSimulator(name, config)
        case SensorType.PARKING:
            return ParkingSimulator(name, config)
        case SensorType.TEMPERATURE:
            return TemperatureSimulator(name, config)
        case SensorType.TRAFFIC:
            return TrafficSimulator(name, config)
        case SensorType.RIVER_LEVEL:
            return RiverLevelSimulator(name, config)
