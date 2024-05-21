import json
import logging as log

import kafka

from .json_serializer import JSONSerializer
from .models.raw_data.raw_data import RawData


class KafkaProducer():

    def __init__(self, *, serializer: JSONSerializer, bootstrap_servers: list[str],
                 max_block_ms: int, acks: int) -> None:
        self.serializer = serializer
        self._producer = kafka.KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            max_block_ms=max_block_ms,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks=acks,
        )

    def produce(self, data: RawData) -> None:
        serialized = data.accept(self.serializer)
        log.info(f'Producing data to topic {data.topic}: {data}')
        self._producer.send(data.topic, serialized)
        self._producer.flush()

    def close(self) -> None:
        self._producer.close(timeout=2)
