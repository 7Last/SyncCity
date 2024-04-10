import os
import asyncio
import logging as log

from core.runner import Runner
from core.config.schema import ConfigSchema
import toml

log.basicConfig(level=log.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.toml')


def main() -> None:
    schema = ConfigSchema(toml.load(config_path))
    log.debug('Loaded config.toml')
    runner = Runner(simulators=list(schema.simulators_generator()))
    log.debug('Starting runner')
    asyncio.run(runner.run())


if __name__ == "__main__":
    main()
