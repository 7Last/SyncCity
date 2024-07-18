from ..models.config.sensor_config import SensorConfig
from ..models.sensor_type import SensorType
from ..simulators.air_quality_simulator_strategy import AirQualitySimulatorStrategy
from ..simulators.charging_station_simulator_strategy import \
    ChargingStationSimulatorStrategy
from ..simulators.humidity_simulator_strategy import HumiditySimulatorStrategy
from ..simulators.parking_simulator_strategy import ParkingSimulatorStrategy
from ..simulators.precipitation_simulator_strategy import PrecipitationSimulatorStrategy
from ..simulators.recycling_point_simulator_strategy import \
    RecyclingPointSimulatorStrategy
from ..simulators.river_level_simulator_strategy import RiverLevelSimulatorStrategy
from ..simulators.simulator_strategy import SimulatorStrategy
from ..simulators.temperature_simulator_strategy import TemperatureSimulatorStrategy
from ..simulators.traffic_simulator_strategy import TrafficSimulatorStrategy


def build_simulators(sensors_config: dict[str, any]) -> list[SimulatorStrategy]:
    return [
        SimulatorFactory.build(name, SensorConfig(config)) for name, config
        in sensors_config.items()
    ]


class SimulatorFactory:
    @staticmethod
    def build(name: str, config: SensorConfig) -> SimulatorStrategy:
        return _build_simulator(name, config)


def _build_simulator(name: str, config: SensorConfig) -> SimulatorStrategy:
    match config.type():
        case SensorType.AIR_QUALITY:
            return AirQualitySimulatorStrategy(name, config)
        case SensorType.RECYCLING_POINT:
            return RecyclingPointSimulatorStrategy(name, config)
        case SensorType.PARKING:
            return ParkingSimulatorStrategy(name, config)
        case SensorType.TEMPERATURE:
            return TemperatureSimulatorStrategy(name, config)
        case SensorType.TRAFFIC:
            return TrafficSimulatorStrategy(name, config)
        case SensorType.HUMIDITY:
            return HumiditySimulatorStrategy(name, config)
        case SensorType.RIVER_LEVEL:
            return RiverLevelSimulatorStrategy(name, config)
        case SensorType.PRECIPITATION:
            return PrecipitationSimulatorStrategy(name, config)
        case SensorType.CHARGING_STATION:
            return ChargingStationSimulatorStrategy(name, config)
