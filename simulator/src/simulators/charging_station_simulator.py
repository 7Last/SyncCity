import random

from .simulator import Simulator
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.charging_station_raw_data import ChargingStationRawData
from ..producers.producer_strategy import ProducerStrategy


class ChargingStationSimulator(Simulator):
    def __init__(self, sensor_name: str, config: SensorConfig,
                 producer: ProducerStrategy) -> None:
        super().__init__(sensor_name, config, producer)
        self._charging_station_power = _initialize_charging_power()
        self._is_in_use = False
        self._remaining_charge_time = 0

    def data(self) -> ChargingStationRawData:
        kwh_supplied = self._generate_energy_consumption()
        data = ChargingStationRawData(
            is_being_used=self._is_in_use,
            kwh_supplied=kwh_supplied,
            remaining_charge_time=self._remaining_charge_time,
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            sensor_uuid=self._sensor_uuid,
            sensor_name=self.sensor_name,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        return data

    def _generate_energy_consumption(self) -> float:
        # Simulate the decision to start a new charging session
        if not self._is_in_use and random.random() < 0.3:
            self._is_in_use = True
            self._remaining_charge_time = _simulate_charging_duration()
            self._initial_battery_level = _simulate_initial_battery_level()
            self._elapsed_time = 0

        if self._is_in_use:
            # Calculate the energy supplied in kWh for this time step
            charging_power = self._charging_station_power
            time_step_hours = self._points_spacing.total_seconds() / 3600
            battery_percentage = self._initial_battery_level + (
                    self._elapsed_time / self._remaining_charge_time) * (
                                         100 - self._initial_battery_level)
            power_factor = _calculate_power_factor(battery_percentage)
            kwh_supplied = charging_power * time_step_hours * power_factor

            self._elapsed_time += time_step_hours
            if self._elapsed_time >= self._remaining_charge_time:
                self._is_in_use = False  # Charging session is complete

            return max(0, min(kwh_supplied, charging_power * time_step_hours, 100))

        return 0  # Charging station is not in use

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


def _initialize_charging_power() -> float:
    """Initialize the charging power with a realistic random value."""
    charging_powers = [11, 22, 50, 100, 150, 350]
    probabilities = [0.3, 0.4, 0.15, 0.1, 0.04,
                     0.01]  # Adjusted probabilities for public use
    return random.choices(charging_powers, probabilities)[0]


def _simulate_vehicle_type() -> str:
    # Assuming probabilities for different vehicle types
    vehicle_types = ['car', 'bike', 'hybrid']
    probabilities = [0.7, 0.2, 0.1]
    return random.choices(vehicle_types, probabilities)[0]


def _simulate_initial_battery_level() -> float:
    # Simulate the initial battery level between 0% and 80%
    return random.uniform(0, 80)


def _simulate_charging_duration() -> float:
    # Simulate the charging duration based on vehicle type
    vehicle_type = _simulate_vehicle_type()
    if vehicle_type == 'car':
        return random.uniform(1, 4)  # 1 to 4 hours
    if vehicle_type == 'bike':
        return random.uniform(0.5, 2)  # 0.5 to 2 hours
    if vehicle_type == 'hybrid':
        return random.uniform(1, 3)  # 1 to 3 hours
    return 0


def _calculate_power_factor(battery_percentage: float) -> float:
    """Calculate the power factor based on the battery percentage."""
    if battery_percentage < 80:
        return 1.0  # Full power up to 80%
    if battery_percentage < 90:
        return 0.5  # 50% power between 80% and 90%
    return 0.2  # 20% power above 90%
