import logging as log
import os
import sys
import pytest
from uuid import UUID
from clickhouse_driver import Client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from simulator.src.producers.kafka_producer import KafkaProducerAdapter
from simulator.src.serializers.avro_record_serialization_strategy import \
    AvroRecordSerializationStrategy
from simulator.src.models.raw_data.air_quality_raw_data import AirQualityRawData

def test() -> None:

    producer = KafkaProducerAdapter(
        bootstrap_servers=["localhost:19092"],
        max_block_ms=1000,
        serializer=AvroRecordSerializationStrategy(),
        acks=1,
    )

    rawdata = AirQualityRawData(pm25= -8.635952949523926, pm10=10.820761680603027, no2=31.258577346801758, o3=37.09177780151367, so2=33.268592834472656, latitude=45.4034159, longitude=11.8756551, sensor_name="unipd-tito-livio", sensor_uuid=UUID('7fd1ec68-79f3-440a-854d-8e0d70e50430'), group_name="")

    producer.produce(rawdata)

    client = Client(host="localhost", port=9000, user="admin", password="admin")
    query = "SELECT * FROM sensors.air_quality"

    row = client.execute(query)

    try:
        assert UUID(str(row[0][0])) == UUID(str(rawdata._sensor_uuid))
        assert row[0][1] == rawdata._sensor_name
        assert row[0][2] == rawdata._group_name
        assert row[0][3] == rawdata._timestamp
        assert row[0][4] == rawdata._latitude
        assert row[0][5] == rawdata._longitude
        assert row[0][6] == rawdata._AirQualityRawData__pm25
        assert row[0][7] == rawdata._AirQualityRawData__pm10
        assert row[0][8] == rawdata._AirQualityRawData__no2
        assert row[0][9] == rawdata._AirQualityRawData__o3
        assert row[0][10] == rawdata._AirQualityRawData__so2
        log.info("Integration test completed successfully")
    except Exception as e:
        log.error(f"Integration test failed: {e}")


if __name__ == "__main__":
    # test()
    pytest.test([__file__])