from abc import ABC, abstractmethod

from ..models.raw_data.raw_data import RawData
from ..serializers.serializer_visitor import SerializerVisitor


class SerializerStrategy(ABC):
    def __init__(self) -> None:
        self._visitor = SerializerVisitor()

    @abstractmethod
    def serialize(self, data: RawData) -> any:
        pass
