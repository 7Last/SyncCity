from enum import Enum


class SensorType(Enum):
    AIR_QUALITY = "air_quality"
    TEMPERATURE = "temperature"
    TRAFFIC = "traffic"
    RECYCLING_POINT = "recycling_point"
    HUMIDITY = "humidity"

    @staticmethod
    def from_str(key: str):  # noqa: ANN205
        return SensorType[key.upper()]
