import logging as log
import os

import toml

from src.kafka_producer import KafkaProducer
from src.models.config.env_config import EnvConfig
from src.models.config.simulator_factory import simulators_generator
from src.runner import Runner
from src.json_serializer import JSONSerializer

sensors_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sensors.toml')


def main() -> None:
    env_config = EnvConfig()
    log.basicConfig(
        level=env_config.log_level,
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    log.debug(f'Loaded configuration from env {env_config}')

    sensors_config = toml.load(sensors_path).get('sensors')
    log.debug(f'Loaded sensors configuration {sensors_config}')

    # producer = StdOutProducer(serializer=JsonSerializer())  # noqa: ERA001

    producer = KafkaProducer(
        bootstrap_servers=[env_config.bootstrap_server],
        max_block_ms=env_config.max_block_ms,
        serializer=JSONSerializer(),
        acks=1,
    )

    runner = Runner(
        simulators=list(simulators_generator(sensors_config)),
        producer=producer,
        max_workers=env_config.max_workers,
    )

    log.debug('Starting runner')
    runner.run()


if __name__ == "__main__":
    main()
