package com.sevenlast.synccity;

import com.sevenlast.synccity.functions.ChargingEfficiencyJoinFunction;
import com.sevenlast.synccity.functions.TimestampDifferenceAggregateFunction;
import com.sevenlast.synccity.models.*;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.UUID;

public class ChargingEfficiencyJob {
    private static final String PARKING_TOPIC = "parking";
    private static final String CHARGING_STATION_TOPIC = "charging_station";
    private static final Duration WINDOW_SIZE = Duration.ofDays(1);
    private static final String CHARGING_EFFICIENCY_TOPIC = "charging_efficiency";
    private static final String GROUP_ID = "charging-efficiency-job";


    public static void main(String[] args) throws Exception {

        var bootstrapServers = System.getenv("BOOTSTRAP_SERVERS");
        var schemaRegistryUrl = System.getenv("SCHEMA_REGISTRY_URL");

        if (bootstrapServers == null || schemaRegistryUrl == null) {
            throw new IllegalArgumentException("BOOTSTRAP_SERVERS and SCHEMA_REGISTRY_URL must be set");
        }

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.STREAMING);
        env.getConfig().setAutoWatermarkInterval(1000);

//        var client = new CachedSchemaRegistryClient(schemaRegistryUrl, 20);
//        var schemaParser = new Schema.Parser();
//        var watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
//                .withTimestampAssigner((event, timestamp) -> {
//                    var eventTimestamp = event.get("timestamp").toString();
//                    return ZonedDateTime.parse(eventTimestamp).toInstant().toEpochMilli();
//                });
//
//        // Source
//        var parkingMetadata = client.getLatestSchemaMetadata(PARKING_TOPIC + "-value");
//        var parkingKafkaSource = KafkaSource.<GenericRecord>builder()
//                .setStartingOffsets(OffsetsInitializer.latest())
//                .setBootstrapServers(bootstrapServers)
//                .setTopics(PARKING_TOPIC)
//                .setGroupId(GROUP_ID)
//                .setValueOnlyDeserializer(ConfluentRegistryAvroDeserializationSchema.forGeneric(
//                        schemaParser.parse(parkingMetadata.getSchema()), schemaRegistryUrl))
//                .build();
//
//        var chargingStationMetadata = client.getLatestSchemaMetadata(CHARGING_STATION_TOPIC + "-value");
//        var chargingStationKafkaSource = KafkaSource.<GenericRecord>builder()
//                .setStartingOffsets(OffsetsInitializer.latest())
//                .setBootstrapServers(bootstrapServers)
//                .setTopics(CHARGING_STATION_TOPIC)
//                .setGroupId(GROUP_ID)
//                .setValueOnlyDeserializer(ConfluentRegistryAvroDeserializationSchema.forGeneric(
//                        schemaParser.parse(chargingStationMetadata.getSchema()), schemaRegistryUrl))
//                .build();
//
//        // Aggregations
//        var efficiencyMetadata = client.getLatestSchemaMetadata(CHARGING_EFFICIENCY_TOPIC + "-value");

        // efficienza 1 = (tempo col. in uso) / (tempo parcheggio totale)
        // efficienza 2 = (tempo col. in uso) / (tempo parcheggio true)


        var uuid = UUID.randomUUID();
        var now = ZonedDateTime.parse("2024-01-01T00:00:00Z");
        var parkingData = List.of(
                new ParkingRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(1), false), // 0 true 0 false
                new ParkingRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(2), true), // 0 true 1 false
                new ParkingRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(3), false), // 1 true 1 false
                new ParkingRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(4), true) // 1 true 2 false
        );

        var chargingStationData = List.of(
                new ChargingStationRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(1), "car", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(2), "car", 0, 20, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(3), "car", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, "1", "test", 45.4642, 9.1900, now.plusHours(4), "car", 0, 20, Duration.ZERO, Duration.ZERO)
        );

//        var parkingStream = env.fromSource(parkingKafkaSource, watermark, "parking-source")
//                .map(ParkingRawData::fromGenericRecord)
        var parkingStream = env.fromCollection(parkingData)
                .assignTimestampsAndWatermarks(WatermarkStrategy.<ParkingRawData>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                        .withTimestampAssigner((event, timestamp) -> event.getTimestamp().toInstant().toEpochMilli()))
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy(ParkingRawData::getSensorUuid)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new TimestampDifferenceAggregateFunction<>());

//        var chargingStationStream = env.fromSource(chargingStationKafkaSource, watermark, "charging-station-source")
//                .map(ChargingStationRawData::fromGenericRecord)
        var chargingStationStream = env.fromCollection(chargingStationData)
                .assignTimestampsAndWatermarks(WatermarkStrategy.<ChargingStationRawData>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                        .withTimestampAssigner((event, timestamp) -> event.getTimestamp().toInstant().toEpochMilli()))
                .filter(data -> data.getGroupName() != null && !data.getGroupName().isEmpty())
                .keyBy(ChargingStationRawData::getSensorUuid)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new TimestampDifferenceAggregateFunction<>());

        var efficiencyStream = parkingStream.join(chargingStationStream)
                .where(TimestampDifferenceResult::getSensorUuid)
                .equalTo(TimestampDifferenceResult::getSensorUuid)
                .window(TumblingEventTimeWindows.of(WINDOW_SIZE))
                .apply(new ChargingEfficiencyJoinFunction())
                .print();

        // Sink
//        var sink = KafkaSink.<RecordSerializable>builder()
//                .setBootstrapServers(bootstrapServers)
//                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
//                        .setTopic(CHARGING_EFFICIENCY_TOPIC)
//                        .setValueSerializationSchema(new RecordSerializationSchema(
//                                CHARGING_EFFICIENCY_TOPIC,
//                                schemaParser.parse(efficiencyMetadata.getSchema()),
//                                schemaRegistryUrl
//                        ))
//                        .build()
//                )
//                .build();
//
//        heatIndexStream.sinkTo(sink);
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