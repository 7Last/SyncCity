from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData
from ...serializers.visitor import Visitor


class AirQualityRawData(RawData):
    def __init__(  # noqa: PLR0913
            self, *, pm25: float, pm10: float, no2: float, o3: float,
            so2: float, latitude: float, longitude: float, group_name: str | None,
            sensor_name: str, sensor_uuid: UUID,
            timestamp: datetime = datetime.now()) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         timestamp=timestamp, group_name=group_name)
        self.pm25 = pm25
        self.pm10 = pm10
        self.no2 = no2
        self.o3 = o3
        self.so2 = so2

    def accept(self, visitor: 'Visitor') -> Dict[str, any]:
        return visitor.visit_air_quality_raw_data(self)

    @property
    def topic(self) -> str:
        return "air_quality"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, AirQualityRawData):
            return False
        return (super().__eq__(other) and
                self.pm25 == other.pm25 and
                self.pm10 == other.pm10 and
                self.no2 == other.no2 and
                self.o3 == other.o3 and
                self.so2 == other.so2)

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.pm25, self.pm10, self.no2,
                     self.o3, self.so2))

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
