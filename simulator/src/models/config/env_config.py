import os

from dotenv import load_dotenv


class EnvConfig:
    def __init__(self) -> None:
        load_dotenv()

        self.__kafka_host = self.__get_or_throw('KAFKA_HOST')
        self.__kafka_port = self.__get_or_throw('KAFKA_PORT')
        self.__log_level = self.__get_or_throw('LOG_LEVEL')
        self.__max_block_ms = int(self.__get_or_none('KAFKA_MAX_BLOCK_MS') or 1000)

    def log_level(self) -> str:
        return self.__log_level

    def max_block_ms(self) -> int:
        return self.__max_block_ms

    @staticmethod
    def __get_or_throw(key: str) -> str:
        val = os.getenv(key)
        if val is None or val == '':
            raise ValueError(f'{key} is not set')
        return val

    @staticmethod
    def __get_or_none(key: str) -> str | None:
        val = os.getenv(key)
        if val is None or val == '':
            return None
        return val

    @property
    def bootstrap_server(self) -> str:
        return f'{self.__kafka_host}:{self.__kafka_port}'

    def __str__(self) -> str:
        return f'{self.__dict__}'
