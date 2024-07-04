package com.sevenlast.synccity;

import com.sevenlast.synccity.functions.AverageWindowFunction;
import com.sevenlast.synccity.functions.HeatIndexJoinFunction;
import com.sevenlast.synccity.models.HumTempRawData;
import com.sevenlast.synccity.models.results.AverageResult;
import com.sevenlast.synccity.models.results.HeatIndexResult;
import com.sevenlast.synccity.serialization.RecordSerializationSchema;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import lombok.AllArgsConstructor;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.connector.source.Source;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;

import java.time.Duration;
import java.time.ZonedDateTime;

import static org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroSerializationSchema.forSpecific;

@AllArgsConstructor
public class HeatIndexJob {
    private static final String TEMPERATURE_TOPIC = "temperature";
    private static final String HUMIDITY_TOPIC = "humidity";
    private static final Duration WINDOW_SIZE = Duration.ofHours(1);
    private static final String HEAT_INDEX_TOPIC = "heat_index";
    private static final String GROUP_ID = "heat-index-job";

    private Source<GenericRecord, ?, ?> temperatureKafkaSource;
    private Source<GenericRecord, ?, ?> humidityKafkaSource;
    private Sink<HeatIndexResult> heatIndexSink;

    public static void main(String[] args) throws Exception {
        var bootstrapServers = System.getenv("BOOTSTRAP_SERVERS");
        var schemaRegistryUrl = System.getenv("SCHEMA_REGISTRY_URL");

        if (bootstrapServers == null || schemaRegistryUrl == null) {
            throw new IllegalArgumentException("BOOTSTRAP_SERVERS and SCHEMA_REGISTRY_URL must be set");
        }

        var client = new CachedSchemaRegistryClient(schemaRegistryUrl, 20);
        // temperature and humidity have the same schema, using temperature as a reference
        var temperatureMetadata = client.getLatestSchemaMetadata(TEMPERATURE_TOPIC + "-value");
        var schemaParser = new Schema.Parser();

        var deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(
                schemaParser.parse(temperatureMetadata.getSchema()), schemaRegistryUrl);

        var temperatureKafkaSource = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(bootstrapServers)
                .setTopics(TEMPERATURE_TOPIC)
                .setGroupId(GROUP_ID)
                .setValueOnlyDeserializer(deserializer)
                .build();

        var humidityKafkaSource = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(bootstrapServers)
                .setTopics(HUMIDITY_TOPIC)
                .setGroupId(GROUP_ID)
                .setValueOnlyDeserializer(deserializer)
                .build();

        var metadata = client.getLatestSchemaMetadata(HEAT_INDEX_TOPIC + "-value");
        var heatIndexSchema = schemaParser.parse(metadata.getSchema());

        var sink = KafkaSink.<HeatIndexResult>builder()
                .setBootstrapServers(bootstrapServers)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(HEAT_INDEX_TOPIC)
                        .setValueSerializationSchema(new RecordSerializationSchema<HeatIndexResult>(
                                HEAT_INDEX_TOPIC,
                                heatIndexSchema,
                                schemaRegistryUrl
                        ))
                        .build()
                )
                .build();

        new HeatIndexJob(temperatureKafkaSource, humidityKafkaSource, sink).execute();
    }

    public void execute() throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
        env.getConfig().setAutoWatermarkInterval(1000);

        var watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                .withTimestampAssigner((event, timestamp) -> {
                    var eventTimestamp = event.get("timestamp").toString();
                    return ZonedDateTime.parse(eventTimestamp).toInstant().toEpochMilli();
                });

        var avgTemperatureStream = env.fromSource(temperatureKafkaSource, watermark, "temperature-source")
                .map(HumTempRawData::fromGenericRecord)
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy(HumTempRawData::getGroupName)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new AverageWindowFunction());

        var avgHumidityStream = env.fromSource(humidityKafkaSource, watermark, "humidity-source")
                .map(HumTempRawData::fromGenericRecord)
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy(HumTempRawData::getGroupName)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new AverageWindowFunction());

        DataStream<HeatIndexResult> heatIndexStream = avgTemperatureStream.join(avgHumidityStream)
                .where(AverageResult::getGroupName)
                .equalTo(AverageResult::getGroupName)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new HeatIndexJoinFunction());

        heatIndexStream.sinkTo(heatIndexSink);
        env.execute("Heat Index Job");
    }
}