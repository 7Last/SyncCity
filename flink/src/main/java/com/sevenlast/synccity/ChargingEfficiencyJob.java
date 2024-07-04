package com.sevenlast.synccity;

import com.sevenlast.synccity.functions.ChargingEfficiencyJoinFunction;
import com.sevenlast.synccity.functions.TimestampDifferenceAggregateFunction;
import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import com.sevenlast.synccity.serialization.RecordSerializationSchema;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import lombok.AllArgsConstructor;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.datastream.DataStreamSink;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.SinkFunction;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;

import java.time.Duration;
import java.time.ZonedDateTime;

@AllArgsConstructor
public class ChargingEfficiencyJob {
    private static final String PARKING_TOPIC = "parking";
    private static final String CHARGING_STATION_TOPIC = "charging_station";
    private static final Duration WINDOW_SIZE = Duration.ofDays(1);
    private static final String CHARGING_EFFICIENCY_TOPIC = "charging_efficiency";
    private static final String GROUP_ID = "charging-efficiency-job";

    private DataStreamSource<GenericRecord> parkingKafkaSource;
    private DataStreamSource<GenericRecord> chargingStationKafkaSource;
    private Sink<ChargingEfficiencyResult> efficiencySink;

    public static void main(String[] args) throws Exception {

        var bootstrapServers = System.getenv("BOOTSTRAP_SERVERS");
        var schemaRegistryUrl = System.getenv("SCHEMA_REGISTRY_URL");

        if (bootstrapServers == null || schemaRegistryUrl == null) {
            throw new IllegalArgumentException("BOOTSTRAP_SERVERS and SCHEMA_REGISTRY_URL must be set");
        }

        var client = new CachedSchemaRegistryClient(schemaRegistryUrl, 20);
        var schemaParser = new Schema.Parser();

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
        env.getConfig().setAutoWatermarkInterval(1000);

        // Source
        var parkingMetadata = client.getLatestSchemaMetadata(PARKING_TOPIC + "-value");
        var parkingKafkaSource = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(bootstrapServers)
                .setTopics(PARKING_TOPIC)
                .setGroupId(GROUP_ID)
                .setValueOnlyDeserializer(ConfluentRegistryAvroDeserializationSchema.forGeneric(
                        schemaParser.parse(parkingMetadata.getSchema()), schemaRegistryUrl))
                .build();

        var chargingStationMetadata = client.getLatestSchemaMetadata(CHARGING_STATION_TOPIC + "-value");
        var chargingStationKafkaSource = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(bootstrapServers)
                .setTopics(CHARGING_STATION_TOPIC)
                .setGroupId(GROUP_ID)
                .setValueOnlyDeserializer(ConfluentRegistryAvroDeserializationSchema.forGeneric(
                        schemaParser.parse(chargingStationMetadata.getSchema()), schemaRegistryUrl))
                .build();

        // Aggregations
        var efficiencyMetadata = client.getLatestSchemaMetadata(CHARGING_EFFICIENCY_TOPIC + "-value");
        var sink = KafkaSink.<ChargingEfficiencyResult>builder()
                .setBootstrapServers(bootstrapServers)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(CHARGING_EFFICIENCY_TOPIC)
                        .setValueSerializationSchema(new RecordSerializationSchema<ChargingEfficiencyResult>(
                                CHARGING_EFFICIENCY_TOPIC,
                                schemaParser.parse(efficiencyMetadata.getSchema()),
                                schemaRegistryUrl
                        ))
                        .build()
                ).build();

        var watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                .withTimestampAssigner((event, timestamp) -> {
                    var eventTimestamp = event.get("timestamp").toString();
                    return ZonedDateTime.parse(eventTimestamp).toInstant().toEpochMilli();
                });

        new ChargingEfficiencyJob(
                env.fromSource(parkingKafkaSource, watermark, "Parking Kafka Source"),
                env.fromSource(chargingStationKafkaSource, watermark, "Charging Station Kafka Source"),
                sink
        ).execute(env);
    }

    public void execute(StreamExecutionEnvironment env) throws Exception {
        var parkingStream = parkingKafkaSource
                .assignTimestampsAndWatermarks(WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                        .withTimestampAssigner((event, timestamp) -> {
                            var eventTimestamp = event.get("timestamp").toString();
                            return ZonedDateTime.parse(eventTimestamp).toInstant().toEpochMilli();
                        }))
                .map(ParkingRawData::fromGenericRecord)
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy(ParkingRawData::getSensorUuid)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new TimestampDifferenceAggregateFunction<>());

        var chargingStationStream = chargingStationKafkaSource
                .assignTimestampsAndWatermarks(WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                        .withTimestampAssigner((event, timestamp) -> {
                            var eventTimestamp = event.get("timestamp").toString();
                            return ZonedDateTime.parse(eventTimestamp).toInstant().toEpochMilli();
                        }))
                .map(ChargingStationRawData::fromGenericRecord)
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy(ChargingStationRawData::getSensorUuid)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new TimestampDifferenceAggregateFunction<>());

        var efficiencyStream = parkingStream.join(chargingStationStream)
                .where(TimestampDifferenceResult::getSensorUuid)
                .equalTo(TimestampDifferenceResult::getSensorUuid)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new ChargingEfficiencyJoinFunction());

        efficiencyStream.sinkTo(efficiencySink);
        env.execute("Charging Efficiency Job");
    }
}