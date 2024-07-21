from datetime import datetime
from uuid import UUID

from .raw_data import RawData


class ParkingRawData(RawData):

    def __init__(self, *, is_occupied: bool, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(),
                 group_name: str | None = None) -> None:
        super().__init__(latitude=latitude, longitude=longitude, group_name=group_name,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.__is_occupied = is_occupied

    @property
    def topic(self) -> str:
        return "parking"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, ParkingRawData):
            return False
        return super().__eq__(other) and self.__is_occupied == other.__is_occupied

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.__is_occupied))
