import concurrent.futures as concurrent
import json
import logging as log
import signal
import threading

from kafka import KafkaProducer

from .models.config.kafka_config import KafkaConfig
from .serialization.serializer_visitor import SerializerVisitor
from .simulators.simulator import Simulator


class Runner:

    def __init__(self, *, env: str, simulators: list[Simulator],
                 kafka_config: KafkaConfig, max_workers: int) -> None:
        self.topic = kafka_config.topic
        self.simulators = simulators
        self.max_workers = max_workers
        self.serializer = SerializerVisitor()
        log.debug(f'Running in {env} environment')

        try:
            bootstrap_servers = kafka_config[env]
            log.debug(f'Connecting to Kafka at {bootstrap_servers}')

            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                max_block_ms=kafka_config.max_block_ms,
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
            log.debug(f'Stopping {simulator.sensor_id}')
            simulator.stop()
        self.producer.close()
        log.debug('Producer closed, exiting.')

    def _callback(self, simulator: Simulator) -> None:
        simulator.start()
        log.info(
            f'Starting {simulator.sensor_id} in {threading.current_thread().name}',
        )

        for item in simulator.stream():
            serialized = item.accept(self.serializer)
            self.producer.send(self.topic, value=serialized)
            self.producer.flush()
            log.debug(f'Thread {threading.current_thread().name}: sent {serialized}')

    def run(self) -> None:
        with concurrent.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._callback, self.simulators)
