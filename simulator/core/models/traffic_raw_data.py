from datetime import datetime

from ..models.raw_data import RawData


class TrafficRawData(RawData):
    def __init__(self, *, vehicles_per_minute: float, avg_speed_per_minute: float,
                 latitude: float, longitude: float, sensor_id: str,
                 timestamp: datetime = datetime.now()) -> None:
        """:param vehicles_per_minute: number of vehicles passing through the location
         per minute
        :param avg_speed_per_minute: average speed in km/h of the vehicles passing through
        the location
        """
        super().__init__(latitude=latitude, longitude=longitude, sensor_id=sensor_id,
                         timestamp=timestamp)
        self.vehicles_per_minute = vehicles_per_minute
        self.avg_speed_per_minute = avg_speed_per_minute
