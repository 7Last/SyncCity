from abc import ABC, abstractmethod

from ...models.raw_data.raw_data import RawData
from ...serializers.visitor.converter_visitor import ConverterVisitor


class RecordSerializationStrategy(ABC):
    def __init__(self, visitor: ConverterVisitor) -> None:
        self._visitor = visitor

    @abstractmethod
    def serialize_key(self, data: RawData) -> any:
        pass

    @abstractmethod
    def serialize_value(self, data: RawData) -> any:
        pass
