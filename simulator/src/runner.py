import concurrent.futures as concurrent
import io
import logging as log
import signal
import threading
import time

import avro.schema
from avro.io import DatumWriter
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

        path = './schema_registry/schemas/reading.avsc'
        schema = avro.schema.parse(open(path).read())

        bootstrap_server = f'{config.kafka_host}:{config.kafka_port}'
        log.debug(f'Connecting to Kafka at {bootstrap_server}')

        try:
            self._producer = KafkaProducer(
                bootstrap_servers=[bootstrap_server],
                max_block_ms=config.max_block_ms,
                acks=1,
            )
            self._writer = DatumWriter(schema)
            self._bytes_writer = io.BytesIO()
            self._encoder = avro.io.BinaryEncoder(self._bytes_writer)
        except Exception as e:
            log.exception('Error while creating KafkaProducer', e)

        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)

    def _graceful_shutdown(self, _, __) -> None:  # noqa: ANN001
        log.info('Received shutdown signal, gracefully stopping...')
        for simulator in self.simulators:
            log.debug(f'Stopping {simulator.sensor_name}')
            simulator.stop()

        time.sleep(1.5)  # wait for the simulators to stop
        self._producer.close()
        log.debug('Producer closed, exiting.')

    def _callback(self, simulator: Simulator) -> None:
        simulator.start()
        thread = threading.current_thread().name
        log.info(f'Starting {simulator.sensor_name} in {thread}')

        for item in simulator.stream():
            json_item = item.accept(self.serializer)
            try:
                # convert the item to bytes
                self._writer.write(json_item, self._encoder)
                raw_bytes = self._bytes_writer.getvalue()

                schema_id = 1
                message_with_schema_id = bytearray([0]) + schema_id.to_bytes(4,
                                                                             'big') + raw_bytes

                self._producer.send(self.topic, message_with_schema_id)
                log.debug(f'Thread {thread}: sent message to Kafka')
            except Exception as e:
                log.exception('Error while sending message to Kafka', e)

    def run(self) -> None:
        log.debug('Creating thread pool with %d workers', self.max_workers)
        with concurrent.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self._callback, self.simulators)
