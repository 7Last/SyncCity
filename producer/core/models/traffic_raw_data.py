from ..models.raw_data import RawData
from datetime import datetime


class TrafficRawData(RawData):
    def __init__(self, vehicles_per_unit: int, avg_speed: float, latitude: float, longitude: float,
                 altitude: float, sensor_id: str, timestamp: datetime = datetime.now()):
        """
        :param vehicles_per_unit: number of vehicles passing through the location per second
        :param avg_speed: average speed in km/h of the vehicles passing through the location
        """
        super().__init__(latitude=latitude, longitude=longitude, altitude=altitude, sensor_id=sensor_id,
                         timestamp=timestamp)
        self.vehicles_per_unit = vehicles_per_unit
        self.avg_speed = avg_speed
