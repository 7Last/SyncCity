from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict
from uuid import UUID


class RawData(ABC):
    def __init__(self, *, latitude: float, longitude: float, sensor_uuid: UUID,
                 timestamp: datetime = datetime.now()) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.sensor_uuid = sensor_uuid
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'

    @abstractmethod
    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        pass
