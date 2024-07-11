from abc import abstractmethod, ABC

from ..models.raw_data.raw_data import RawData


class SerializationStrategy(ABC):
    @abstractmethod
    def serialize(self, raw_data: RawData):
        pass
