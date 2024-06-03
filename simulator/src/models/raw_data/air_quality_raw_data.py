from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class AirQualityRawData(RawData):
    MAX_OZONE_CONCENTRATION = 800
    MAX_NITROGEN_DIOXIDE_CONCENTRATION = 1000
    MAX_SULFUR_DIOXIDE_CONCENTRATION = 1250
    MAX_PM25_CONCENTRATION = 800
    MAX_PM10_CONCENTRATION = 1200

    def __init__(self, *, pm25: float, pm10: float, no2: float, o3: float,
                 so2: float, latitude: float, longitude: float,
                 sensor_name: str, sensor_uuid: UUID,
                 timestamp: datetime = datetime.now()) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_name=sensor_name, sensor_uuid=sensor_uuid,
                         timestamp=timestamp)
        self.pm25 = pm25
        self.pm10 = pm10
        self.no2 = no2
        self.o3 = o3
        self.so2 = so2

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_air_quality_raw_data(self)

    @property
    def topic(self) -> str:
        return "air_quality"
