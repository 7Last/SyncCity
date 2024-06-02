package com.sevenlast.synccity;

import com.twitter.chill.java.UnmodifiableCollectionSerializer;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.generic.GenericRecordBuilder;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.SerializableTimestampAssigner;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.connector.base.DeliveryGuarantee;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroSerializationSchema;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.triggers.ContinuousProcessingTimeTrigger;
import org.apache.flink.streaming.api.windowing.triggers.EventTimeTrigger;
import org.apache.flink.streaming.api.windowing.triggers.ProcessingTimeTrigger;
import org.apache.flink.streaming.util.serialization.KeyedSerializationSchema;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public class Job {
    public static void main(String[] args) throws Exception {
        var broker = "localhost:19092";
        var topic = "temperature";
        var schemaRegistryUrl = "http://localhost:18081";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        Class<?> unmodColl = Class.forName("java.util.Collections$UnmodifiableCollection");
        env.getConfig().addDefaultKryoSerializer(unmodColl, UnmodifiableCollectionSerializer.class);
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

        var serializer = ConfluentRegistryAvroSerializationSchema.forGeneric(
                "temperature-out-value",
                schemaOut,
                schemaRegistryUrl
        );

        var aggregatedStream = sourceStream
                .keyBy(record -> record.get("sensor_name"))
                .window(TumblingEventTimeWindows.of(Time.minutes(1)))
                .trigger(EventTimeTrigger.create())
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

            if (acc.timestamp == null) {
                // Assuming the record has a field "timestamp" with the event timestamp
                var recordTimestamp = record.get("timestamp").toString();
                var zonedDateTime = ZonedDateTime.parse(recordTimestamp);
                var windowStart = zonedDateTime.withSecond(0).withNano(0);
                acc.timestamp = windowStart;
            }
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