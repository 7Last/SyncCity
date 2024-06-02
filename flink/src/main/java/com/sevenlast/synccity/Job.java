package com.sevenlast.synccity;

import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.kafka.clients.consumer.ConsumerConfig;

import java.util.Properties;

public class Job {
    public static void main(String[] args) throws Exception {
        var kafkaBroker = "localhost:19092";
        var topic = "temperature";
        var schemaRegistryUrl = "http://localhost:18081";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();

        var props = new Properties();
        props.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBroker);
        props.setProperty(ConsumerConfig.GROUP_ID_CONFIG, "consumer_test");

        var client = new CachedSchemaRegistryClient(schemaRegistryUrl, 20);
        var metadata = client.getLatestSchemaMetadata(topic + "-value");
        var schemaParser = new Schema.Parser();

        var deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(
                schemaParser.parse(metadata.getSchema()), schemaRegistryUrl);

        var kafkaConsumer = KafkaSource.<GenericRecord>builder()
                .setBootstrapServers(kafkaBroker)
                .setTopics(topic)
                .setGroupId("consumer_test")
                .setProperties(props)
                .setValueOnlyDeserializer(deserializer)
                .build();

        var kafkaStream = env.fromSource(kafkaConsumer, WatermarkStrategy.noWatermarks(), "Kafka Source");
        kafkaStream.print();

        env.execute("Kafka Consumer Example");
    }
}