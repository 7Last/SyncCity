package com.sevenlast.synccity;

import com.sevenlast.synccity.functions.ChargingEfficiencyJoinFunction;
import com.sevenlast.synccity.functions.ChargingStationTimeDifferenceWindowFunction;
import com.sevenlast.synccity.functions.ParkingTimeDifferenceWindowFunction;
import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import com.sevenlast.synccity.serialization.ChargingEfficiencyRecordSerializableAdapter;
import com.sevenlast.synccity.serialization.RecordSerializable;
import com.sevenlast.synccity.serialization.RecordSerializationSchema;
import io.confluent.kafka.schemaregistry.client.CachedSchemaRegistryClient;
import lombok.AllArgsConstructor;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroDeserializationSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.DataStreamSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.SinkFunction;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;

@SuppressWarnings("ALL")
@AllArgsConstructor
public class ChargingEfficiencyJob {
    private static final String PARKING_TOPIC = "parking";
    private static final String CHARGING_STATION_TOPIC = "charging_station";
    private static final Time WINDOW_SIZE = Time.days(1);
    private static final String CHARGING_EFFICIENCY_TOPIC = "charging_efficiency";
    private static final String GROUP_ID = "charging-efficiency-job";

    private DataStreamSource<GenericRecord> parkingKafkaSource;
    private DataStreamSource<GenericRecord> chargingStationKafkaSource;
    private SinkFunction<RecordSerializable> efficiencySink;
    private WatermarkStrategy<GenericRecord> watermark;

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
        env.setParallelism(1);

        // Source
        var parkingMetadata = client.getLatestSchemaMetadata(PARKING_TOPIC + "-value");
        var deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(
                schemaParser.parse(parkingMetadata.getSchema()), schemaRegistryUrl);

        var parkingKafkaSource = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(bootstrapServers)
                .setTopics(PARKING_TOPIC)
                .setGroupId(GROUP_ID)
                .setValueOnlyDeserializer(deserializer)
                .build();

        var chargingStationMetadata = client.getLatestSchemaMetadata(CHARGING_STATION_TOPIC + "-value");
        deserializer = ConfluentRegistryAvroDeserializationSchema.forGeneric(
                schemaParser.parse(chargingStationMetadata.getSchema()), schemaRegistryUrl);
        var chargingStationKafkaSource = KafkaSource.<GenericRecord>builder()
                .setStartingOffsets(OffsetsInitializer.latest())
                .setBootstrapServers(bootstrapServers)
                .setTopics(CHARGING_STATION_TOPIC)
                .setGroupId(GROUP_ID)
                .setValueOnlyDeserializer(deserializer)
                .build();

        // Aggregations
        var efficiencyMetadata = client.getLatestSchemaMetadata(CHARGING_EFFICIENCY_TOPIC + "-value");
        var sink = new FlinkKafkaProducer<>(
                bootstrapServers,
                CHARGING_EFFICIENCY_TOPIC,
                new RecordSerializationSchema<>(
                        CHARGING_EFFICIENCY_TOPIC,
                        schemaParser.parse(efficiencyMetadata.getSchema()),
                        schemaRegistryUrl
                )
        );

        var watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                .withTimestampAssigner((event, timestamp) -> {
                    var eventTimestamp = event.get("timestamp").toString();
                    return LocalDateTime.parse(eventTimestamp).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli();
                });

        new ChargingEfficiencyJob(
                env.fromSource(parkingKafkaSource, watermark, "Parking Kafka Source"),
                env.fromSource(chargingStationKafkaSource, watermark, "Charging Station Kafka Source"),
                sink,
                watermark
        ).execute(env);
    }

    public void execute(StreamExecutionEnvironment env) throws Exception {
        var parkingStream = parkingKafkaSource
                .assignTimestampsAndWatermarks(watermark)
                .map(ParkingRawData::fromGenericRecord)
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy((data) -> data.getSensorUuid().toString())
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new ParkingTimeDifferenceWindowFunction());

        var chargingStationStream = chargingStationKafkaSource
                .assignTimestampsAndWatermarks(watermark)
                .map(ChargingStationRawData::fromGenericRecord)
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy((data) -> data.getSensorUuid().toString())
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new ChargingStationTimeDifferenceWindowFunction());

        DataStream<RecordSerializable> efficiencyStream = parkingStream.join(chargingStationStream)
                .where(TimestampDifferenceResult::getSensorUuid)
                .equalTo(TimestampDifferenceResult::getSensorUuid)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new ChargingEfficiencyJoinFunction())
                .map(ChargingEfficiencyRecordSerializableAdapter::new);

        efficiencyStream.addSink(efficiencySink);
        env.execute("Charging Efficiency Job");
    }
}