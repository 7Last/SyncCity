import unittest
from datetime import datetime, UTC
from uuid import UUID

from simulator.src.models.raw_data.recycling_point_raw_data import RecyclingPointRawData
from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.models.raw_data.traffic_raw_data import TrafficRawData
from simulator.src.models.raw_data.air_quality_raw_data import AirQualityRawData
from simulator.src.models.raw_data.parking_raw_data import ParkingRawData
from simulator.src.models.raw_data.charging_station_raw_data import ChargingStationRawData
from simulator.src.models.raw_data.humidity_raw_data import HumidityRawData
from simulator.src.models.raw_data.precipitation_raw_data import PrecipitationRawData
from simulator.src.models.raw_data.river_level_raw_data import RiverLevelRawData
from simulator.src.serializers.serializer_visitor import SerializerVisitor


class TestSerializerVisitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.datetime = datetime(
            year=2024,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            tzinfo=UTC,
        )

    def test_serialize_temperature_raw_data(self) -> None:
        temperature_raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "value": 0.0,
        }
        self.assertEqual(visitor.visit_temperature_raw_data(temperature_raw_data),
                         expected)

    def test_serialize_temperature_raw_data_without_group(self) -> None:
        temperature_raw_data = TemperatureRawData(
            sensor_name="sensor_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": None,
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "value": 0.0,
        }
        self.assertEqual(visitor.visit_temperature_raw_data(temperature_raw_data),
                         expected)

    def test_serialize_traffic_raw_data(self) -> None:
        traffic_raw_data = TrafficRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            vehicles=0,
            avg_speed=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "vehicles": 0,
            "avg_speed": 0.0,
        }
        self.assertEqual(visitor.visit_traffic_raw_data(traffic_raw_data),
                         expected)

    def test_serialize_recycling_point_raw_data(self) -> None:
        recycling_point_raw_data = RecyclingPointRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            filling=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "filling": 0.0,
        }
        self.assertEqual(
            visitor.visit_recycling_point_raw_data(recycling_point_raw_data),
            expected)
        
    def test_serialize_air_quality_raw_data(self) -> None:
        air_quality_raw_data = AirQualityRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            pm25=0.0,
            pm10=0.0,
            no2=0.0,
            o3=0.0,
            so2=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "pm25": 0.0,
            "pm10": 0.0,
            "no2": 0.0,
            "o3": 0.0,
            "so2":0.0,

        }
        self.assertEqual(
            visitor.visit_air_quality_raw_data(air_quality_raw_data),
            expected)

    def test_serialize_parking_raw_data(self) -> None:
        parking_raw_data = ParkingRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            is_occupied=0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "is_occupied": 0,
        }
        self.assertEqual(
            visitor.visit_parking_raw_data(parking_raw_data),
            expected)
        
    def test_charging_station_raw_data(self) -> None:
        charging_station_raw_data = ChargingStationRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            is_being_used=0,
            kwh_supplied=0.0,
            remaining_charge_time=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "is_being_used":0,
            "kwh_supplied": 0.0,
            "remaining_charge_time": 0.0,
        }
        self.assertEqual(
            visitor.visit_charging_station_raw_data(charging_station_raw_data),
            expected)
        
    def test_humidity_raw_data(self) -> None:
        humidity_raw_data = HumidityRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "value": 0.0,
        }
        self.assertEqual(
            visitor.visit_humidity_raw_data(humidity_raw_data),
            expected)
        
    def test_precipitation_raw_data(self) -> None:
        precipitation_raw_data = PrecipitationRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "value": 0.0,
        }
        self.assertEqual(
            visitor.visit_precipitation_raw_data(precipitation_raw_data),
            expected)
        
    def test_river_level_raw_data(self) -> None:
        river_level_raw_data = RiverLevelRawData(
            sensor_name="sensor_name",
            group_name="group_name",
            sensor_uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
            latitude=0.0,
            longitude=0.0,
            timestamp=self.datetime,
            value=0.0,
        )
        visitor = SerializerVisitor()

        expected = {
            "sensor_name": "sensor_name",
            "group_name": "group_name",
            "sensor_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": "2024-01-01T00:00:00+00:00",
            "value": 0.0,
        }
        self.assertEqual(
            visitor.visit_river_level_raw_data(river_level_raw_data),
            expected)