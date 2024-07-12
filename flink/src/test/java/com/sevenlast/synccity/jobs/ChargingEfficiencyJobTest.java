package com.sevenlast.synccity.jobs;

import com.sevenlast.synccity.ChargingEfficiencyJob;
import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.serialization.ChargingEfficiencyRecordSerializableAdapter;
import com.sevenlast.synccity.serialization.RecordSerializable;
import com.sevenlast.synccity.utils.CollectionSink;
import com.sevenlast.synccity.utils.SimpleGenericRecord;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;


public class ChargingEfficiencyJobTest {
    private final WatermarkStrategy<GenericRecord> watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
            .withTimestampAssigner((event, timestamp) -> {
                var eventTimestamp = event.get("timestamp").toString();
                return LocalDateTime.parse(eventTimestamp).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli();

            });

    @BeforeEach
    public void before() {
        CollectionSink.values.clear();
    }

    @Test
    public void testSingleSensor() throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        var uuid = "00000000-0000-0000-0000-000000000000";
        var groupName = "group";
        var parkingSensorName = "parking";
        String chargingSensorName = "charging";
        var timestamp = LocalDateTime.parse("2024-01-01T00:00:00");

        //@formatter:off
        var parkingData = Stream.of(
                new ParkingRawData(uuid, parkingSensorName, groupName, 0, 0, timestamp, true), // occupied 0 free 0
                new ParkingRawData(uuid, parkingSensorName, groupName, 0, 0, timestamp.plusHours(1), false), // occupied 1h free 0
                new ParkingRawData(uuid, parkingSensorName, groupName, 0, 0, timestamp.plusHours(2), true), // occupied 1h free 1h
                new ParkingRawData(uuid, parkingSensorName, groupName, 0, 0, timestamp.plusHours(4), false), // occupied 3h free 1h
                new ParkingRawData(uuid, parkingSensorName, groupName, 0, 0, timestamp.plusHours(4).plusMinutes(10), true), // occupied 3h free 1h10m
                new ParkingRawData(uuid, parkingSensorName, groupName, 0, 0, timestamp.plusHours(4).plusMinutes(20), false) // occupied 3h10m free 1h10m
        ).map(this::toRecord).toList();
        //@formatter:on

        //@formatter:off
        var chargingData = Stream.of(
            // 4 * 20m = used for 1h20m
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp, "type", 0, 20, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp.plusMinutes(20), "type", 0, 11, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp.plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp.plusHours(1), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp.plusHours(1).plusMinutes(20), "type", 0, 5, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp.plusHours(1).plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp.plusHours(2), "type", 0, 8, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid, chargingSensorName, groupName, 0, 0, timestamp.plusHours(2).plusMinutes(20), "type", 0, 3, Duration.ZERO, Duration.ZERO)
        ).map(this::toRecord).toList();
        //@formatter:on

        var mockSink = new CollectionSink<RecordSerializable>();

        var job = new ChargingEfficiencyJob(
                env.fromCollection(parkingData),
                env.fromCollection(chargingData),
                mockSink,
                watermark
        );

        job.execute(env);
        var expected = new ChargingEfficiencyResult(
                0.3076923076923077,
                0.42105263157894735,
                uuid,
                timestamp,
                groupName,
                Set.of(parkingSensorName, chargingSensorName)
        );
        var actual = ((ChargingEfficiencyRecordSerializableAdapter) CollectionSink.values.get(0)).getAdaptee();
        assertEquals(expected, actual);
    }

    @Test
    public void maximumEfficiencyAndUtilizationTest() throws Exception {
        // Efficiency is 1.0 when the charging station is always in use when the park is occupied
        // Utilization is 1.0 when the charging station is always in use in respect to the total time

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        var uuid1 = "00000000-0000-0000-0000-000000000000";
        var uuid2 = "00000000-0000-0000-0000-000000000001";
        var groupName = "group";
        var timestamp = LocalDateTime.parse("2024-01-01T00:00:00");

        var parkingData = List.of(
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp, true), // occupied 0 free 0
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp.plusHours(2), false), // occupied 2h free 0

                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp, true), // occupied 0 free 0
                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp.plusHours(1), false) // occupied 1h free 0
        );

        var chargingData = List.of(
                // occupied 2h free 0
                new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp, "type", 0f, 0f, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusHours(2), "type", 0f, 1f, Duration.ZERO, Duration.ZERO),

                // occupied 1h free 0
                new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp, "type", 0f, 0f, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusHours(1), "type", 0f, 1f, Duration.ZERO, Duration.ZERO)
        );

        var mockSink = new CollectionSink<RecordSerializable>();

        var job = new ChargingEfficiencyJob(
                env.fromCollection(parkingData.stream().map(this::toRecord).toList()),
                env.fromCollection(chargingData.stream().map(this::toRecord).toList()),
                mockSink,
                watermark
        );
        job.execute(env);

        var maxEfficiency = List.of(
                new ChargingEfficiencyResult(
                        1.0,
                        1.0,
                        uuid1,
                        timestamp,
                        groupName,
                        Set.of("parking-1", "charging-1")
                ),
                new ChargingEfficiencyResult(
                        1.0,
                        1.0,
                        uuid2,
                        timestamp,
                        groupName,
                        Set.of("parking-2", "charging-2")
                )
        );

        var actual = CollectionSink.values
                .stream().map(ChargingEfficiencyRecordSerializableAdapter.class::cast)
                .map(ChargingEfficiencyRecordSerializableAdapter::getAdaptee).toList();

        assertTrue(
                actual.size() == 2 &&
                        maxEfficiency.containsAll(actual) &&
                        actual.containsAll(maxEfficiency)
        );
    }

    @Test
    public void zeroEfficiencyAndUtilizationTest() throws Exception {
        // Efficiency is 0.0 when the charging station is never in use when the park is occupied
        // Utilization is 0.0 when the charging station is never in use in respect to the total time

        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        var uuid1 = "00000000-0000-0000-0000-000000000000";
        var uuid2 = "00000000-0000-0000-0000-000000000001";
        var groupName = "group";
        var beginDate = LocalDateTime.parse("2024-01-01T00:00:00");

        var parkingData = List.of(
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, beginDate, true), // occupied 0 free 0
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, beginDate.plusHours(2), false), // occupied 2h free 0

                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, beginDate, true), // occupied 0 free 0
                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, beginDate.plusHours(1), false) // occupied 1h free 0
        );

        var chargingData = List.of(
                new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, beginDate, "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, beginDate.plusHours(2), "type", 0, 0, Duration.ZERO, Duration.ZERO),

                new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, beginDate, "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, beginDate.plusHours(1), "type", 0, 0, Duration.ZERO, Duration.ZERO)
        );


        var mockSink = new CollectionSink<RecordSerializable>();

        var job = new ChargingEfficiencyJob(
                env.fromCollection(parkingData.stream().map(this::toRecord).toList()),
                env.fromCollection(chargingData.stream().map(this::toRecord).toList()),
                mockSink,
                watermark
        );

        job.execute(env);

        var minEfficiency = List.of(
                ChargingEfficiencyResult.zero(uuid1, beginDate, groupName, Set.of("parking-1", "charging-1")),
                ChargingEfficiencyResult.zero(uuid2, beginDate, groupName, Set.of("parking-2", "charging-2"))
        );

        var actual = CollectionSink.values
                .stream().map(ChargingEfficiencyRecordSerializableAdapter.class::cast)
                .map(ChargingEfficiencyRecordSerializableAdapter::getAdaptee).toList();

        assertTrue(
                actual.size() == 2 &&
                        minEfficiency.containsAll(actual) &&
                        actual.containsAll(minEfficiency)
        );
    }

    @Test
    public void multipleSensors() throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        var uuid1 = "00000000-0000-0000-0000-000000000000";
        var uuid2 = "00000000-0000-0000-0000-000000000001";
        var groupName = "group";
        var timestamp = LocalDateTime.parse("2024-01-01T00:00:00");

        //@formatter:off
        var parkingData = Stream.of(
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp, true), // occupied 0 free 0
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp.plusMinutes(20), false), // occupied 20m free 0
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp.plusHours(2), true), // occupied 20m free 1h40m
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp.plusHours(4), false), // occupied 2h20m free 1h40m
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp.plusHours(4).plusMinutes(10), true), // occupied 2h20m free 1h50m
                new ParkingRawData(uuid1, "parking-1", groupName, 0, 0, timestamp.plusHours(4).plusMinutes(20), false), // occupied 2h30m free 1h50m

                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp, true), // occupied 0 free 0
                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp.plusMinutes(5), false), // occupied 5m free 0
                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp.plusMinutes(20), true), // occupied 5m free 15m
                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp.plusHours(3), false), // occupied 2h45m free 15m
                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp.plusHours(3).plusMinutes(10), true), // occupied 2h45m free 25m
                new ParkingRawData(uuid2, "parking-2", groupName, 0, 0, timestamp.plusHours(4).plusMinutes(20), false) // occupied 3h55m free 25m
        ).map(this::toRecord).toList();
        //@formatter:on

        //@formatter:off
        var chargingData = Stream.of(
            // occupied 1h20m free 1h
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp, "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusMinutes(20), "type", 0, 11, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusHours(1), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusHours(1).plusMinutes(20), "type", 0, 5, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusHours(1).plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusHours(2), "type", 0, 8, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid1, "charging-1", groupName, 0, 0, timestamp.plusHours(2).plusMinutes(20), "type", 0, 3, Duration.ZERO, Duration.ZERO),

            // occupied 40m free 1h40m
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp, "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusMinutes(20), "type", 5, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusMinutes(40), "type", 0, 10, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusHours(1), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusHours(1).plusMinutes(20), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusHours(1).plusMinutes(40), "type", 0, 10, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusHours(2), "type", 0, 0, Duration.ZERO, Duration.ZERO),
            new ChargingStationRawData(uuid2, "charging-2", groupName, 0, 0, timestamp.plusHours(2).plusMinutes(20), "type", 0, 0, Duration.ZERO, Duration.ZERO)
        ).map(this::toRecord).toList();
        //@formatter:on

        var mockSink = new CollectionSink<RecordSerializable>();

        var job = new ChargingEfficiencyJob(
                env.fromCollection(parkingData),
                env.fromCollection(chargingData),
                mockSink,
                watermark
        );

        job.execute(env);
        var expected = List.of(
                new ChargingEfficiencyResult(
                        0.3076923076923077,
                        0.5333333333333333,
                        uuid1,
                        timestamp,
                        groupName,
                        Set.of("parking-1", "charging-1")
                ),
                new ChargingEfficiencyResult(
                        0.15384615384615385,
                        0.1702127659574468,
                        uuid2,
                        timestamp,
                        groupName,
                        Set.of("parking-2", "charging-2")
                )
        );

        var actual = CollectionSink.values
                .stream().map(ChargingEfficiencyRecordSerializableAdapter.class::cast)
                .map(ChargingEfficiencyRecordSerializableAdapter::getAdaptee).toList();

        assertTrue(
                actual.size() == 2 &&
                        expected.containsAll(actual) &&
                        actual.containsAll(expected)
        );
    }

    private GenericRecord toRecord(ParkingRawData data) {
        var simpleRecord = new SimpleGenericRecord();
        simpleRecord.put("sensor_uuid", data.getSensorUuid());
        simpleRecord.put("sensor_name", data.getSensorName());
        simpleRecord.put("group_name", data.getGroupName());
        simpleRecord.put("latitude", data.getLatitude());
        simpleRecord.put("longitude", data.getLongitude());
        simpleRecord.put("timestamp", data.getTimestamp().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        simpleRecord.put("is_occupied", data.isOccupied());
        return simpleRecord;
    }

    private GenericRecord toRecord(ChargingStationRawData data) {
        var simpleRecord = new SimpleGenericRecord();
        simpleRecord.put("sensor_uuid", data.getSensorUuid());
        simpleRecord.put("sensor_name", data.getSensorName());
        simpleRecord.put("group_name", data.getGroupName());
        simpleRecord.put("latitude", data.getLatitude());
        simpleRecord.put("longitude", data.getLongitude());
        simpleRecord.put("timestamp", data.getTimestamp().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        simpleRecord.put("kwh_supplied", data.getKwhSupplied());
        simpleRecord.put("battery_level", data.getBatteryLevel());
        simpleRecord.put("remaining_charge_time", data.getRemainingChargeTime().getSeconds());
        simpleRecord.put("elapsed_time", data.getElapsedTime().getSeconds());
        simpleRecord.put("vehicle_type", data.getVehicleType());
        return simpleRecord;
    }
}
