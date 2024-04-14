from datetime import datetime
from typing import Dict

from .raw_data import RawData


class TrafficRawData(RawData):
    def __init__(self, *, vehicles_per_hour: float, avg_speed: float,
                 latitude: float, longitude: float, sensor_id: str,
                 timestamp: datetime = datetime.now()) -> None:
        """
        :param vehicles_per_hour: number of vehicles passing through the location
        :param avg_speed: average speed in km/h of the vehicles passing
        through the location
        """
        super().__init__(latitude=latitude, longitude=longitude, sensor_id=sensor_id,
                         timestamp=timestamp)
        self.vehicles_per_hour = vehicles_per_hour
        self.avg_speed = avg_speed

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_traffic_raw_data(self)
