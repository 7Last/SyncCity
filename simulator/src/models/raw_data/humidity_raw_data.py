from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class HumidityRawData(RawData):

    def __init__(self, *, filling: float, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now()) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_humidity_raw_data(self)

    @property
    def topic(self) -> str:
        return "humidity"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, HumidityRawData):
            return False
        return super().__eq__(other) and self.filling == other.filling

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.filling))
