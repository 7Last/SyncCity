import signal
from aiostream import stream
from .producers.producer import Producer
import logging as log


class Runner:

    def __init__(self, producers: list[Producer]):
        self.producers = producers
        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, _, __):
        log.info('Received shutdown signal, gracefully stopping...')
        for producer in self.producers:
            producer.stop()

    async def run(self):
        for producer in self.producers:
            producer.start()

        combine = stream.merge(*(producer.stream() for producer in self.producers))

        async with combine.stream() as streamer:
            async for item in streamer:
                print(item.sensor_id, item)
