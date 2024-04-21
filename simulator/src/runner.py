import concurrent.futures as concurrent
import logging as log
import threading
import time
from typing import Dict

from avro.schema import Schema
from kafka import KafkaProducer

from .models.config.env_config import EnvConfig
from .simulators.simulator import Simulator
from .utils.avro_converter import AvroConverter
from .utils.serializer_visitor import SerializerVisitor


class Runner:
    _SUBJECT = 'temperature-value'

    def __init__(self, *, simulators: list[Simulator], config: EnvConfig,
                 schema_by_subject: Dict[str, tuple[int, Schema]]) -> None:
        self.serializer = SerializerVisitor()
        schema_id, schema = schema_by_subject[self._SUBJECT]

        self.simulators = simulators
        self.max_workers = config.max_workers

        bootstrap_server = f'{config.kafka_host}:{config.kafka_port}'
        log.debug(f'Connecting to Kafka at {bootstrap_server}')

        try:
            self._producer = KafkaProducer(
                bootstrap_servers=[bootstrap_server],
                max_block_ms=config.max_block_ms,
                acks=1,
            )

            self._avro_converter = AvroConverter(schema_id, schema)
        except Exception as e:
            log.exception('Error while creating KafkaProducer', e)

    def _callback(self, simulator: Simulator) -> None:
        simulator.start()
        thread = threading.current_thread().name
        log.info(f'Starting {simulator.sensor_name} in {thread}')

        for item in simulator.stream():
            json_item = item.accept(self.serializer)
            try:
                item_type = json_item['type']
                # remove type from the message
                del json_item['type']
                value = self._avro_converter.encode(json_item)
                self._producer.send(item_type, value=value)
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
