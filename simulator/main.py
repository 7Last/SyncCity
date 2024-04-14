import logging as log
import os

import toml

from src.models.config.config import Config
from src.runner import Runner

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.toml')


def main() -> None:
    config = Config(toml.load(config_path))

    log.basicConfig(
        level=config.general.log_level,
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    log.debug('Loaded config.toml')

    runner = Runner(
        env=os.environ.get('SENSORS_SIMULATOR_ENV'),
        simulators=list(config.simulators_generator()),
        kafka_config=config.kafka,
        max_workers=config.general.max_workers,
    )
    log.debug('Starting runner')
    runner.run()


if __name__ == "__main__":
    main()
