import os
from dotenv import load_dotenv


class EnvConfig:
    def __init__(self) -> None:
        load_dotenv()

        self.kafka_host = self._get_or_throw('KAFKA_HOST')
        self.kafka_port = self._get_or_throw('KAFKA_PORT')
        self.kafka_topic = self._get_or_throw('KAFKA_TOPIC')
        self.log_level = self._get_or_throw('LOG_LEVEL')
        self.max_workers = int(os.environ.get('MAX_WORKERS', 1))
        self.max_block_ms = int(os.environ.get('MAX_BLOCK_MS', 1000))

    @staticmethod
    def _get_or_throw(key: str) -> str:
        val = os.getenv(key)
        if val is None:
            raise ValueError(f'{key} is not set')
        return val

    def __str__(self) -> str:
        return f'{self.__dict__}'
