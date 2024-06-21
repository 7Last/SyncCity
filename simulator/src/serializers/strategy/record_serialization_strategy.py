from abc import ABC, abstractmethod

from simulator.src.models.raw_data.raw_data import RawData
from simulator.src.serializers.visitor.serialization_visitor import SerializationVisitor


class RecordSerializationStrategy(ABC):
    def __init__(self, visitor: SerializationVisitor) -> None:
        self._visitor = visitor

    @abstractmethod
    def serialize_key(self, data: RawData) -> any:
        pass

    @abstractmethod
    def serialize_value(self, data: RawData) -> any:
        pass
