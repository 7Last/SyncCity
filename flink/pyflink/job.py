import os

from pyflink.common import WatermarkStrategy
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaSource
from pyflink.datastream.formats.avro import AvroRowDeserializationSchema

env = StreamExecutionEnvironment.get_execution_environment()
current_path = os.path.dirname(os.path.realpath(__file__))
env.add_jars(
    f"file://{current_path}/flink-sql-connector-kafka-3.1.0-1.18.jar",
    f"file:///{current_path}/flink-sql-avro-1.19.0.jar",
)

properties = {
    'bootstrap.servers': 'localhost:19092',
    'sasl.mechanism': 'PLAIN',
    'security.protocol': 'PLAINTEXT',
    'group.id': 'observability',
    'sasl.jaas.config': "org.apache.kafka.common.security.plain.PlainLoginModule required",
}

earliest = False
offset = KafkaOffsetsInitializer.earliest() if earliest else KafkaOffsetsInitializer.latest()

schema = """
{
  "type": "record",
  "name": "Temperature",
  "fields": [
    {
      "name": "sensor_uuid",
      "type": "string"
    },
    {
      "name": "sensor_name",
      "type": "string"
    },
    {
      "name": "latitude",
      "type": "double"
    },
    {
      "name": "longitude",
      "type": "double"
    },
    {
      "name": "timestamp",
      "type": "string"
    },
    {
      "name": "value",
      "type": "float"
    }
  ]
}
"""

# Create a Kafka Source
kafka_source = KafkaSource.builder() \
    .set_topics("temperature") \
    .set_properties(properties) \
    .set_starting_offsets(offset) \
    .set_value_only_deserializer(AvroRowDeserializationSchema(avro_schema_string=schema)) \
    .build()

data_stream = env.from_source(kafka_source,
                              WatermarkStrategy.no_watermarks(),
                              "Temperature Sensor Data")

print("start reading data from kafka")

data_stream.map(lambda x: print(x))

# Print in a more readable format
# Execute the Flink pipeline
env.execute("Kafka Source Example")
