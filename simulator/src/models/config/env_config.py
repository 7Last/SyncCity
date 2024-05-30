import os

from dotenv import load_dotenv


class EnvConfig:
    def __init__(self) -> None:
        load_dotenv()

        self.kafka_host = self._get_or_throw('KAFKA_HOST')
        self.kafka_port = self._get_or_throw('KAFKA_PORT')
        self.log_level = self._get_or_throw('LOG_LEVEL')
        max_block_ms = os.environ.get('MAX_BLOCK_MS')
        self.max_block_ms = 1000 if max_block_ms == '' or max_block_ms is None else int(max_block_ms)

    @staticmethod
    def _get_or_throw(key: str) -> str:
        val = os.getenv(key)
        if val is None or val == '':
            raise ValueError(f'{key} is not set')
        return val

    @property
    def bootstrap_server(self) -> str:
        return f'{self.kafka_host}:{self.kafka_port}'

    def __str__(self) -> str:
        return f'{self.__dict__}'
