import logging as log

import kafka

from .producer_strategy import ProducerStrategy
from ..models.raw_data.raw_data import RawData
from ..serializers.strategy.record_serialization_strategy import \
    RecordSerializationStrategy


class KafkaProducerAdapter(ProducerStrategy):

    def __init__(self, *, serializer: RecordSerializationStrategy,
                 bootstrap_servers: list[str],
                 max_block_ms: int, acks: int) -> None:
        super().__init__(serializer)
        self._adaptee = kafka.KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            max_block_ms=max_block_ms,
            acks=acks,
        )

    def produce(self, data: RawData) -> bool:
        try:
            serialized = self._serializer.serialize_value(data)
            log.info(f'Producing data to topic {data.topic}: {data}')
            self._adaptee.send(data.topic, value=serialized)
            self._adaptee.flush()
            return True
        except Exception as e:
            log.error(f'Failed to produce data to topic {data.topic}: {e}')
            return False

    def close(self) -> None:
        self._adaptee.close(timeout=2)
