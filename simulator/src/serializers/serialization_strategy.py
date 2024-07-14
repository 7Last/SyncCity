from abc import abstractmethod, ABC

from .dict_raw_data_adapter import DictSerializable
from ..models.raw_data.raw_data import RawData


class SerializationStrategy(ABC):
    @abstractmethod
    def serialize(self, data: DictSerializable) -> bytes:
        pass
