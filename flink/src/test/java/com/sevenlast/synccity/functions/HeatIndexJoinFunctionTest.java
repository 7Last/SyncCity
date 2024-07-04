package com.sevenlast.synccity.functions;

import com.google.common.collect.Sets;
import com.sevenlast.synccity.models.SensorLocation;
import com.sevenlast.synccity.models.results.AverageResult;
import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.models.results.HeatIndexResult;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.HashSet;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class HeatIndexJoinFunctionTest {
    @Test
    public void testHeatIndexCalculation() {
        var groupName = "group-name";
        var dateTime = ZonedDateTime.parse("2021-01-01T00:00:00Z");
        var averageTemperature = new AverageResult(
                groupName,
                Sets.newHashSet(
                        new SensorLocation("temperature-1", 10, 10),
                        new SensorLocation("temperature-2", -10, -10)
                ),
                25,
                dateTime
        );

        var averageHumidity = new AverageResult(
                groupName,
                Set.of(
                        new SensorLocation("humidity-1", 20, 10),
                        new SensorLocation("humidity-2", -10, -20)
                ),
                50,
                dateTime
        );

        var function = new HeatIndexJoinFunction();
        var result = function.join(averageTemperature, averageHumidity);

        var expected = new HeatIndexResult(
                Sets.newHashSet(
                        "temperature-1",
                        "temperature-2",
                        "humidity-1",
                        "humidity-2"
                ),
                groupName,
                25.88890924444001,
                25.0,
                50.0,
                2.5,
                -2.5,
                2384.74025022510930,
                dateTime
        );

        // unordered equals for sets
        assertEquals(expected.getSensorNames(), result.getSensorNames());
        assertEquals(expected.getGroupName(), result.getGroupName());
        assertEquals(expected.getHeatIndex(), result.getHeatIndex());
        assertEquals(expected.getAverageTemperature(), result.getAverageTemperature());
        assertEquals(expected.getAverageHumidity(), result.getAverageHumidity());
        assertEquals(expected.getCenterOfMassLatitude(), result.getCenterOfMassLatitude());
        assertEquals(expected.getCenterOfMassLongitude(), result.getCenterOfMassLongitude());
        assertEquals(expected.getRadius(), result.getRadius());
        assertEquals(expected.getWindowStart(), result.getWindowStart());

    }
}
