import random
from datetime import timedelta

from .simulator import Simulator
from ..models.config.sensor_config import SensorConfig
from ..models.raw_data.charging_station_raw_data import ChargingStationRawData
from ..producers.producer_strategy import ProducerStrategy


class ChargingStationSimulator(Simulator):
    VEHICLE_TYPES = {
        "bike": {"probability": 0.1, "max_battery": 2, "max_power": 1},
        "car": {"probability": 0.5, "max_battery": 60, "max_power": 22},
        "hybrid": {"probability": 0.1, "max_battery": 20, "max_power": 11},
        "suv": {"probability": 0.2, "max_battery": 100, "max_power": 50},
        "truck": {"probability": 0.1, "max_battery": 300, "max_power": 150},
    }

    CHARGING_STATION_TYPES = {
        "slow": {"probability": 0.5, "power": 7.4},  # 7.4 kW (slow charging, AC)
        "fast": {"probability": 0.3, "power": 22.0}, # 22 kW (fast charging, AC)
        "rapid": {"probability": 0.15, "power": 50.0}, # 50 kW (rapid charging, DC)
        "ultra_rapid": {"probability": 0.05, "power": 150.0}, # 150 kW (ultra-rapid charging, DC)
    }

    def __init__(self, sensor_name: str, config: SensorConfig, producer: ProducerStrategy) -> None:
        super().__init__(sensor_name, config, producer)
        self._charging_station_power = self._initialize_charging_power()
        self._vehicle_type = ''
        self._battery_level = 0
        self._remaining_charge_time = timedelta(seconds=0)
        self._elapsed_time = timedelta(seconds=0)
        self._initialize_new_session()
        self._idle_time = timedelta(seconds=0)  # Initialize idle time
        self._usage_frequency_factor = random.randint(1, 10)  # Randomize usage frequency factor

    def data(self) -> ChargingStationRawData:
        if self._idle_time > timedelta(seconds=0):
            self._idle_time -= self._points_spacing
            return ChargingStationRawData(
                vehicle_type='',
                battery_level=0.0,
                kwh_supplied=0.0,
                remaining_charge_time=0,
                elapsed_time=0,
                latitude=self._latitude,
                longitude=self._longitude,
                timestamp=self._timestamp,
                sensor_uuid=self._sensor_uuid,
                sensor_name=self.sensor_name,
                group_name=self._group_name,
            )

        kwh_supplied = max(0, min(self._charging_station_power, self._generate_energy_consumption()))
        data = ChargingStationRawData(
            vehicle_type=self._vehicle_type,
            battery_level=self._battery_level,
            kwh_supplied=kwh_supplied,
            remaining_charge_time=int(self._remaining_charge_time.total_seconds()),
            elapsed_time=int(self._elapsed_time.total_seconds()),
            latitude=self._latitude,
            longitude=self._longitude,
            timestamp=self._timestamp,
            sensor_uuid=self._sensor_uuid,
            sensor_name=self.sensor_name,
            group_name=self._group_name,
        )

        self._timestamp += self._points_spacing
        self._elapsed_time += self._points_spacing

        # Update remaining charge time and battery level
        if self._remaining_charge_time > timedelta(seconds=0):
            self._update_charge_status(kwh_supplied)
        else:
            if random.random() < 0.2:  # 20% chance to stay connected after charge completion
                self._remaining_charge_time = timedelta(seconds=0)
            else:
                self._initialize_new_session()

        return data

    def _initialize_charging_power(self) -> float:
        rand = random.random()
        cumulative_probability = 0.0
        for station_type, info in self.CHARGING_STATION_TYPES.items():
            cumulative_probability += info["probability"]
            if rand <= cumulative_probability:
                return info["power"]
        return 22.0  # Default to "fast" if something goes wrong

    def _initialize_new_session(self):
        self._vehicle_type = self._choose_vehicle_type()
        vehicle_info = self.VEHICLE_TYPES[self._vehicle_type]
        self._battery_level = self._initialize_battery_level(vehicle_info["max_battery"])
        self._remaining_charge_time = self._calculate_remaining_charge_time(vehicle_info["max_battery"])
        self._elapsed_time = timedelta(seconds=0)
        self._idle_time = timedelta(seconds=0)

    def _choose_vehicle_type(self) -> str:
        rand = random.random()
        cumulative_probability = 0.0
        for vehicle, info in self.VEHICLE_TYPES.items():
            cumulative_probability += info["probability"]
            if rand <= cumulative_probability:
                return vehicle
        return "car"  # Default to "car" if something goes wrong

    def _initialize_battery_level(self, max_battery: float) -> float:
        # Initialize battery level with a decreasing probability as the charge level increases
        return max_battery * (1 - random.random()**2)

    def _calculate_remaining_charge_time(self, max_battery: float) -> timedelta:
        charge_needed = max_battery - self._battery_level
        charge_time_hours = charge_needed / self._charging_station_power
        return timedelta(hours=charge_time_hours)

    def _generate_energy_consumption(self) -> float:
        # Simulate realistic energy consumption based on battery level percentage
        if self._remaining_charge_time.total_seconds() <= 0:
            return 0.0

        max_battery = self.VEHICLE_TYPES[self._vehicle_type]["max_battery"]
        battery_percentage = self._battery_level / max_battery

        # Power curve based on battery percentage
        if battery_percentage < 0.2:
            # Higher power at low charge levels (simulate peak power)
            charging_power = self._charging_station_power * (0.8 + 0.4 * random.random())
        elif battery_percentage < 0.8:
            # Nominal power at mid charge levels
            charging_power = self._charging_station_power * (0.7 + 0.3 * random.random())
        else:
            # Reduced power at high charge levels (simulate trickle charging)
            charging_power = self._charging_station_power * (0.3 + 0.4 * random.random())

        return charging_power

    def _update_charge_status(self, kwh_supplied: float):
        max_battery = self.VEHICLE_TYPES[self._vehicle_type]["max_battery"]
        charge_added = kwh_supplied * (self._points_spacing.total_seconds() / 3600.0)  # Convert kW to kWh based on time spacing

        self._battery_level += charge_added
        if self._battery_level > max_battery:
            self._battery_level = max_battery

        charge_needed = max_battery - self._battery_level
        charge_time_hours = charge_needed / self._charging_station_power
        self._remaining_charge_time = timedelta(hours=charge_time_hours)

        if self._battery_level >= max_battery:
            self._remaining_charge_time = timedelta(seconds=0)
            # Chance to remain connected after charge completion
            if random.random() < 0.2:  # 20% chance
                self._idle_time = timedelta(minutes=random.randint(10, 60))
            else:
                # Initialize a new idle period with a decreasing probability over time
                self._idle_time = timedelta(hours=random.randint(1, 30 * self._usage_frequency_factor) * random.random())
