from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict
from uuid import UUID


class RawData(ABC):
    def __init__(self, *, sensor_name: str, latitude: float, longitude: float,
                 group_name: str | None, sensor_uuid: UUID,
                 timestamp: datetime = datetime.now()) -> None:
        self._sensor_name = sensor_name
        self._latitude = latitude
        self._longitude = longitude
        self._sensor_uuid = sensor_uuid
        self._timestamp = timestamp
        self._group_name = group_name

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'

    @property
    @abstractmethod
    def topic(self) -> str:
        pass

    def sensor_uuid(self) -> UUID:
        return self._sensor_uuid

    def sensor_name(self) -> str:
        return self._sensor_name

    def value_subject(self) -> str:
        return f'{self.topic}-value'

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, RawData):
            return False
        return self._sensor_name == other._sensor_name and \
            self._group_name == other._group_name and \
            self._latitude == other._latitude and \
            self._longitude == other._longitude and \
            self._sensor_uuid == other._sensor_uuid and \
            self._timestamp == other._timestamp

    def __hash__(self) -> int:
        return hash((
            self._sensor_name,
            self._group_name,
            self._latitude,
            self._longitude,
            self._sensor_uuid,
            self._timestamp,
        ))
