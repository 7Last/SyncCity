import random
from datetime import datetime
from typing import Iterable

from math import pi, sin

from .simulator import Simulator
from ..models.raw_data.river_level_raw_data import RiverLevelRowData


class RiverLevelSimulator(Simulator):
    def data(self) -> Iterable[RiverLevelRowData]:
        while self._limit != 0 and self._running:
            yield RiverLevelRowData(
                value=_sinusoidal_value(self._timestamp, self._latitude),
                sensor_uuid=self._sensor_uuid,
                sensor_name=self.sensor_name,
                latitude=self._latitude,
                longitude=self._longitude,
                timestamp=self._timestamp,
                group_name=self._group_name,
            )

            if self._limit is not None:
                self._limit -= 1
            self._timestamp += self._points_spacing
            self._event.wait(self._generation_delay.total_seconds())

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'



def _sinusoidal_value(timestamp: datetime, latitude: float) -> float:
    # Costanti che possono essere modificate per adattare il modello alla realtà
    DAILY_AMPLITUDE = 0.5   # Variazione giornaliera dei livelli del fiume
    SEASONAL_AMPLITUDE = 1.5 # Variazione stagionale dei livelli del fiume
    BASE_LEVEL = 5.0        # Livello base del fiume
    LATITUDE_FACTOR = (sin(latitude / 90.0 * pi / 2)) ** 2  # Fattore non lineare per la latitudine

    # Calcolo dell'offset stagionale (giorno dell'anno)
    day_of_year = timestamp.timetuple().tm_yday
    seasonal_variation = SEASONAL_AMPLITUDE * sin(2 * pi * day_of_year / 365.25)

    # Calcolo dell'offset giornaliero (secondo del giorno)
    seconds_in_day = timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second
    daily_variation = DAILY_AMPLITUDE * sin(2 * pi * seconds_in_day / 86400)

    # Introduzione di una variabilità casuale controllata
    RANDOM_VARIABILITY = 0.1  # Questo valore può essere modificato per aumentare o diminuire la variabilità
    random_factor = random.gauss(1, RANDOM_VARIABILITY)

    # Calcolo del valore finale con variabilità casuale
    value = ((BASE_LEVEL + seasonal_variation + daily_variation * LATITUDE_FACTOR) * random_factor) * 500

    return value