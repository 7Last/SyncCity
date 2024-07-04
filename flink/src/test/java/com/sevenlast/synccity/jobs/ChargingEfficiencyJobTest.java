package com.sevenlast.synccity.jobs;

import com.sevenlast.synccity.ChargingEfficiencyJob;
import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.utils.CollectionSink;
import com.sevenlast.synccity.utils.SimpleGenericRecord;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.connector.sink2.SinkWriter;
import org.apache.flink.api.connector.sink2.WriterInitContext;
import org.apache.flink.runtime.testutils.MiniClusterResourceConfiguration;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.operators.collect.CollectSinkFunction;
import org.apache.flink.streaming.experimental.CollectSink;
import org.apache.flink.test.junit5.MiniClusterExtension;
import org.junit.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.extension.RegisterExtension;

import java.io.IOException;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import static org.junit.Assert.assertNotEquals;

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
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        UUID uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");

        var parkingData = List.of(
                toRecord(new ParkingRawData(uuid, "name", "group", 0, 0, ZonedDateTime.now(), false))
        );

        var chargingData = List.of(
                toRecord(new ChargingStationRawData(uuid, "name", "group", 0, 0, ZonedDateTime.now(), "type", 0, 0, Duration.ofSeconds(0), Duration.ofSeconds(0)))
        );

        CollectionSink mockSink = new CollectionSink();
        CollectionSink.values.clear();

        var job = new ChargingEfficiencyJob(
                env.fromData(parkingData),
                env.fromData(chargingData),
                mockSink
        );

        job.execute(env);
        assertNotEquals(0, CollectionSink.values.size());
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
