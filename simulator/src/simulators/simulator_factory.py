from ..models.config.sensor_config import SensorConfig
from ..models.sensor_type import SensorType
from ..producers.producer_strategy import ProducerStrategy
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


def build_simulators(sensors_config: dict[str, any], producer: ProducerStrategy) -> \
        list[SimulatorStrategy]:
    return [
        SimulatorFactory.generate(name, SensorConfig(config), producer) for name, config
        in sensors_config.items()
    ]


class SimulatorFactory:
    @staticmethod
    def generate(name: str, config: SensorConfig,
                 producer: ProducerStrategy) -> SimulatorStrategy:
        return _get_simulator(name, config, producer)


def _get_simulator(name: str, config: SensorConfig,  # noqa: PLR0911
                   producer: ProducerStrategy) -> SimulatorStrategy:
    match config.type():
        case SensorType.AIR_QUALITY:
            return AirQualitySimulatorStrategy(name, config, producer)
        case SensorType.RECYCLING_POINT:
            return RecyclingPointSimulatorStrategy(name, config, producer)
        case SensorType.PARKING:
            return ParkingSimulatorStrategy(name, config, producer)
        case SensorType.TEMPERATURE:
            return TemperatureSimulatorStrategy(name, config, producer)
        case SensorType.TRAFFIC:
            return TrafficSimulatorStrategy(name, config, producer)
        case SensorType.HUMIDITY:
            return HumiditySimulatorStrategy(name, config, producer)
        case SensorType.RIVER_LEVEL:
            return RiverLevelSimulatorStrategy(name, config, producer)
        case SensorType.PRECIPITATION:
            return PrecipitationSimulatorStrategy(name, config, producer)
        case SensorType.CHARGING_STATION:
            return ChargingStationSimulatorStrategy(name, config, producer)
