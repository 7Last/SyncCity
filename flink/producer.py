import random
import time
from datetime import datetime, timedelta, UTC
from pathlib import Path
from typing import Dict

from confluent_avro import AvroValueSerde, SchemaRegistry
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:19092')

temperature = {
    "sensor_name": 'via-pralungo',
    "sensor_uuid": '00000000-0000-0000-0000-000000000000',
    "group_name": 'temp-hum-group',
    "latitude": 45.4018782,
    "longitude": 11.7769644,
}

temperature2 = {
    "sensor_name": 'via-martiri',
    "sensor_uuid": '00000000-0000-0000-0000-000000000000',
    "group_name": 'temp-hum-group',
    "latitude": 45.4318782,
    "longitude": 11.7769644,
}

humidity = {
    "sensor_name": 'humidity',
    "sensor_uuid": '00000000-0000-0000-0000-000000000000',
    "group_name": 'temp-hum-group',
    "latitude": 45.4218782,
    "longitude": 11.7969644,
}

humidity2 = {
    "sensor_name": 'humidity',
    "sensor_uuid": '00000000-0000-0000-0000-000000000000',
    "group_name": 'temp-hum-group',
    "latitude": 45.4318782,
    "longitude": 11.7969644,
}

begin_date = datetime(2024, 1, 1, 1, 5, 0)

registry_client = SchemaRegistry(
    url='http://localhost:18081',
    headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
)


def serialize(json_item: Dict, value_subject: str, topic: str) -> bytes:
    avro_serde = AvroValueSerde(registry_client, topic)
    path = Path(__file__).parent.joinpath('../redpanda/schemas')
    value_schema = (path / f"{value_subject}.avsc").read_text()
    return avro_serde.serialize(json_item, value_schema)


i = 0
while True:
    item_date = begin_date + timedelta(minutes=i)
    item_date_ms = int(item_date.timestamp() * 1000)

    if i % 2 == 0:
        item = {
            **temperature,
            "value": random.randint(25, 40),
            "timestamp": item_date.astimezone(UTC).isoformat(),
        }
        serialized = serialize(item, 'temperature-value', 'temperature')
        producer.send('temperature', value=serialized, timestamp_ms=item_date_ms)
        print(f"Sent: {item}")

        item = {
            **temperature2,
            "value": random.randint(25, 40),
            "timestamp": item_date.astimezone(UTC).isoformat(),
        }
        serialized = serialize(item, 'temperature-value', 'temperature')
        producer.send('temperature', value=serialized, timestamp_ms=item_date_ms)
        print(f"Sent: {item}")

    else:
        item = {
            **humidity,
            "value": random.random(),
            "timestamp": item_date.astimezone(UTC).isoformat(),
        }
        serialized = serialize(item, 'humidity-value', 'humidity')
        producer.send('humidity', value=serialized, timestamp_ms=item_date_ms)
        print(f"Sent: {item}")
        item = {
            **humidity2,
            "value": random.random(),
            "timestamp": item_date.astimezone(UTC).isoformat(),
        }

        serialized = serialize(item, 'humidity-value', 'humidity')
        producer.send('humidity', value=serialized, timestamp_ms=item_date_ms)
        print(f"Sent: {item}")

    time.sleep(1)
    i += 1
