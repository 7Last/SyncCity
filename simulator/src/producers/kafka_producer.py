import logging as log

import kafka

from .producer_strategy import ProducerStrategy
from ..models.raw_data.raw_data import RawData
from ..serializers.serializer_strategy import SerializerStrategy


class KafkaProducer(ProducerStrategy):

    def __init__(self, *, serializer: SerializerStrategy, bootstrap_servers: list[str],
                 max_block_ms: int, acks: int) -> None:
        super().__init__(serializer)
        self._producer = kafka.KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            max_block_ms=max_block_ms,
            acks=acks,
        )

    def produce(self, data: RawData) -> None:
        serialized = self._serializer.serialize(data)
        log.info(f'Producing data to topic {data.topic}: {data}')
        self._producer.send(data.topic, value=serialized)
        self._producer.flush()

    def close(self) -> None:
        self._producer.close()
