from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict
from uuid import UUID


class RawData(ABC):
    def __init__(self, *, sensor_name: str, latitude: float, longitude: float,
                 sensor_uuid: UUID, timestamp: datetime = datetime.now()) -> None:
        self.sensor_name = sensor_name
        self.latitude = latitude
        self.longitude = longitude
        self.sensor_uuid = sensor_uuid
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'

    @abstractmethod
    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        pass

    @property
    @abstractmethod
    def topic(self) -> str:
        pass

    def value_subject(self) -> str:
        return f'{self.topic}-value'

    def key_subject(self) -> str:
        return f'{self.topic}-key'

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, RawData):
            return False
        return self.sensor_name == other.sensor_name and \
            self.latitude == other.latitude and \
            self.longitude == other.longitude and \
            self.sensor_uuid == other.sensor_uuid and \
            self.timestamp == other.timestamp

    def __hash__(self) -> int:
        return hash((
            self.sensor_name,
            self.latitude,
            self.longitude,
            self.sensor_uuid,
            self.timestamp,
        ))
