import random
from datetime import datetime, timedelta

from .simulator import Simulator
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.charging_station_raw_data import ChargingStationRawData
from ..producers.producer_strategy import ProducerStrategy


class ChargingStationSimulator(Simulator):
    def __init__(self, sensor_name: str, config: SensorConfig, producer: ProducerStrategy) -> None:
        super().__init__(sensor_name, config, producer)
        self._charging_station_power = self._initialize_charging_power()

    def data(self) -> ChargingStationRawData:
        kwh_supplied = self._generate_energy_consumption()
        data = ChargingStationRawData(
            is_being_used=kwh_supplied>0,
            kwh_supplied=kwh_supplied,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            sensor_uuid=self._sensor_uuid,
            sensor_name=self.sensor_name,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def _initialize_charging_power(self) -> float:
        """Initialize the charging power with a realistic random value."""
        charging_powers = [11, 22, 50, 100, 150, 350]
        probabilities = [0.3, 0.4, 0.15, 0.1, 0.04, 0.01]  # Adjusted probabilities for public use
        return random.choices(charging_powers, probabilities)[0]

    def _generate_energy_consumption(self) -> float:
        # Simulate the type of vehicle: car, bike, or hybrid
        vehicle_type = self._simulate_vehicle_type()
        # Simulate the battery level at the start of the charging session
        initial_battery_level = self._simulate_initial_battery_level()
        # Simulate the duration of the charging session in hours
        charging_duration = self._simulate_charging_duration(vehicle_type)

        # Calculate the energy supplied in kWh using the object's charging power
        kwh_supplied = self._charging_station_power * charging_duration * (1 - initial_battery_level / 100)
        
        # Ensure kwh_supplied is not negative and does not exceed the maximum capacity
        kwh_supplied = max(0, min(kwh_supplied, self._charging_station_power * charging_duration))
        
        return kwh_supplied

    def _simulate_vehicle_type(self) -> str:
        # Assuming probabilities for different vehicle types
        vehicle_types = ['car', 'bike', 'hybrid']
        probabilities = [0.7, 0.2, 0.1]
        return random.choices(vehicle_types, probabilities)[0]

    def _simulate_initial_battery_level(self) -> float:
        # Simulate the initial battery level between 0% and 80%
        return random.uniform(0, 80)

    def _simulate_charging_duration(self, vehicle_type: str) -> float:
        # Simulate the charging duration based on vehicle type
        if vehicle_type == 'car':
            return random.uniform(1, 4)  # 1 to 4 hours
        elif vehicle_type == 'bike':
            return random.uniform(0.5, 2)  # 0.5 to 2 hours
        elif vehicle_type == 'hybrid':
            return random.uniform(1, 3)  # 1 to 3 hours
        else:
            return 0

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
