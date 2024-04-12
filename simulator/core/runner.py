import json
import signal
import logging as log
import threading
import concurrent.futures

from kafka import KafkaProducer

from .simulators.simulator import Simulator


class Runner:

    def __init__(self, simulators: list[Simulator], bootstrap_server: str,
                 max_block_ms: int, topic: str) -> None:
        self.simulators = simulators
        self.topic = topic
        self.bootstrap_server = bootstrap_server
        self.max_block_ms = max_block_ms

        self.producer = KafkaProducer(
            bootstrap_servers=[self.bootstrap_server],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks=1,
        )

        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, _, __) -> None:  # noqa: ANN001
        log.info('Received shutdown signal, gracefully stopping...')
        for simulator in self.simulators:
            simulator.stop()
        self.producer.close()

    def _callback(self, simulator: Simulator) -> None:
        simulator.start()
        log.info(
            f'Starting {simulator.sensor_id} '
            f'in thread {threading.current_thread().name}',
        )

        for item in simulator.stream():
            log.debug('Sending on thread', threading.current_thread().name,
                      item.serialize())
            self.producer.send(self.topic, value=item.serialize())
            self.producer.flush()
            log.debug('Sent')

    def run(self) -> None:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self._callback, self.simulators)
