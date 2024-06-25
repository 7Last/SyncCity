from datetime import UTC
from typing import Dict

from ...serializers.visitor.converter_visitor import ConverterVisitor
from ...models.raw_data.air_quality_raw_data import AirQualityRawData
from ...models.raw_data.parking_raw_data import ParkingRawData
from ...models.raw_data.raw_data import RawData
from ...models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from ...models.raw_data.temperature_raw_data import TemperatureRawData
from ...models.raw_data.traffic_raw_data import TrafficRawData
from ...models.raw_data.charging_station_raw_data import ChargingStationRawData
from ...models.raw_data.precipitation_raw_data import PrecipitationRawData
from ...models.raw_data.river_level_raw_data import RiverLevelRawData
from ...models.raw_data.humidity_raw_data import HumidityRawData


class JsonConverterVisitor(ConverterVisitor):

    @staticmethod
    def _visit_raw_data(raw_data: RawData) -> Dict:
        return {
            "sensor_name": raw_data.sensor_name,
            "sensor_uuid": str(raw_data.sensor_uuid),
            "group_name": raw_data.group_name,
            "latitude": raw_data.latitude,
            "longitude": raw_data.longitude,
            "timestamp": raw_data.timestamp.astimezone(tz=UTC).isoformat(),
        }

    @staticmethod
    def visit_air_quality_raw_data(raw_data: AirQualityRawData) -> Dict:
        return {
            "pm25": raw_data.pm25,
            "pm10": raw_data.pm10,
            "no2": raw_data.no2,
            "o3": raw_data.o3,
            "so2": raw_data.so2,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }

    @staticmethod
    def visit_parking_raw_data(raw_data: ParkingRawData) -> Dict:
        return {
            "is_occupied": raw_data.is_occupied,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }

    @staticmethod
    def visit_recycling_point_raw_data(raw_data: RecyclingPointRawData) -> Dict:
        return {
            "filling": raw_data.filling,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }

    @staticmethod
    def visit_temperature_raw_data(raw_data: TemperatureRawData) -> Dict:
        return {
            "value": raw_data.value,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }

    @staticmethod
    def visit_traffic_raw_data(raw_data: TrafficRawData) -> Dict:
        return {
            "vehicles": raw_data.vehicles,
            "avg_speed": raw_data.avg_speed,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }

    @staticmethod
    def visit_humidity_raw_data(raw_data: HumidityRawData) -> Dict:
        return {
            "value": raw_data.value,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }

    @staticmethod
    def visit_charging_station_raw_data(raw_data: ChargingStationRawData) -> Dict:
        return {
            "vehicle_type": raw_data.vehicle_type,
            "battery_level": raw_data.battery_level,
            "kwh_supplied": raw_data.kwh_supplied,
            "remaining_charge_time": raw_data.remaining_charge_time,
            "elapsed_time": raw_data.elapsed_time,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }
    @staticmethod
    def visit_precipitation_raw_data(raw_data: PrecipitationRawData) -> Dict:
        return {
            "value": raw_data.value,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }

    @staticmethod
    def visit_river_level_raw_data(raw_data: RiverLevelRawData) -> Dict:
        return {
            "value": raw_data.value,
            **(JsonConverterVisitor._visit_raw_data(raw_data)),
        }
