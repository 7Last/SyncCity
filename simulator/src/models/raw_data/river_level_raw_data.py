from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class RiverLevelRowData(RawData):
    def __init__(self, *, value: float, latitude: float, longitude: float,
                 sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(), group_name: str | None = None,
                 ) -> None:
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, timestamp=timestamp,
                         sensor_name=sensor_name, group_name=group_name)
        self.value = value

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.visit_river_level_raw_data(self)

    @property
    def topic(self) -> str:
        return "river_level"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, RiverLevelRowData):
            return False
        return self.value == other.value and super().__eq__(other)

    def __hash__(self) -> int:
        return hash((self.value, super().__hash__()))
