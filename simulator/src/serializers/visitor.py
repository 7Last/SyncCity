from abc import ABC, abstractmethod

from ..models.raw_data.air_quality_raw_data import AirQualityRawData
from ..models.raw_data.parking_raw_data import ParkingRawData
from ..models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from ..models.raw_data.temperature_raw_data import TemperatureRawData
from ..models.raw_data.traffic_raw_data import TrafficRawData
from ..models.raw_data.charging_station_raw_data import ChargingStationRawData
from ..models.raw_data.precipitation_raw_data import PrecipitationRawData
from ..models.raw_data.river_level_raw_data import RiverLevelRowData
from ..models.raw_data.humidity_raw_data import HumidityRawData

class Visitor(ABC):
    @staticmethod
    @abstractmethod
    def visit_air_quality_raw_data(raw_data: 'AirQualityRawData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_parking_raw_data(raw_data: 'ParkingRawData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_recycling_point_raw_data(raw_data: 'RecyclingPointRawData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_temperature_raw_data(raw_data: 'TemperatureRawData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_traffic_raw_data(raw_data: 'TrafficRawData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_charging_station_raw_data(raw_data: 'ChargingStationRawData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_precipitation_raw_data(raw_data: 'PrecipitationRawData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_river_level_raw_data(raw_data: 'RiverLevelRowData') -> any:
        pass

    @staticmethod
    @abstractmethod
    def visit_humidity_raw_data(raw_data: 'HumidityRawData') -> any:
        pass