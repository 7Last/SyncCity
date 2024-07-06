package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import com.sevenlast.synccity.utils.MockCollector;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;


public class TimestampDifferenceAggregateFunctionTest {
    @Test
    public void testParking1() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = "00000000-0000-0000-0000-000000000000";
        var groupName = "group-name";
        var sensorName = "sensor-name-1";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var input = List.of(
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp, true), // occupied 0 free 0
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1), false), // occupied 1h free 0
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2), true), // occupied 1h free 1h
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(4), false), // occupied 3h free 1h
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(4).plusMinutes(10), true), // occupied 3h free 1h10m
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(4).plusMinutes(20), false) // occupied 3h10m free 1h10m
        );

        var function = new ParkingTimeDifferenceWindowFunction();
        var window = new TimeWindow(
                timestamp.atZone(ZoneId.of("UTC")).toInstant().toEpochMilli(),
                timestamp.plusDays(1).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli()
        );
        function.apply(uuid, window, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ofHours(3).plusMinutes(10),
                        Duration.ofHours(1).plusMinutes(10),
                        uuid,
                        timestamp,
                        groupName,
                        Set.of(sensorName)
                )
        );
    }

    @Test
    public void testParking2() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = "00000000-0000-0000-0000-000000000000";
        var groupName = "group-name";
        var sensorName = "sensor-name-1";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var input = List.of(
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp, false), // 0 occupied 0 free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1), true), // 1h occupied 0 free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2), false), // 1h occupied 1h free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2).plusMinutes(10), true), // 1h occupied 1h10m free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2).plusMinutes(30), false), // 1h20m occupied 1h10m free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(8), true) // 1h20m occupied 6h40m free
        );

        var function = new ParkingTimeDifferenceWindowFunction();
        var window = new TimeWindow(
                timestamp.atZone(ZoneId.of("UTC")).toInstant().toEpochMilli(),
                timestamp.plusDays(1).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli()
        );
        function.apply(uuid, window, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ofHours(1).plusMinutes(20),
                        Duration.ofHours(6).plusMinutes(40),
                        uuid,
                        timestamp,
                        groupName,
                        Set.of(sensorName)
                )
        );
    }


    @Test
    public void testChargingStation1() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = "00000000-0000-0000-0000-000000000000";
        var groupName = "group-name";
        var sensorName = "sensor-name-1";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var input = List.of(
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp, "type", 0, 20, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusMinutes(20), "type", 0, 11, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1), "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1).plusMinutes(20), "type", 0, 5, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1).plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2), "type", 0, 8, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2).plusMinutes(20), "type", 0, 3, Duration.ZERO, Duration.ZERO)
        );

        var function = new ChargingStationTimeDifferenceWindowFunction();
        var window = new TimeWindow(
                timestamp.atZone(ZoneId.of("UTC")).toInstant().toEpochMilli(),
                timestamp.plusDays(1).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli()
        );
        function.apply(uuid, window, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ofHours(1).plusMinutes(20),
                        Duration.ofHours(1),
                        uuid,
                        timestamp,
                        groupName,
                        Set.of(sensorName)
                )
        );
    }

    @Test
    public void testChargingStationNeverOccupied() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = "00000000-0000-0000-0000-000000000000";
        var groupName = "group-name";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var input = List.of(
                new ChargingStationRawData(uuid, "charging-1", groupName, 0, 0, timestamp, "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, "charging-1", groupName, 0, 0, timestamp.plusHours(2), "type", 0, 0, Duration.ZERO, Duration.ZERO)
        );

        var function = new ChargingStationTimeDifferenceWindowFunction();
        var window = new TimeWindow(
                timestamp.atZone(ZoneId.of("UTC")).toInstant().toEpochMilli(),
                timestamp.plusDays(1).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli()
        );
        function.apply(uuid, window, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ZERO,
                        Duration.ofHours(2),
                        uuid,
                        timestamp,
                        groupName,
                        Set.of("charging-1")
                )
        );
    }

    @Test
    public void parkingNeverOccupied() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = "00000000-0000-0000-0000-000000000000";
        var groupName = "group-name";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var input = List.of(
                new ParkingRawData(uuid, "parking-1", groupName, 0, 0, timestamp, false),
                new ParkingRawData(uuid, "parking-1", groupName, 0, 0, timestamp.plusHours(2), true)
        );

        var function = new ParkingTimeDifferenceWindowFunction();
        var window = new TimeWindow(
                timestamp.atZone(ZoneId.of("UTC")).toInstant().toEpochMilli(),
                timestamp.plusDays(1).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli()
        );

        function.apply(uuid, window, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ZERO,
                        Duration.ofHours(2),
                        uuid,
                        timestamp,
                        groupName,
                        Set.of("parking-1")
                )
        );
    }

}
