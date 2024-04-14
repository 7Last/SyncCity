from typing import Dict


class KafkaConfig:
    def __init__(self, kafka_config: Dict[str, any]) -> None:
        self.topic: str = kafka_config.get('topic')
        self.max_block_ms: int = kafka_config.get('max_block_ms')

        self._bootstrap_servers = {
            env: str(BootstrapServerConfig(server))
            for env, server in kafka_config.get('bootstrap_servers').items()
        }

    def default_bootstrap_server(self) -> str:
        return self._bootstrap_servers.get('local')

    def __getitem__(self, key: str) -> str:
        if key is None:
            return self.default_bootstrap_server()
        return self._bootstrap_servers.get(key, self.default_bootstrap_server())

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.__dict__}'


class BootstrapServerConfig:
    def __init__(self, bootstrap_server: Dict[str, any]) -> None:
        self.host = bootstrap_server.get('host')
        self.port = bootstrap_server.get('port')

    def __str__(self) -> str:
        return f'{self.host}:{self.port}'
