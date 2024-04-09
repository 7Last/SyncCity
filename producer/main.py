from datetime import datetime, timedelta
import asyncio
import logging as log

from core.runner import Runner
from core.producers.temperature_producer import TemperatureProducer

log.basicConfig(level=log.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


def main() -> None:
    runner = Runner(producers=[
        TemperatureProducer(
            sensor_id='temperature-sensor-1',
            points_spacing=timedelta(hours=1),
            generation_delay=timedelta(seconds=1),
            begin_date=datetime(2023, 1, 1, 0, 0, 0),
            latitude=40.416775,
            longitude=-3.703790,
            limit=24,
        ),
    ])

    log.debug('Starting runner')
    asyncio.run(runner.run())


if __name__ == "__main__":
    main()
