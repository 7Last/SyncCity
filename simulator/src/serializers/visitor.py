from abc import ABC, abstractmethod


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
