package com.sevenlast.synccity.jobs;

import com.sevenlast.synccity.ChargingEfficiencyJob;
import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.utils.MockCollectSink;
import com.sevenlast.synccity.utils.SimpleGenericRecord;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.runtime.testutils.MiniClusterResourceConfiguration;
import org.apache.flink.streaming.api.datastream.DataStreamSink;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.PrintSink;
import org.apache.flink.streaming.api.functions.sink.v2.DiscardingSink;
import org.apache.flink.streaming.experimental.CollectSink;
import org.apache.flink.test.junit5.MiniClusterExtension;
import org.junit.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.extension.RegisterExtension;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

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

        var parkingData = List.of(
                toRecord(new ParkingRawData(UUID.randomUUID(), "name", "group", 0, 0, ZonedDateTime.now(), false))
        );

        var chargingData = List.of(
                toRecord(new ChargingStationRawData(UUID.randomUUID(), "name", "group", 0, 0, ZonedDateTime.now(), "type", 0, 0, Duration.ofSeconds(0), Duration.ofSeconds(0)))
        );

        var collectSink = new PrintSink<ChargingEfficiencyResult>();
//
        var job = new ChargingEfficiencyJob(
                env.fromData(parkingData),
                env.fromData(chargingData),
                collectSink
        );

        job.execute(env);

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
