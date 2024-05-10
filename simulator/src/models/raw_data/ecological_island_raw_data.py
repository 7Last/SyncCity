import random
from datetime import datetime
from typing import Dict
from uuid import UUID

from .raw_data import RawData


class EcologicalIslandRawData(RawData):
    __riempimento_max = 95 # in percentuale
    __riempimento_min = 5
    __velocita_riempimento = 5

    def __init__(self, *, riempimento_iniziale=30, latitude: float, longitude: float,
                 sensor_uuid: UUID, sensor_name: str,
                 timestamp: datetime = datetime.now()) -> None:
        # parametro riempimento_iniziale: percentuale di riempimento dell'isola ecologica

        super().__init__(latitude=latitude, longitude=longitude,
                         sensor_uuid=sensor_uuid, sensor_name=sensor_name,
                         timestamp=timestamp)
        self.riempimento_iniziale = riempimento_iniziale  
    
    def _generazione_dati(self):
        self._misurazione += random.uniform(-EcologicalIslandRawData.__velocita_riempimento, EcologicalIslandRawData.__velocita_riempimento)
        self._misurazione = max(EcologicalIslandRawData.__riempimento_min,
                              min(EcologicalIslandRawData.__riempimento_max, self._misurazione))

    def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
        return visitor.serialize_ecological_island_raw_data(self)                          
        
    @property
    def topic(self) -> str:
        return "ecological_island"