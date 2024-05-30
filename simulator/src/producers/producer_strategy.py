from abc import ABC, abstractmethod

from ..models.raw_data.raw_data import RawData
from ..serializers.serializer_strategy import SerializerStrategy


class ProducerStrategy(ABC):
    def __init__(self, serializer: SerializerStrategy) -> None:
        self._serializer = serializer

    @abstractmethod
    def produce(self, data: RawData) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
