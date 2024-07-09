from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class ChargingStationRawData(RawData):

    def __init__(self, *, vehicle_type: str, battery_level: float, kwh_supplied: float,  # noqa: PLR0913
                 remaining_charge_time: int, elapsed_time: int, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(),
                 group_name: str | None = None) -> None:
        super().__init__(latitude=latitude, longitude=longitude, group_name=group_name,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.__vehicle_type = vehicle_type
        self.__battery_level = battery_level
        self.__kwh_supplied = kwh_supplied
        self.__remaining_charge_time = remaining_charge_time
        self.__elapsed_time = elapsed_time

    @property
    def topic(self) -> str:
        return "charging_station"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, ChargingStationRawData):
            return False
        return (super().__eq__(other) and
                self.__vehicle_type == other.__vehicle_type and
                self.__battery_level == other.__battery_level and
                self.__kwh_supplied == other.__kwh_supplied and
                self.__remaining_charge_time == other.__remaining_charge_time and
                self.__elapsed_time == other.__elapsed_time)

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.__vehicle_type, self.__battery_level,
                     self.__kwh_supplied, self.__remaining_charge_time,
                     self.__elapsed_time))

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
