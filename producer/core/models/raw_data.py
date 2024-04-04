from datetime import datetime
from abc import ABC


class RawData(ABC):
    def __init__(self, latitude: float, longitude: float, altitude: float, sensor_id: str,
                 timestamp: datetime = datetime.now()):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.sensor_id = sensor_id
        self.timestamp = timestamp

    def __str__(self):
        return f'{self.__class__.__name__} {self.__dict__}'
