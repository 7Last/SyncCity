from typing import Dict

from ..models.raw_data.raw_data import RawData
from ..models.raw_data.temperature_raw_data import TemperatureRawData
from ..models.raw_data.traffic_raw_data import TrafficRawData
from ..models.sensor_type import SensorType


class SerializerVisitor:

    @staticmethod
    def _serialize_raw_data(raw_data: RawData) -> Dict:
        return {
            "sensor_uuid": str(raw_data.sensor_uuid),
            "latitude": raw_data.latitude,
            "longitude": raw_data.longitude,
            "timestamp": raw_data.timestamp.isoformat(),
        }

    @staticmethod
    def serialize_temperature_raw_data(raw_data: TemperatureRawData) -> Dict:
        return {
            "type": SensorType.TEMPERATURE.value,
            "value_1": raw_data.value,
            **(SerializerVisitor._serialize_raw_data(raw_data)),
        }

    @staticmethod
    def serialize_traffic_raw_data(raw_data: TrafficRawData) -> Dict:
        return {
            "type": SensorType.TRAFFIC.value,
            "value_1": raw_data.vehicles_per_hour,
            "value_2": raw_data.avg_speed,
            **(SerializerVisitor._serialize_raw_data(raw_data)),
        }
