from abc import ABC, abstractmethod

from ..models.raw_data.raw_data import RawData
from ..serializers.dict_raw_data_adapter import DictSerializable
from ..serializers.serialization_strategy import SerializationStrategy


class ProducerStrategy(ABC):
    def __init__(self, serialization_strategy: SerializationStrategy) -> None:
        self._serialization_strategy = serialization_strategy

    @abstractmethod
    def produce(self, data: RawData) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
