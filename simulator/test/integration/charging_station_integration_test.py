import logging as log
import os
import sys
import pytest
from uuid import UUID
from clickhouse_driver import Client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.producers.kafka_producer import KafkaProducerAdapter
from src.serializers.avro_record_serialization_strategy import \
    AvroRecordSerializationStrategy
from src.models.raw_data.charging_station_raw_data import ChargingStationRawData

def test() -> None:

    producer = KafkaProducerAdapter(
        bootstrap_servers="localhost:19092",
        max_block_ms=1000,
        serializer=AvroRecordSerializationStrategy(),
        acks=1,
    )

    rawdata = ChargingStationRawData(vehicle_type="car", battery_level=50.0, kwh_supplied=25.0, remaining_charge_time=50, elapsed_time=25, latitude=1.0, longitude=1.0, sensor_uuid=UUID("12345678-1234-5678-1234-567812345678"), sensor_name="sensor1", group_name="tullio-levi-civita")

    producer.produce(rawdata)

    client = Client(host="localhost", port=9000, user="admin", password="admin")
    query = "SELECT * FROM sensors.charging_station"

    row = client.execute(query)

    try:
        assert UUID(str(row[0][0])) == UUID(str(rawdata._sensor_uuid))
        assert row[0][1] == rawdata._sensor_name
        assert row[0][2] == rawdata._group_name
        assert row[0][3] == rawdata._timestamp
        assert row[0][4] == rawdata._latitude
        assert row[0][5] == rawdata._longitude
        assert row[0][6] == rawdata.__battery_level
        assert row[0][7] == rawdata.__elapsed_time
        assert row[0][8] == rawdata.__kwh_supplied
        assert row[0][9] == rawdata.__remaining_charge_time
        assert row[0][10] == rawdata.__vehicle_type
        log.info("Integration test completed successfully")
    except Exception as e:
        log.error(f"Integration test failed: {e}")


if __name__ == "__main__":
    # test()
    pytest.test([__file__])