package com.sevenlast.synccity;

import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.json.JsonDeserializationSchema;
import org.apache.flink.formats.json.JsonSerializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

public class Job {
    public static void main(String[] args) throws Exception {
        String broker = args[0];
        String topic = args[1];
//        String broker = "localhost:19092";
//        String topic = "sensors";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
        env.getConfig().setAutoWatermarkInterval(1000L);

        JsonDeserializationSchema<SensorData> jsonFormat = new JsonDeserializationSchema<>(SensorData.class);
        var source = KafkaSource.<SensorData>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(broker)
                .setTopics(topic)
                .setGroupId("consumer_test")
                .setValueOnlyDeserializer(jsonFormat)
                .build();

        var watermark = WatermarkStrategy.<SensorData>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                .withTimestampAssigner((event, timestamp) -> event.datetime.toInstant(ZoneOffset.UTC).toEpochMilli());

        var aggregated = env.fromSource(source, watermark, "Kafka Source")
                .keyBy(data -> data.name)
                .window(TumblingEventTimeWindows.of(Time.minutes(10)))
                .aggregate(new Average())
                .map(AggregatedRecord::toString);

        var sink = KafkaSink.<String>builder()
                .setBootstrapServers(broker)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic("aggregated")
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .build()
                )
                .build();

        aggregated.sinkTo(sink);
        env.execute("Kafka Consumer Example");
    }

    public static class SensorData {
        private String name;
        private Integer temperature;
        private LocalDateTime datetime;

        public SensorData() {
        }

        public SensorData(String name, Integer temperature, LocalDateTime datetime) {
            this.name = name;
            this.temperature = temperature;
            this.datetime = datetime;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public Integer getTemperature() {
            return temperature;
        }

        public void setTemperature(Integer temperature) {
            this.temperature = temperature;
        }

        public LocalDateTime getDatetime() {
            return datetime;
        }

        public void setDatetime(LocalDateTime datetime) {
            this.datetime = datetime;
        }

        @Override
        public String toString() {
            return "SensorData{" +
                    "sensor='" + name + '\'' +
                    ", value=" + temperature +
                    ", timestamp=" + datetime +
                    '}';
        }
    }

    public static class AverageAccumulator {
        String sensorName;
        LocalDateTime timestamp;
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

    public static class Average implements AggregateFunction<SensorData, AverageAccumulator, AggregatedRecord> {
        public AverageAccumulator createAccumulator() {
            return new AverageAccumulator();
        }

        public AverageAccumulator merge(AverageAccumulator a, AverageAccumulator b) {
            a.count += b.count;
            a.sum += b.sum;
            return a;
        }

        public AverageAccumulator add(SensorData record, AverageAccumulator acc) {
            if (acc.sensorName == null) {
                acc.sensorName = record.name;
            }

            // Assuming the record has a field "timestamp" with the event timestamp
            if (acc.timestamp == null) {
                var timestamp = record.datetime;
                acc.timestamp = timestamp.withSecond(0).withNano(0);
            }

            var value = record.temperature;
            acc.sum += value;
            acc.count++;
            return acc;
        }

        public AggregatedRecord getResult(AverageAccumulator acc) {
            double avg = acc.count == 0 ? 0 : acc.sum / acc.count;
            DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
            String formattedDateTime = acc.timestamp.format(formatter);
            return new AggregatedRecord(acc.sensorName, formattedDateTime, avg);
        }
    }
}