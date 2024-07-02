from abc import ABC, abstractmethod

from ..serializers.record_serialization_template import RecordSerializationTemplate
from ..models.raw_data.raw_data import RawData


class ProducerStrategy(ABC):
    def __init__(self, serializer: RecordSerializationTemplate) -> None:
        self._serializer = serializer

    @abstractmethod
    def produce(self, data: RawData) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
