from .producer_strategy import ProducerStrategy
from ..models.raw_data.raw_data import RawData
from ..serializers.dict_raw_data_adapter import DictRawDataAdapter
from ..serializers.serialization_strategy import SerializationStrategy


class StdOutProducer(ProducerStrategy):
    def __init__(self, serialization_strategy: SerializationStrategy) -> None:
        super().__init__(serialization_strategy)

    def produce(self, data: RawData) -> bool:
        serialized = self._serialization_strategy.serialize(DictRawDataAdapter(data))
        print(serialized)
        return True

    def close(self) -> None:
        pass
