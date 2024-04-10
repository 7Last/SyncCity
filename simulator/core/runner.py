import signal
import logging as log

from aiostream import stream

from .simulators.simulator import Simulator


class Runner:

    def __init__(self, simulators: list[Simulator]) -> None:
        self.simulators = simulators
        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, _, __) -> None:  # noqa: ANN001
        log.info('Received shutdown signal, gracefully stopping...')
        for simulator in self.simulators:
            simulator.stop()

    async def run(self) -> None:
        for simulator in self.simulators:
            simulator.start()

        combine = stream.merge(*(simulator.stream() for simulator in self.simulators))

        async with combine.stream() as streamer:
            async for item in streamer:
                print(item.sensor_id, item)
