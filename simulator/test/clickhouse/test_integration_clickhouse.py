import os
import zoneinfo
from datetime import datetime
import pytest
import clickhouse_connect
from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.producers.kafka_producer import KafkaProducerAdapter
from simulator.src.serializers.record_serialization_template import RecordSerializationTemplate

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
topic = "test"

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")


@pytest.fixture
def kafka_producer():
    producer = KafkaProducerAdapter(
        serializer=RecordSerializationTemplate(),
        bootstrap_servers=[f"{KAFKA_HOST}:{KAFKA_PORT}"],
        max_block_ms=1000,
        acks=1,
    )
    yield producer
    producer.close()


@pytest.fixture
def clickhouse_connection():
    connection = clickhouse_connect.get_client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, database="sensors")
    yield connection
    connection.close()