import logging as log
import asyncio
from producers.temperature_producer import TemperatureProducer

log.basicConfig(level=log.DEBUG, format='[%(asctime)s] %(levelname)s: %(message)s')


async def main():
    temp_prod = TemperatureProducer(
        sensor_id="temperature-sensor-1",
        frequency=1000,
        limit=10,
    )
    # iterate over TemperatureRawData objects
    async for temp_data in temp_prod.produce():
        log.info(temp_data)


if __name__ == "__main__":
    asyncio.run(main())