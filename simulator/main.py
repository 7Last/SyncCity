import logging as log
import os

import toml

from src.producers.kafka_producer import KafkaProducerAdapter
from src.serializers.avro_serialization_strategy import \
    AvroSerializationStrategy
from src.models.config.env_config import EnvConfig
from src.simulators.simulator_executor import SimulatorExecutor

sensors_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sensors.toml')


def main() -> None:
    env_config = EnvConfig()
    log.basicConfig(
        level=env_config.log_level(),
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    log.debug(f'Loaded configuration from env {env_config}')

    sensors_config = toml.load(sensors_path).get('sensors')
    log.debug(f'Loaded sensors configuration {sensors_config}')

    # producer = StdOutProducer(
    #     serialization_strategy=JsonSerializationStrategy()
    # )  # noqa: ERA001

    producer = KafkaProducerAdapter(
        bootstrap_servers=[env_config.bootstrap_server],
        max_block_ms=env_config.max_block_ms(),
        serialization_strategy=AvroSerializationStrategy(),
        acks=1,
    )

    runner = SimulatorExecutor(sensors_config, producer)
    log.debug('Starting runner')
    runner.run()


if __name__ == "__main__":
    main()
