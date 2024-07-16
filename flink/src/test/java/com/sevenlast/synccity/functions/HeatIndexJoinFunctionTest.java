package com.sevenlast.synccity.functions;

import com.google.common.collect.Sets;
import com.sevenlast.synccity.models.SensorLocation;
import com.sevenlast.synccity.models.results.AverageResult;
import com.sevenlast.synccity.models.results.HeatIndexResult;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class HeatIndexJoinFunctionTest {
    @Test
    public void testHeatIndexCalculation() {
        var groupName = "group-name";
        var dateTime = LocalDateTime.parse("2021-01-01T00:00:00");
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
                2.540697329480218,
                -2.622949155866025,
                2376.3602040235223,
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
