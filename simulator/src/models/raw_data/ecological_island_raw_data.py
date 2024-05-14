import random
from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class EcologicalIslandRawData(RawData):

    def __init__(self, *, starting_filling: int, filling_speed: float, filling_value: float, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str, timestamp: datetime = datetime.now()) -> None:
        """
        :param starting_filling: initial filling percentage of the ecological island
        :param filling_speed: filling speed in percentage per hour (?)\
        :param filling_value: filling value in percentage
        """
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.starting_filling = starting_filling
        self.filling_speed = filling_speed
        self.filling_value = filling_value

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_ecological_island_raw_data(self)

    @property
    def topic(self) -> str:
        return "ecological_island"
