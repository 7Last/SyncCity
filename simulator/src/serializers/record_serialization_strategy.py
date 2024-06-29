from abc import ABC, abstractmethod

from ..models.raw_data.raw_data import RawData


class RecordSerializationStrategy(ABC):
    @abstractmethod
    def serialize_key(self, raw_data: RawData) -> bytes:
        pass

    @abstractmethod
    def serialize_value(self, raw_data: RawData) -> bytes:
        pass
