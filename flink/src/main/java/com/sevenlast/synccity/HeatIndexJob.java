package com.sevenlast.synccity;

import com.sevenlast.synccity.functions.AverageWindowFunction;
import com.sevenlast.synccity.models.AverageResult;
import com.sevenlast.synccity.models.HeatIndexResult;
import com.sevenlast.synccity.models.HumTempRawData;
import com.sevenlast.synccity.models.SensorLocation;
import com.sevenlast.synccity.serialization.RecordSerializable;
import com.sevenlast.synccity.serialization.RecordSerializationSchema;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.stream.Collectors;

public class HeatIndexJob {
    private static final String TEMPERATURE_TOPIC = "temperature";
    private static final String HUMIDITY_TOPIC = "humidity";
    private static final Time WINDOW_SIZE = Time.hours(1);
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

        final double c1 = -8.78469475556;
        final double c2 = 1.61139411;
        final double c3 = 2.33854883889;
        final double c4 = -0.14611605;
        final double c5 = -0.012308094;
        final double c6 = -0.0164248277778;
        final double c7 = 2.211732e-3;
        final double c8 = 7.2546e-4;
        final double c9 = -3.582e-6;

        var metadata = client.getLatestSchemaMetadata(HEAT_INDEX_TOPIC + "-value");
        var heatIndexSchema = schemaParser.parse(metadata.getSchema());

        DataStream<RecordSerializable> heatIndexStream = avgTemperatureStream.join(avgHumidityStream)
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

                    var sensors = averageTemperature.getSensors();
                    sensors.addAll(averageHumidity.getSensors());

                    Tuple2<Double, Double> centerOfMass = sensors.stream()
                            .map(sensor -> new Tuple2<>(sensor.getLatitude(), sensor.getLongitude()))
                            .reduce((a, b) -> new Tuple2<>(a.f0 + b.f0, a.f1 + b.f1))
                            .map(tuple -> new Tuple2<>(tuple.f0 / sensors.size(), tuple.f1 / sensors.size()))
                            .orElseThrow();

                    double maxRadius = sensors.stream()
                            .map(sensor -> haversine(sensor.getLatitude(), sensor.getLongitude(), centerOfMass.f0, centerOfMass.f1))
                            .max(Double::compareTo)
                            .orElseThrow();

                    return new HeatIndexResult(
                            sensors.stream().map(SensorLocation::getSensorName).collect(Collectors.toSet()),
                            averageTemperature.getGroupName(),
                            heatIndex,
                            averageTemperature.getValue(),
                            averageHumidity.getValue(),
                            centerOfMass.f0,
                            centerOfMass.f1,
                            maxRadius,
                            averageTemperature.getWindowStart()
                    );
                });

        var sink = KafkaSink.<RecordSerializable>builder()
                .setBootstrapServers(bootstrapServers)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(HEAT_INDEX_TOPIC)
                        .setValueSerializationSchema(new RecordSerializationSchema(
                                HEAT_INDEX_TOPIC,
                                heatIndexSchema,
                                schemaRegistryUrl
                        ))
                        .build()
                )
                .build();

        heatIndexStream.sinkTo(sink);
        env.execute("Heat Index Job");
    }

    static double haversine(double lat1, double lon1, double lat2, double lon2) {
        double latitudeDistance = Math.toRadians(lat2 - lat1);
        double longitudeDistance = Math.toRadians(lon2 - lon1);

        // convert to radians
        lat1 = Math.toRadians(lat1);
        lat2 = Math.toRadians(lat2);

        // apply formulae
        double a = Math.pow(Math.sin(latitudeDistance / 2), 2) +
                Math.pow(Math.sin(longitudeDistance / 2), 2) *
                        Math.cos(lat1) *
                        Math.cos(lat2);
        double rad = 6371;
        double c = 2 * Math.asin(Math.sqrt(a));
        return rad * c; // in kilometers
    }
}