from abc import ABC, abstractmethod

from ..models.raw_data.raw_data import RawData

Record = (bytes | None, bytes)


class RecordSerializationTemplate(ABC):

    def serialize(self, raw_data: RawData) -> Record:
        return self.serialize_key(raw_data), self.serialize_value(raw_data)

    def serialize_key(self, raw_data: RawData) -> bytes:  # default implementation
        return str(raw_data.sensor_uuid()).encode('utf-8')

    @abstractmethod
    def serialize_value(self, raw_data: RawData) -> bytes:
        pass
