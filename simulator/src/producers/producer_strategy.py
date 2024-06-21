from abc import ABC, abstractmethod

from ..models.raw_data.raw_data import RawData
from simulator.src.serializers.strategy.record_serialization_strategy import RecordSerializationStrategy


class ProducerStrategy(ABC):
    def __init__(self, serializer: RecordSerializationStrategy) -> None:
        self._serializer = serializer

    @abstractmethod
    def produce(self, data: RawData) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
