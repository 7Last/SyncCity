package com.sevenlast.synccity;

import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.SerializableTimestampAssigner;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public class Job {
    public static void main(String[] args) throws Exception {
        var broker = "localhost:19092";
        var topic = "temperature";
        var schemaRegistryUrl = "http://localhost:18081";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);

        var client = new CachedSchemaRegistryClient(schemaRegistryUrl, 20);
        var metadata = client.getLatestSchemaMetadata(topic + "-value");
        var schema = new Schema.Parser().parse(metadata.getSchema());

        var deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(schema, schemaRegistryUrl);

        var source = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(broker)
                .setTopics(topic)
                .setGroupId("consumer_test")
                .setValueOnlyDeserializer(deserializer)
                .build();

        var watermarkStrategy = WatermarkStrategy
                .<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                .withTimestampAssigner((SerializableTimestampAssigner<GenericRecord>) (element, internalTimestamp) -> {
                    var recordTimestamp = element.get("timestamp").toString();
                    var zonedDateTime = ZonedDateTime.parse(recordTimestamp);
                    return zonedDateTime.toInstant().toEpochMilli();
                });

        var sourceStream = env.fromSource(source, watermarkStrategy, "Temperature source");
        var metadataOut = client.getLatestSchemaMetadata("temperature-out-value");
        var schemaOut = new Schema.Parser().parse(metadataOut.getSchema());

//        var serializer = ConfluentRegistryAvroSerializationSchema.forGeneric(
//                "temperature-out-value",
//                schemaOut,
//                schemaRegistryUrl
//        );

        var aggregatedStream = sourceStream
                .keyBy(record -> record.get("sensor_name"))
                .window(TumblingEventTimeWindows.of(Time.seconds(10)))
//                .trigger(ContinuousProcessingTimeTrigger.of(Time.minutes(1)))
//                .evictor(TimeEvictor.of(Time.minutes(1)))
                .aggregate(new Average(schemaOut));

//        var sink = KafkaSink.<GenericRecord>builder()
//                .setBootstrapServers(broker)
//                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
//                                .setTopic("temperature-out")
////                        .setTopicSelector((element) -> {<your-topic-selection-logic>})
//                                .setValueSerializationSchema(serializer)
//                                .build()
//                )
//                .setDeliveryGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
//                .build();

//        aggregatedStream.sinkTo(sink);
        aggregatedStream.print();

        env.execute("Kafka Consumer Example");
    }

    public static class AverageAccumulator {
        String sensorName;
        ZonedDateTime timestamp;
        Double count;
        Double sum;

        public AverageAccumulator() {
            this.count = 0.0;
            this.sum = 0.0;
        }
    }

    public static class AggregatedRecord {
        String sensorName;
        String timestamp;
        Double average;

        public AggregatedRecord(String sensorName, String timestamp, Double average) {
            this.sensorName = sensorName;
            this.timestamp = timestamp;
            this.average = average;
        }

        @Override
        public String toString() {
            return "AggregatedRecord{" +
                    "sensorName='" + sensorName + '\'' +
                    ", timestamp='" + timestamp + '\'' +
                    ", average=" + average +
                    '}';
        }
    }

    public static class Average implements AggregateFunction<GenericRecord, AverageAccumulator, AggregatedRecord> {
        final Schema schema;

        public Average(Schema schema) {
            this.schema = schema;
        }

        public AverageAccumulator createAccumulator() {
            return new AverageAccumulator();
        }

        public AverageAccumulator merge(AverageAccumulator a, AverageAccumulator b) {
            a.count += b.count;
            a.sum += b.sum;
            return a;
        }

        public AverageAccumulator add(GenericRecord record, AverageAccumulator acc) {
            if (acc.sensorName == null) {
                acc.sensorName = record.get("sensor_name").toString();
            }

            // Assuming the record has a field "timestamp" with the event timestamp
            var recordTimestamp = record.get("timestamp").toString();
            var zonedDateTime = ZonedDateTime.parse(recordTimestamp);
            var windowStart = zonedDateTime.withSecond(0).withNano(0);
            acc.timestamp = windowStart;
            var value = (Float) record.get("value");
            acc.sum += value;
            acc.count++;
            return acc;
        }

        public AggregatedRecord getResult(AverageAccumulator acc) {
            double avg = acc.count == 0 ? 0 : acc.sum / acc.count;
            DateTimeFormatter formatter = DateTimeFormatter.ISO_ZONED_DATE_TIME;
            String formattedDateTime = acc.timestamp.format(formatter);
            return new AggregatedRecord(acc.sensorName, formattedDateTime, avg);
        }
    }
}