from enum import Enum


class SensorType(Enum):
    TEMPERATURE = "temperature"
    TRAFFIC = "traffic"

    @staticmethod
    def from_str(key: str):  # noqa: ANN205
        return SensorType[key.upper()]
