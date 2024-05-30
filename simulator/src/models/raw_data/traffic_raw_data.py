from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class TrafficRawData(RawData):
    def __init__(self, *, vehicles: int, avg_speed: float,
                 latitude: float, longitude: float, sensor_uuid: UUID,
                 sensor_name: str, timestamp: datetime = datetime.now()) -> None:
        """
        :param vehicles: number of vehicles passing through the location
        :param avg_speed: average speed in km/h of the vehicles passing
        through the location
        """
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.vehicles = vehicles
        self.avg_speed = avg_speed

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_traffic_raw_data(self)

    @property
    def topic(self) -> str:
        return "traffic"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, TrafficRawData):
            return False
        return (super().__eq__(other) and
                self.vehicles == other.vehicles and
                self.avg_speed == other.avg_speed)

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.vehicles, self.avg_speed))
