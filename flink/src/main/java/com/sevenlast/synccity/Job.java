package com.sevenlast.synccity;

import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.formats.avro.registry.confluent.ConfluentSchemaRegistryCoder;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.kafka.clients.consumer.ConsumerConfig;

import java.util.Properties;
import java.util.UUID;

public class Job {
    public static void main(String[] args) throws Exception {
        var kafkaBroker = "localhost:19092";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();

        var kafkaProps = new Properties();
        kafkaProps.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBroker);
        kafkaProps.setProperty(ConsumerConfig.GROUP_ID_CONFIG, "consumer_test");

        var topic = "temperature";

        // create schema from string
        var schema = Schema.parse("{\n" +
                "    \"type\": \"record\",\n" +
                "    \"name\": \"Temperature\",\n" +
                "    \"fields\": [\n" +
                "        {\n" +
                "            \"name\": \"sensor_uuid\",\n" +
                "            \"type\": \"string\"\n" +
                "        },\n" +
                "        {\n" +
                "            \"name\": \"sensor_name\",\n" +
                "            \"type\": \"string\"\n" +
                "        },\n" +
                "        {\n" +
                "            \"name\": \"latitude\",\n" +
                "            \"type\": \"double\"\n" +
                "        },\n" +
                "        {\n" +
                "            \"name\": \"longitude\",\n" +
                "            \"type\": \"double\"\n" +
                "        },\n" +
                "        {\n" +
                "            \"name\": \"timestamp\",\n" +
                "            \"type\": \"string\"\n" +
                "        },\n" +
                "        {\n" +
                "            \"name\": \"value\",\n" +
                "            \"type\": \"float\"\n" +
                "        }\n" +
                "    ]\n" +
                "}");

        var deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(schema, "http://localhost:18081");

        var kafkaConsumer = KafkaSource.<GenericRecord>builder()
                .setBootstrapServers(kafkaBroker)
                .setTopics(topic)
                .setGroupId("consumer_test")
                .setProperties(kafkaProps)
                .setValueOnlyDeserializer(deserializer)
                .build();

        var kafkaStream = env.fromSource(kafkaConsumer, WatermarkStrategy.noWatermarks(), "Kafka Source");
        kafkaStream.print();

        env.execute("Kafka Consumer Example");
    }
}