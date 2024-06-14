package com.sevenlast.synccity;

import com.sevenlast.synccity.functions.AverageWindowFunction;
import com.sevenlast.synccity.models.AverageResult;
import com.sevenlast.synccity.models.HeatIndexResult;
import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.serialization.HeatIndexSerializationSchema;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;
import java.time.ZonedDateTime;

public class HeatIndexJob {
    private static final String TEMPERATURE_TOPIC = "temperature";
    private static final String HUMIDITY_TOPIC = "humidity";
    private static final Time WINDOW_SIZE = Time.minutes(5);
    private static final String HEAT_INDEX_TOPIC = "heat_index";

    private static final String GROUP_ID = "heat-index-job";


    public static void main(String[] args) throws Exception {

        var bootstrapServers = System.getenv("BOOTSTRAP_SERVERS");
        var schemaRegistryUrl = System.getenv("SCHEMA_REGISTRY_URL");

        if (bootstrapServers == null || schemaRegistryUrl == null) {
            throw new IllegalArgumentException("BOOTSTRAP_SERVERS and SCHEMA_REGISTRY_URL must be set");
        }

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
        env.getConfig().setAutoWatermarkInterval(1000);

        var client = new CachedSchemaRegistryClient(schemaRegistryUrl, 20);
        // temperature and humidity have the same schema, using temperature as a reference
        var temperatureMetadata = client.getLatestSchemaMetadata(TEMPERATURE_TOPIC + "-value");
        var schemaParser = new Schema.Parser();

        var deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(
                schemaParser.parse(temperatureMetadata.getSchema()), schemaRegistryUrl);

        var watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                .withTimestampAssigner((event, timestamp) -> {
                    var eventTimestamp = event.get("timestamp").toString();
                    return ZonedDateTime.parse(eventTimestamp).toInstant().toEpochMilli();
                });

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

        var avgTemperatureStream = env.fromSource(temperatureKafkaSource, watermark, "temperature-source")
                .map(RawData::fromGenericRecord)
                .filter(data -> !data.getGroupName().isEmpty())
                .keyBy(RawData::getGroupName)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new AverageWindowFunction());

        var avgHumidityStream = env.fromSource(humidityKafkaSource, watermark, "humidity-source")
                .map(RawData::fromGenericRecord)
                .filter(data -> !data.getGroupName().isEmpty())
                .keyBy(RawData::getGroupName)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new AverageWindowFunction());


        final double c1 = -42.379;
        final double c2 = 2.04901523;
        final double c3 = 10.14333127;
        final double c4 = -0.22475541;
        final double c5 = -0.00683783;
        final double c6 = -0.05481717;
        final double c7 = 0.00122874;
        final double c8 = 0.00085282;
        final double c9 = -0.00000199;

        var metadata = client.getLatestSchemaMetadata(HEAT_INDEX_TOPIC + "-value");
        var heatIndexSchema = schemaParser.parse(metadata.getSchema());

        var heatIndexStream = avgTemperatureStream.join(avgHumidityStream)
                .where(AverageResult::getGroupName)
                .equalTo(AverageResult::getGroupName)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply((averageTemperature, averageHumidity) -> {
                    double t = averageTemperature.getValue();
                    double h = averageHumidity.getValue();

                    double heatIndex = c1 + (c2 * t) + (c3 * h) + (c4 * t * h)
                            + (c5 * t * t) + (c6 * h * h)
                            + (c7 * t * t * h) + (c8 * t * h * h)
                            + (c9 * t * t * h * h);

                    var sensors = averageTemperature.getSensorNames();
                    sensors.addAll(averageHumidity.getSensorNames());
                    return new HeatIndexResult(
                            sensors,
                            averageTemperature.getGroupName(),
                            heatIndex,
                            t,
                            h,
                            averageTemperature.getWindowStart()
                    );
                });

        var sink = KafkaSink.<HeatIndexResult>builder()
                .setBootstrapServers(bootstrapServers)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(HEAT_INDEX_TOPIC)
                        .setValueSerializationSchema(new HeatIndexSerializationSchema(
                                HEAT_INDEX_TOPIC,
                                heatIndexSchema,
                                schemaRegistryUrl
                        ))
                        .build()
                )
                .build();

//        heatIndexStream.print();
        heatIndexStream.sinkTo(sink);
        env.execute("Heat Index Job");
    }

}