package com.sevenlast.synccity;

import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.json.JsonDeserializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;
import java.time.ZoneOffset;

public class Job {
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

        var broker = "http://redpanda:9092";
        var topic = "sensors";
        var groupId = "flink-group";
        var sourceName = "sensors-source";
        var sinkTopic = "sensors-aggregated";
        var jobName = "sensors-aggregator";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
//        long watermarkInterval = Long.parseLong(configLoader.getProperty("flink.watermark-interval"));
        long watermarkInterval = 1000;
        env.getConfig().setAutoWatermarkInterval(watermarkInterval);

        JsonDeserializationSchema<SensorData> jsonFormat = new JsonDeserializationSchema<>(SensorData.class);
        var source = KafkaSource.<SensorData>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(broker)
                .setTopics(topic)
                .setGroupId(groupId)
                .setValueOnlyDeserializer(jsonFormat)
                .build();

        var watermark = WatermarkStrategy.<SensorData>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                .withTimestampAssigner((event, timestamp) -> event.getDatetime().toInstant(ZoneOffset.UTC).toEpochMilli());

        var aggregated = env.fromSource(source, watermark, sourceName)
                .keyBy(SensorData::getName)
                .window(TumblingEventTimeWindows.of(Time.minutes(10)))
                .apply(new AverageWindowFunction())
                .map(Tuple3::toString);

        var sink = KafkaSink.<String>builder()
                .setBootstrapServers(broker)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(sinkTopic)
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .build()
                )
                .build();

        aggregated.sinkTo(sink);
        env.execute(jobName);
    }

}