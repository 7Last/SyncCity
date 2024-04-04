from raw_data import RawData
from datetime import datetime


class TrafficRawData(RawData):
    def __init__(self, vehicles_count: int, avg_speed: float, latitude: float, longitude: float,
                 altitude: float, sensor_id: str, timestamp: datetime = datetime.now()):
        """
        :param vehicles_count: number of vehicles passing through the location per minute
        :param avg_speed: average speed of the vehicles passing through the location in km/h
        """
        super().__init__(latitude=latitude, longitude=longitude, altitude=altitude, sensor_id=sensor_id,
                         timestamp=timestamp)
        self.vehicles_count = vehicles_count
        self.avg_speed = avg_speed
