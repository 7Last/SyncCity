from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class HumidityRawData(RawData):

    def __init__(self, *, value: float, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(),
                 group_name: str | None = None) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp, group_name=group_name)
        self.__value = value

    @property
    def topic(self) -> str:
        return "humidity"

    def to_json(self) -> Dict[str, any]:
        return {
            **super().to_json(),
            "value": self.__value,
        }

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, HumidityRawData):
            return False
        return super().__eq__(other) and self.__value == other.__value

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.__value))
