from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class RecyclingPointRawData(RawData):

    def __init__(self, *, filling: float, latitude: float, group_name: str | None,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now()) -> None:
        """
        :param filling: filling value in percentage
        """
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp, group_name=group_name)
        self.filling = filling

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_recycling_point_raw_data(self)

    @property
    def topic(self) -> str:
        return "recycling_point"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, RecyclingPointRawData):
            return False
        return super().__eq__(other) and self.filling == other.filling

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.filling))
