# from datetime import datetime
# from random import Random
# from typing import Type

# from src.simulator.sensor_simulator_strategy import SensorSimulatorStrategy
# import math
# from src.utils.sensor_types import SensorTypes
# from src.utils.json_message_maker import json_message_maker
# from src.utils.coordinates import Coordinates


# class HumiditySensorSensorSimulator(SensorSimulatorStrategy):
#     # Imposta lo spostamento di fase per allineare il picco di umidità con le ore del mattino
#     __phase: float = 0.2
#     __amplitude: float
#     __percen: float

#     def __init__(self, sensor_name: str, random_obj: Random, datetime_obj: Type[datetime], coordinates: Coordinates):
#         super().__init__(sensor_name, random_obj, datetime_obj, coordinates)
#         self.__amplitude = self.__calculate_ampiezza()

#     def __calculate_ampiezza(self) -> float:

#         current_month = self._datetime_obj.now().month
#         if 3 <= current_month <= 5:  # Primavera: da marzo a maggio
#             return 0.45
#         elif 6 <= current_month <= 8:  # Estate: da giugno a agosto
#             return 0.3
#         elif 9 <= current_month <= 11:  # Autunno: da settembre a novembre
#             return 0.65
#         else:  # Inverno: da dicembre a febbraio
#             return 0.85

#     def __calcola_percentuale(self) -> float:
#         now = self._datetime_obj.now()
#         hours = (int(now.timestamp()) % 86400) / 3600
#         relative_humidity = (
#             math.sin(2 * math.pi * (hours - self.__phase) / 24) * self.__amplitude + 1) / 2
#         relative_humidity += self._random_obj.uniform(-0.01, 0.01)
#         relative_humidity = max(0.0, min(1.0, relative_humidity))
#         oscillazione = self._random_obj.uniform(-0.1, 0.1)
#         percentile = relative_humidity * (100 - 35) + 35 + oscillazione
#         return percentile

#     def simulate(self) -> str:

#         timestamp = self._datetime_obj.now()
#         self.__percen = self.__calcola_percentuale()

#         reading = {
#             "type": "%",
#             "value": round(self.__percen, 2)
#         }

#         dato = json_message_maker(SensorTypes.HUMIDITY, str(timestamp), [
#                                   reading], self._sensor_name, self._coordinates)

#         return dato
