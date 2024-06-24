from simulator.src.serializers.strategy.record_serialization_strategy import \
    RecordSerializationStrategy
from .producer_strategy import ProducerStrategy
from ..models.raw_data.raw_data import RawData


class StdOutProducer(ProducerStrategy):
    def __init__(self, serializer: RecordSerializationStrategy) -> None:
        super().__init__(serializer)

    def produce(self, data: RawData) -> bool:
        serialized = self._serializer.serialize_value(data)
        print(serialized)
        return True

    def close(self) -> None:
        pass
