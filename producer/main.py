import logging as log
import asyncio
from core.runner import Runner
from core.producers.temperature_producer import TemperatureProducer

log.basicConfig(level=log.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


def main():
    temperature_sensor_1 = TemperatureProducer(
        sensor_id='temperature-sensor-1',
        frequency=1000,
        limit=10
    )

    temperature_sensor_2 = TemperatureProducer(
        sensor_id='temperature-sensor-2',
        frequency=2000,
        limit=10
    )

    temperature_sensor_3 = TemperatureProducer(
        sensor_id='temperature-sensor-3',
        frequency=3000,
        limit=10
    )

    runner = Runner(producers=[
        temperature_sensor_1,
        temperature_sensor_2,
        temperature_sensor_3
    ])

    log.info('Starting runner')
    asyncio.run(runner.run())


if __name__ == "__main__":
    main()