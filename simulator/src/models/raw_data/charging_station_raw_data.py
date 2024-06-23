from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class ChargingStationRawData(RawData):

    def __init__(self, *, vehicle_type: str, battery_level: float, kwh_supplied: float,
                 remaining_charge_time: int, elapsed_time: int, latitude: float,
                 longitude: float, sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now(),
                 group_name: str | None = None) -> None:
        super().__init__(latitude=latitude, longitude=longitude, group_name=group_name,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.vehicle_type = vehicle_type
        self.battery_level = battery_level
        self.kwh_supplied = kwh_supplied
        self.remaining_charge_time = remaining_charge_time
        self.elapsed_time = elapsed_time

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.visit_charging_station_raw_data(self)

    @property
    def topic(self) -> str:
        return "charging_station"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, ChargingStationRawData):
            return False
        return (super().__eq__(other) and
                self.vehicle_type == other.vehicle_type and
                self.battery_level == other.battery_level and
                self.kwh_supplied == other.kwh_supplied and
                self.remaining_charge_time == other.remaining_charge_time and
                self.elapsed_time == other.elapsed_time)

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.vehicle_type, self.battery_level,
                     self.kwh_supplied, self.remaining_charge_time, self.elapsed_time))

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
