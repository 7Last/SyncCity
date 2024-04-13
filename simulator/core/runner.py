import json
import signal
import logging as log
import threading
import concurrent.futures as concurrent

from kafka import KafkaProducer

from .simulators.simulator import Simulator
from .models.config.kafka_config import KafkaConfig
from .serialization.serializer_visitor import SerializerVisitor


class Runner:

    def __init__(self, simulators: list[Simulator], kafka_config: KafkaConfig,
                 max_workers: int) -> None:
        self.topic = kafka_config.topic
        self.simulators = simulators
        self.max_workers = max_workers
        self.serializer = SerializerVisitor()

        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[kafka_config.bootstrap_server],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                max_block_ms=kafka_config.max_block_ms,
                acks=1,
            )
        except Exception as e:
            log.fatal('Error connecting to Kafka', e)
            raise

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
            serialized = item.accept(self.serializer)
            self.producer.send(self.topic, value=serialized)
            self.producer.flush()
            log.debug(f'Thread {threading.current_thread().name}: sent {serialized}')

    def run(self) -> None:
        with concurrent.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._callback, self.simulators)
