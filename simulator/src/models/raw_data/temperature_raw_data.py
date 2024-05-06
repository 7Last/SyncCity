from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class TemperatureRawData(RawData):
    def __init__(self, *, value: float, latitude: float, longitude: float,
                 sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now()) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, timestamp=timestamp,
                         sensor_name=sensor_name)
        self.value = value

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_temperature_raw_data(self)

    @property
    def topic(self) -> str:
        return "temperature"
