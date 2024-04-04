from datetime import datetime
from .raw_data import RawData


class TemperatureRawData(RawData):
    def __init__(self, value: float, latitude: float, longitude: float, altitude: float, sensor_id: str,
                 timestamp: datetime = datetime.now()):
        super().__init__(latitude=latitude, longitude=longitude, altitude=altitude, sensor_id=sensor_id,
                         timestamp=timestamp)
        self.value = value
