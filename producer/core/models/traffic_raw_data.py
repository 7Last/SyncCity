from datetime import datetime

from ..models.raw_data import RawData


class TrafficRawData(RawData):
    def __init__(self, *, vehicles_per_unit: float, avg_speed_per_unit: float,
                 latitude: float, longitude: float, sensor_id: str,
                 timestamp: datetime = datetime.now()) -> None:
        """:param vehicles_per_unit: number of vehicles passing through the location
         per second
        :param avg_speed_per_unit: average speed in km/h of the vehicles passing through
        the location
        """
        super().__init__(latitude=latitude, longitude=longitude, sensor_id=sensor_id,
                         timestamp=timestamp)
        self.vehicles_per_unit = vehicles_per_unit
        self.avg_speed_per_unit = avg_speed_per_unit
