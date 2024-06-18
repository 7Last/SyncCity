from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class ChargingStationRawData(RawData):

    def __init__(self, *, is_occupied: bool, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(),
                 group_name: str | None = None) -> None:
        super().__init__(latitude=latitude, longitude=longitude, group_name=group_name,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.is_occupied = is_occupied

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.visit_charging_station_raw_data(self)

    @property
    def topic(self) -> str:
        return "charging_station"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, ChargingStationRawData):
            return False
        return super().__eq__(other) and self.is_occupied == other.is_occupied

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.is_occupied))
