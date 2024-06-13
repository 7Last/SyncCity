import os

from dotenv import load_dotenv


class EnvConfig:
    def __init__(self) -> None:
        load_dotenv()

        self.kafka_host = self._get_or_throw('KAFKA_HOST')
        self.kafka_port = self._get_or_throw('KAFKA_PORT')
        self.log_level = self._get_or_throw('LOG_LEVEL')
        self.max_block_ms = int(self._get_or_none('KAFKA_MAX_BLOCK_MS') or 1000)

    @staticmethod
    def _get_or_throw(key: str) -> str:
        val = os.getenv(key)
        if val is None or val == '':
            raise ValueError(f'{key} is not set')
        return val

    @staticmethod
    def _get_or_none(key: str) -> str | None:
        val = os.getenv(key)
        if val is None or val == '':
            return None
        return val

    @property
    def bootstrap_server(self) -> str:
        return f'{self.kafka_host}:{self.kafka_port}'

    def __str__(self) -> str:
        return f'{self.__dict__}'
