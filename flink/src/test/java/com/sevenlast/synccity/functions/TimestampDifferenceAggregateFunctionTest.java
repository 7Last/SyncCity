package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import com.sevenlast.synccity.utils.MockCollector;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;


public class TimestampDifferenceAggregateFunctionTest {
    @Test
    public void testParking1() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var groupName = "group-name";
        var sensorName = "sensor-name-1";
        var timestamp = ZonedDateTime.parse("2021-01-01T00:00:00Z");

        List<RawData> input = List.of(
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp, true), // occupied 0 free 0
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1), false), // occupied 1h free 0
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2), true), // occupied 1h free 1h
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(4), false), // occupied 3h free 1h
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(4).plusMinutes(10), true), // occupied 3h free 1h10m
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(4).plusMinutes(20), false) // occupied 3h10m free 1h10m
        );

        var function = new TimestampDifferenceAggregateFunction<>();
        function.apply(uuid, null, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ofHours(3).plusMinutes(10),
                        Duration.ofHours(1).plusMinutes(10),
                        uuid
                )
        );
    }

    @Test
    public void testParking2() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var groupName = "group-name";
        var sensorName = "sensor-name-1";
        var beginDate = ZonedDateTime.parse("2021-01-01T00:00:00Z");

        List<RawData> input = List.of(
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, beginDate, false), // 0 occupied 0 free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, beginDate.plusHours(1), true), // 0 occupied 1h free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, beginDate.plusHours(2), false), // 1h occupied 1h free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, beginDate.plusHours(2).plusMinutes(10), true), // 1h10m occupied 1h free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, beginDate.plusHours(2).plusMinutes(30), false), // 1h10m occupied 1h20m free
                new ParkingRawData(uuid, sensorName, groupName, 0, 0, beginDate.plusHours(8), true) // 6h40m occupied 1h20m free
        );

        var function = new TimestampDifferenceAggregateFunction<>();
        function.apply(uuid, null, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ofHours(6).plusMinutes(40),
                        Duration.ofHours(1).plusMinutes(20),
                        uuid
                )
        );
    }

    @Test
    public void chargingStation1() {
        var mockCollector = new MockCollector<TimestampDifferenceResult>();

        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var groupName = "group-name";
        var sensorName = "sensor-name-1";
        var timestamp = ZonedDateTime.parse("2021-01-01T00:00:00Z");

        List<RawData> input = List.of(
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp, "type", 0, 20, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusMinutes(20), "type", 0, 11, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1), "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1).plusMinutes(20), "type", 0, 5, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(1).plusMinutes(40), "type", 0, 0, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2), "type", 0, 8, Duration.ZERO, Duration.ZERO),
                new ChargingStationRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusHours(2).plusMinutes(20), "type", 0, 3, Duration.ZERO, Duration.ZERO)
        );

        var function = new TimestampDifferenceAggregateFunction<>();
        function.apply(uuid, null, input, mockCollector);

        var result = mockCollector.getResult();
        assertEquals(
                result,
                new TimestampDifferenceResult(
                        Duration.ofHours(1),
                        Duration.ofHours(1).plusMinutes(20),
                        uuid
                )
        );

    }

}
