from datetime import datetime
from uuid import UUID

from .raw_data import RawData


class TrafficRawData(RawData):
    def __init__(self, *, vehicles: int, avg_speed: float, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(),
                 group_name: str | None = None) -> None:
        """
        :param vehicles: number of vehicles passing through the location
        :param avg_speed: average speed in km/h of the vehicles passing
        through the location
        """
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp, group_name=group_name)
        self.__vehicles = vehicles
        self.__avg_speed = avg_speed

    @property
    def topic(self) -> str:
        return "traffic"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, TrafficRawData):
            return False
        return (super().__eq__(other) and
                self.__vehicles == other.__vehicles and
                self.__avg_speed == other.__avg_speed)

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.__vehicles, self.__avg_speed))
