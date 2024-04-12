from typing import Dict


class KafkaConfig:
    def __init__(self, kafka_config: Dict[str, any]) -> None:
        port: int = kafka_config.get('port')
        host: str = kafka_config.get('host')

        self.topic: str = kafka_config.get('topic')
        self.max_block_ms: int = kafka_config.get('max_block_ms')
        self.bootstrap_server = f'{host}:{port}'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'
