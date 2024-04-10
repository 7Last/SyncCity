from abc import ABC, abstractmethod
from typing import Dict
from datetime import datetime


class RawData(ABC):
    def __init__(self, *, latitude: float, longitude: float, sensor_id: str,
                 timestamp: datetime = datetime.now()) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.sensor_id = sensor_id
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'

    @abstractmethod
    def serialize(self) -> Dict:
        return {
            "sensor_id": self.sensor_id,
            "lat": self.latitude,
            "lon": self.longitude,
            "timestamp": self.timestamp.isoformat(),
        }
