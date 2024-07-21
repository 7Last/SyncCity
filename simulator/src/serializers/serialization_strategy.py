from abc import abstractmethod, ABC

from .dict_raw_data_adapter import DictSerializable


class SerializationStrategy(ABC):
    @abstractmethod
    def serialize(self, data: DictSerializable) -> bytes:
        pass
