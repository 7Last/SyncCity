import os
import logging as log

from core.runner import Runner
from core.models.config.config import Config
import toml

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.toml')


def main() -> None:
    config = Config(toml.load(config_path))

    log.basicConfig(
        level=config.general.log_level,
        format='%(asctime)s %(levelname)s: %(message)s',
    )
    log.debug('Loaded config.toml')

    runner = Runner(
        simulators=list(config.simulators_generator()),
        kafka_config=config.kafka,
        max_workers=config.general.max_workers,
    )
    log.debug('Starting runner')
    runner.run()


if __name__ == "__main__":
    main()
