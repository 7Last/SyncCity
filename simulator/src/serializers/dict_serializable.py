from abc import ABC, abstractmethod


class DictSerializable(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def topic(self) -> str:
        pass
