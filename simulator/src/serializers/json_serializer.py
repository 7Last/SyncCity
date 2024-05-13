from typing import Dict

from ..models.raw_data.raw_data import RawData
from ..models.raw_data.temperature_raw_data import TemperatureRawData
from ..models.raw_data.traffic_raw_data import TrafficRawData


class JSONSerializer:

    @staticmethod
    def _serialize_raw_data(raw_data: RawData) -> Dict:
        return {
            "sensor_name": raw_data.sensor_name,
            "sensor_uuid": str(raw_data.sensor_uuid),
            "latitude": raw_data.latitude,
            "longitude": raw_data.longitude,
            "timestamp": raw_data.timestamp.isoformat(),
        }

    @staticmethod
    def serialize_temperature_raw_data(raw_data: TemperatureRawData) -> Dict:
        return {
            "value": raw_data.value,
            **(JSONSerializer._serialize_raw_data(raw_data)),
        }

    @staticmethod
    def serialize_traffic_raw_data(raw_data: TrafficRawData) -> Dict:
        return {
            "vehicles_per_hour": raw_data.vehicles_per_hour,
            "avg_speed": raw_data.avg_speed,
            **(JSONSerializer._serialize_raw_data(raw_data)),
        }
