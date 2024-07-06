from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class AirQualityRawData(RawData):
    def __init__(  # noqa: PLR0913
            self, *, pm25: float, pm10: float, no2: float, o3: float,
            so2: float, latitude: float, longitude: float,
            sensor_name: str, sensor_uuid: UUID, timestamp: datetime = datetime.now(),
            group_name: str | None = None) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         timestamp=timestamp, group_name=group_name)
        self.__pm25 = pm25
        self.__pm10 = pm10
        self.__no2 = no2
        self.__o3 = o3
        self.__so2 = so2

    @property
    def topic(self) -> str:
        return "air_quality"

    def to_json(self) -> Dict[str, any]:
        return {
            "pm25": self.__pm25,
            "pm10": self.__pm10,
            "no2": self.__no2,
            "o3": self.__o3,
            "so2": self.__so2,
            **(super().to_json()),
        }

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, AirQualityRawData):
            return False
        return (super().__eq__(other) and
                self.__pm25 == other.__pm25 and
                self.__pm10 == other.__pm10 and
                self.__no2 == other.__no2 and
                self.__o3 == other.__o3 and
                self.__so2 == other.__so2)

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.__pm25, self.__pm10, self.__no2,
                     self.__o3, self.__so2))

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
