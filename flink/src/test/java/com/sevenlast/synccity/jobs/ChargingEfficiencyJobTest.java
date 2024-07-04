package com.sevenlast.synccity.jobs;

import com.sevenlast.synccity.ChargingEfficiencyJob;
import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.utils.CollectionSink;
import com.sevenlast.synccity.utils.SimpleGenericRecord;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.runtime.testutils.MiniClusterResourceConfiguration;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.test.junit5.MiniClusterExtension;
import org.junit.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.extension.RegisterExtension;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;
import java.util.stream.Stream;

import static junit.framework.TestCase.assertEquals;

@ExtendWith(MiniClusterExtension.class)
public class ChargingEfficiencyJobTest {

    @RegisterExtension
    public static final MiniClusterExtension MINI_CLUSTER_RESOURCE = new MiniClusterExtension(
            new MiniClusterResourceConfiguration.Builder()
                    .setNumberSlotsPerTaskManager(2)
                    .setNumberTaskManagers(1)
                    .build());

    @Test
    public void testPipeline() throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var groupName = "group";
        var parkingSensorName = "parking";
        String chargingSensorName = "charging";
        var timestamp = ZonedDateTime.parse("2024-01-01T00:00:00Z");

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

        CollectionSink mockSink = new CollectionSink();
        CollectionSink.values.clear();

        var job = new ChargingEfficiencyJob(
                env.fromData(parkingData),
                env.fromData(chargingData),
                mockSink
        );

        job.execute(env);
        var expected = new ChargingEfficiencyResult(
                0.23076923076923078,
                0.3157894736842105
        );
        var actual = CollectionSink.values.get(0);
        assertEquals(expected, actual);
    }

    private GenericRecord toRecord(ParkingRawData data) {
        var simpleRecord = new SimpleGenericRecord();
        simpleRecord.put("sensor_uuid", data.getSensorUuid().toString());
        simpleRecord.put("sensor_name", data.getSensorName());
        simpleRecord.put("group_name", data.getGroupName());
        simpleRecord.put("latitude", data.getLatitude());
        simpleRecord.put("longitude", data.getLongitude());
        simpleRecord.put("timestamp", data.getTimestamp().format(DateTimeFormatter.ISO_OFFSET_DATE_TIME));
        simpleRecord.put("is_occupied", data.isOccupied());
        return simpleRecord;
    }

    private GenericRecord toRecord(ChargingStationRawData data) {
        var simpleRecord = new SimpleGenericRecord();
        simpleRecord.put("sensor_uuid", data.getSensorUuid().toString());
        simpleRecord.put("sensor_name", data.getSensorName());
        simpleRecord.put("group_name", data.getGroupName());
        simpleRecord.put("latitude", data.getLatitude());
        simpleRecord.put("longitude", data.getLongitude());
        simpleRecord.put("timestamp", data.getTimestamp().format(DateTimeFormatter.ISO_OFFSET_DATE_TIME));
        simpleRecord.put("kwh_supplied", data.getKwhSupplied());
        simpleRecord.put("battery_level", data.getBatteryLevel());
        simpleRecord.put("remaining_charge_time", data.getRemainingChargeTime().getSeconds());
        simpleRecord.put("elapsed_time", data.getElapsedTime().getSeconds());
        simpleRecord.put("vehicle_type", data.getVehicleType());
        return simpleRecord;
    }
}
