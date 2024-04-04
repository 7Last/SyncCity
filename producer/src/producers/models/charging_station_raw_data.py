from datetime import datetime
from enum import Enum
from raw_data import RawData


class ChargingStationRawData(RawData):
    class Status(Enum):
        FREE = 0
        CHARGING = 1
        PAUSED = 2
        COMPLETED = 3
        MALFUNCTION = 4

    def __init__(self, status: Status, latitude: float, longitude: float, altitude: float, sensor_id: str,
                 timestamp: datetime = datetime.now()):
        super().__init__(latitude=latitude, longitude=longitude, altitude=altitude, sensor_id=sensor_id,
                         timestamp=timestamp)
        self.status = status
