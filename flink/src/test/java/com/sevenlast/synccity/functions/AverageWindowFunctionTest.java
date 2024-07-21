package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.HumTempRawData;
import com.sevenlast.synccity.models.results.AverageResult;
import com.sevenlast.synccity.utils.MockCollector;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class AverageWindowFunctionTest {
    @Test
    public void testAverageCalculation() {
        var function = new AverageWindowFunction();

        var uuid = "00000000-0000-0000-0000-000000000000";
        var sensorName = "sensor-name";
        var groupName = "group-name";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var data = List.of(
                new HumTempRawData(uuid, sensorName, groupName, 0, 0, timestamp, 10),
                new HumTempRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusMinutes(1), 20),
                new HumTempRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusMinutes(2), 30),
                new HumTempRawData(uuid, sensorName, groupName, 0, 0, timestamp.plusMinutes(3), 25)
        );

        var mockCollector = new MockCollector<AverageResult>();
        var timeWindow = new TimeWindow(0, 0);
        function.apply(groupName, timeWindow, data, mockCollector);
        assertEquals(21.25, mockCollector.getResult().getValue());
    }
}
