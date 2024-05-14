from enum import Enum


class SensorType(Enum):
    TEMPERATURE = "temperature"
    TRAFFIC = "traffic"
    ECOLOGICAL_ISLAND = "ecological_island"

    @staticmethod
    def from_str(key: str):  # noqa: ANN205
        return SensorType[key.upper()]
