import concurrent.futures as concurrent
import io
import logging as log
import threading
import time
from typing import Dict

from avro.io import DatumWriter, BinaryEncoder
from avro.schema import Schema
from kafka import KafkaProducer

from .models.config.env_config import EnvConfig
from .simulators.simulator import Simulator
from .utils.serializer_visitor import SerializerVisitor


class Runner:
    _SUBJECT = 'reading'

    def __init__(self, *, simulators: list[Simulator], config: EnvConfig,
                 schema_by_subject: Dict[str, tuple[int, Schema]]) -> None:
        self.serializer = SerializerVisitor()
        self.simulators = simulators
        self.topic = config.kafka_topic
        self.max_workers = config.max_workers
        schema_id, self.avro_schema = schema_by_subject[self._SUBJECT]

        self.schema_id_bytes = self._build_avro_bytes_identifier(schema_id)

        bootstrap_server = f'{config.kafka_host}:{config.kafka_port}'
        log.debug(f'Connecting to Kafka at {bootstrap_server}')

        try:
            self._producer = KafkaProducer(
                bootstrap_servers=[bootstrap_server],
                max_block_ms=config.max_block_ms,
                acks=1,
            )
            self._writer = DatumWriter(self.avro_schema)
            self._bytes_writer = io.BytesIO()
            self._encoder = BinaryEncoder(self._bytes_writer)
        except Exception as e:
            log.exception('Error while creating KafkaProducer', e)

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

                # clean the bytes writer
                self._bytes_writer.truncate(0)
                self._bytes_writer.seek(0)

                self._producer.send(
                    self.topic,
                    self._prepend_schema_id(raw_bytes),
                )
                self._producer.flush()
                log.info(f'Thread {thread}: sent {json_item} to Kafka')
            except Exception as e:
                log.exception('Error while sending message to Kafka', e)

    def run(self) -> None:
        try:
            log.debug('Creating thread pool with %d workers', self.max_workers)
            with concurrent.ThreadPoolExecutor(
                    max_workers=self.max_workers) as executor:
                executor.map(self._callback, self.simulators)
        except KeyboardInterrupt:
            log.info('Received shutdown signal, gracefully stopping...')
            for simulator in self.simulators:
                log.debug(f'Stopping {simulator.sensor_name}')
                simulator.stop()
        except Exception as e:
            log.exception('Error while running simulator', e)
        finally:
            time.sleep(2)
            self._producer.close()
            log.debug('Producer closed, exiting.')

    @staticmethod
    def _build_avro_bytes_identifier(schema_id: int) -> bytes:
        """
        Returns the schema id as bytes prepended with the magic byte,
        which is used by the Avro serializer to identify the schema.
        """
        magic_byte = bytearray([0])
        return magic_byte + schema_id.to_bytes(4, 'big')
        return bytearray()

    def _prepend_schema_id(self, raw_bytes: bytes) -> bytes:
        """
        Concatenates the schema id bytes with the raw bytes of the message.
        """
        return self.schema_id_bytes + raw_bytes
