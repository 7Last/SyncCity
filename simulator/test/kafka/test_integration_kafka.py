import os
import zoneinfo
from datetime import datetime
import pytest
import json
from simulator.src.models.raw_data.temperature_raw_data import TemperatureRawData
from simulator.src.models.config.sensor_config import SensorConfig
from simulator.src.producers.kafka_producer import KafkaProducerAdapter
from simulator.src.serializers.record_serialization_template import RecordSerializationTemplate
import uuid

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
topic = "test"


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
def kafka_write(kafka_producer):
    def write(data):
        kafka_producer.produce(TemperatureRawData(
            sensor_name=data.get("sensor_name"),
            sensor_uuid=data.get("sensor_uuid"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            timestamp=datetime.fromisoformat(data.get("timestamp")),
            value=data.get("value"),
        ))
    return write


def test_kafka_integration_base(kafka_producer):
    kafka_producer.produce(TemperatureRawData(
        sensor_name="test_sensor_name",
        sensor_uuid=uuid.UUID("00000000-0000-0000-0000-000000000000"),
        latitude=0.0,
        longitude=0.0,
        timestamp=datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0,
                           tzinfo=zoneinfo.ZoneInfo("Europe/Rome")),
        value=0.0,
    ))


def test_kafka_integration(kafka_write):
    data = {
        "sensor_name": "test_base",
        "sensor_uuid": "00000000-0000-0000-0000-000000000000",
        "latitude": 0,
        "longitude": 0,
        "timestamp": "2024-01-01T00:00:00",
        "value": 0,
    }
    try:
        kafka_write(data)
    except Exception as e:
        assert False, f"Failed to write to Kafka: {e}"
    assert True


def test_kafka_integration_multiple(kafka_write):
    for i in range(50):
        data = {
            "sensor_name": f"test_{i}",
            "sensor_uuid": uuid.uuid4(),
            "latitude": 0,
            "longitude": 0,
            "timestamp": "2024-01-01T00:00:00",
            "value": i,
        }
        try:
            kafka_write(data)
        except Exception as e:
            assert False, f"Failed to write to Kafka: {e}"
    assert True
