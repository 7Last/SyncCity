package com.sevenlast.synccity;

import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;

public class HeatIndexJob {
    public static void main(String[] args) throws Exception {

//        var appEnv = System.getProperty("app.env", "local");
//        var configLoader = new ConfigLoader(appEnv);
//
//        var broker = configLoader.getProperty("kafka.bootstrap.servers");
//        var topic = configLoader.getProperty("flink.source.topic");
//        var groupId = configLoader.getProperty("kafka.group.id");
//        var sourceName = configLoader.getProperty("flink.source.name");
//        var sinkTopic = configLoader.getProperty("flink.sink.topic");
//        var jobName = configLoader.getProperty("flink.job.name");

//        var broker = "http://redpanda:9092";
//        var schemaRegistryUrl = "http://redpanda:8081";
        var broker = "http://localhost:19092";
        var schemaRegistryUrl = "http://localhost:18081";
        var sourceTopic = "temperature";
        var groupId = "flink-group";
        var sourceName = "sensors-source";
        var sinkTopic = "sensors-aggregated";
        var jobName = "sensors-aggregator";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
//        long watermarkInterval = Long.parseLong(configLoader.getProperty("flink.watermark-interval"));
        long watermarkInterval = 1000;
        env.getConfig().setAutoWatermarkInterval(watermarkInterval);

        var client = new CachedSchemaRegistryClient(schemaRegistryUrl, 20);
        var metadata = client.getLatestSchemaMetadata(sourceTopic + "-value");
        var schemaParser = new Schema.Parser();

        var deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(
                schemaParser.parse(metadata.getSchema()), schemaRegistryUrl);

        var watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                .withTimestampAssigner((event, timestamp) -> {
                    var eventTimestamp = event.get("timestamp").toString();
                    return ZonedDateTime.parse(eventTimestamp).toInstant().toEpochMilli();
                });

        var temperatureKafkaSource = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(broker)
                .setTopics(sourceTopic)
                .setGroupId(groupId)
                .setValueOnlyDeserializer(deserializer)
                .build();

        var temperatureStream = env.fromSource(temperatureKafkaSource, watermark, sourceName);

        temperatureStream.print();

//        var sink = KafkaSink.<String>builder()
//                .setBootstrapServers(broker)
//                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
//                        .setTopic(sinkTopic)
//                        .setValueSerializationSchema(new SimpleStringSchema())
//                        .build()
//                )
//                .build();
//
//        aggregated.sinkTo(sink);
        env.execute(jobName);
    }

}