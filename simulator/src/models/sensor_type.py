from enum import Enum


class SensorType(Enum):
    AIR_QUALITY = "air_quality"
    PARKING = "parking"
    RECYCLING_POINT = "recycling_point"
    TEMPERATURE = "temperature"
    TRAFFIC = "traffic"
    CHARGING_STATION="charging_station"

    @staticmethod
    def from_str(key: str) -> "SensorType":
        return SensorType[key.upper()]
