from datetime import datetime, timedelta
import asyncio
import logging as log

from core.runner import Runner
from core.simulators.traffic_simulator import TrafficSimulator
from core.simulators.temperature_simulator import TemperatureSimulator

log.basicConfig(level=log.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


def main() -> None:
    runner = Runner(simulators=[
        TemperatureSimulator(
            sensor_id='temperature-sensor-1',
            points_spacing=timedelta(hours=1),
            generation_delay=timedelta(seconds=1),
            begin_date=datetime(2023, 1, 1, 0, 0, 0),
            latitude=40.416775,
            longitude=-3.703790,
            limit=24,
        ),
        TrafficSimulator(
            sensor_id='traffic-simulator-1',
            points_spacing=timedelta(minutes=10),
            generation_delay=timedelta(seconds=2),
            limit=10,
            latitude=43.416775,
            longitude=4.703790,
        ),
    ])

    log.debug('Starting runner')
    asyncio.run(runner.run())


if __name__ == "__main__":
    main()
