import random
from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData

class EcologicalIslandRawData(RawData):
    '''
    __min_filling = 5
    __max_filling = 95
    __filling_speed = 2.5
    '''

    def __init__(self, *, starting_filling: int, max_filling: float, min_filling: float, filling_speed: float, filling_value: float, latitude: float, longitude: float,
                 sensor_uuid: UUID, sensor_name: str, timestamp: datetime = datetime.now()) -> None:
        """
        :param starting_filling: initial filling percentage of the ecological island
        :param max_filling: maximum filling percentage of the ecological island
        :param min_filling: minimum filling percentage of the ecological island
        :param filling_speed: filling speed in percentage per hour (?)\
        :param filling_value: filling value in percentage
        """
        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.starting_filling = starting_filling
        self.max_filling = max_filling
        self.min_filling = min_filling
        self.filling_speed = filling_speed
        self.filling_value = filling_value

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_ecological_island_raw_data(self)
    
    '''
    def generate_data(self):
        actual_filling = self.starting_filling + self.filling_speed
        actual_filling = max(self.__min_filling, min(self.__max_filling, actual_filling))

        return actual_filling
    '''

    @property
    def topic(self) -> str:
        return "ecological_island"
