import concurrent.futures as concurrent
import json
import logging as log
import signal
import threading

from kafka import KafkaProducer

from .models.config.env_config import EnvConfig
from .serialization.serializer_visitor import SerializerVisitor
from .simulators.simulator import Simulator


class Runner:

    def __init__(self, *, simulators: list[Simulator], config: EnvConfig) -> None:
        self.serializer = SerializerVisitor()
        self.simulators = simulators
        self.topic = config.kafka_topic
        self.max_workers = config.max_workers

        bootstrap_server = f'{config.kafka_host}:{config.kafka_port}'
        log.debug(f'Connecting to Kafka at {bootstrap_server}')

        try:

            self.producer = KafkaProducer(
                bootstrap_servers=[bootstrap_server],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                max_block_ms=config.max_block_ms,
                acks=1,
            )
        except Exception as e:
            log.exception('Error while creating KafkaProducer', e)
            raise

        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, _, __) -> None:  # noqa: ANN001
        log.info('Received shutdown signal, gracefully stopping...')
        for simulator in self.simulators:
            log.debug(f'Stopping {simulator.sensor_name}')
            simulator.stop()
        self.producer.close()
        log.debug('Producer closed, exiting.')

    def _callback(self, simulator: Simulator) -> None:
        simulator.start()
        thread = threading.current_thread().name
        log.info(f'Starting {simulator.sensor_name} in {thread}')

        for item in simulator.stream():
            serialized = item.accept(self.serializer)
            self.producer.send(self.topic, value=serialized)
            self.producer.flush()
            log.debug(f'Thread {thread}: sent {serialized}')

    def run(self) -> None:
        log.debug('Creating thread pool with %d workers', self.max_workers)
        with concurrent.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._callback, self.simulators)
