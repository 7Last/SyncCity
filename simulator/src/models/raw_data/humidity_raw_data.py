from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class HumidityRawData(RawData):

    def __init__(self, *, value: float, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(),
                 group_name: str | None = None) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp, group_name=group_name)
        self.value = value

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.visit_humidity_raw_data(self)

    @property
    def topic(self) -> str:
        return "humidity"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, HumidityRawData):
            return False
        return super().__eq__(other) and self.value == other.value

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.value))
