import logging as log

import kafka

from .producer_strategy import ProducerStrategy
from ..models.raw_data.raw_data import RawData
from ..serializers.dict_raw_data_adapter import DictRawDataAdapter
from ..serializers.serialization_strategy import SerializationStrategy


class KafkaProducerAdapter(ProducerStrategy):

    def __init__(self, *, serialization_strategy: SerializationStrategy,
                 bootstrap_servers: list[str], max_block_ms: int,
                 acks: int) -> None:
        super().__init__(serialization_strategy)
        self.__adaptee = kafka.KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            max_block_ms=max_block_ms,
            acks=acks,
        )

    def produce(self, data: RawData) -> bool:
        try:
            key = str(data.sensor_uuid()).encode('utf-8')
            value = self._serialization_strategy.serialize(DictRawDataAdapter(data))
            log.info(f'Producing data to topic {data.topic}: {data}')
            self.__adaptee.send(data.topic, key=key, value=value)
            self.__adaptee.flush()
            return True
        except Exception as e:
            log.error(f'Failed to produce data to topic {data.topic}: {e}')
            return False

    def close(self) -> None:
        self.__adaptee.close(timeout=2)
