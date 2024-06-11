from typing import Dict

from ..models.raw_data.raw_data import RawData
from ..models.raw_data.air_quality_raw_data import AirQualityRawData
from ..models.raw_data.parking_raw_data import ParkingRawData
from ..models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from ..models.raw_data.temperature_raw_data import TemperatureRawData
from ..models.raw_data.traffic_raw_data import TrafficRawData


class SerializerVisitor:

    @staticmethod
    def _serialize_raw_data(raw_data: RawData) -> Dict:
        return {
            "sensor_name": raw_data.sensor_name,
            "sensor_uuid": str(raw_data.sensor_uuid),
            "group_name": raw_data.group_name,
            "latitude": raw_data.latitude,
            "longitude": raw_data.longitude,
            "timestamp": raw_data.timestamp.isoformat(),
        }

    @staticmethod
    def serialize_air_quality_raw_data(raw_data: AirQualityRawData) -> Dict:
        return {
            "pm25": raw_data.pm25,
            "pm10": raw_data.pm10,
            "no2": raw_data.no2,
            "o3": raw_data.o3,
            "so2": raw_data.so2,
            **(SerializerVisitor._serialize_raw_data(raw_data)),
        }
    
    @staticmethod
    def serialize_parking_raw_data(raw_data: ParkingRawData) -> Dict:
        return {
            "is_occupied": raw_data.is_occupied,
            **(SerializerVisitor._serialize_raw_data(raw_data)),
        }

    @staticmethod
    def serialize_recycling_point_raw_data(raw_data: RecyclingPointRawData) -> Dict:
        return {
            "filling": raw_data.filling,
            **(SerializerVisitor._serialize_raw_data(raw_data)),
        }

    @staticmethod
    def serialize_temperature_raw_data(raw_data: TemperatureRawData) -> Dict:
        return {
            "value": raw_data.value,
            **(SerializerVisitor._serialize_raw_data(raw_data)),
        }

    @staticmethod
    def serialize_traffic_raw_data(raw_data: TrafficRawData) -> Dict:
        return {
            "vehicles": raw_data.vehicles,
            "avg_speed": raw_data.avg_speed,
            **(SerializerVisitor._serialize_raw_data(raw_data)),
        }
