package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;


public class TimestampDifferenceAggregateFunctionTest {
    @Test
    public void testSingleSensor() {
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
}
