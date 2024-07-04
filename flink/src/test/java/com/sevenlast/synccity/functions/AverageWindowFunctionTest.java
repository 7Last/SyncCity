package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.HumTempRawData;
import com.sevenlast.synccity.models.results.AverageResult;
import org.apache.flink.runtime.operators.chaining.ChainedDriver;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.junit.jupiter.api.Test;

import java.time.ZonedDateTime;
import java.util.List;
import java.util.UUID;

import static org.apache.flink.runtime.metrics.groups.InternalSourceReaderMetricGroup.mock;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class AverageWindowFunctionTest {
    @Test
    public void testAverageCalculation() {
        var function = new AverageWindowFunction();

        var guid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var sensorName = "sensor-name";
        var groupName = "group-name";
        var timestamp = ZonedDateTime.parse("2021-01-01T00:00:00Z");

        var data = List.of(
                new HumTempRawData(guid, sensorName, groupName, 0, 0, timestamp, 10),
                new HumTempRawData(guid, sensorName, groupName, 0, 0, timestamp.plusMinutes(1), 20),
                new HumTempRawData(guid, sensorName, groupName, 0, 0, timestamp.plusMinutes(2), 30),
                new HumTempRawData(guid, sensorName, groupName, 0, 0, timestamp.plusMinutes(3), 25)
        );

        var mockCollector = new Collector<AverageResult>() {
            private AverageResult result;
            @Override
            public void collect(AverageResult averageResult) {
                result = averageResult;
            }

            @Override
            public void close() {}
        };

        var timeWindow = new TimeWindow(timestamp.toEpochSecond(), timestamp.plusHours(1).toEpochSecond());

        function.apply(groupName, timeWindow, data, mockCollector);
        assertEquals(21.25, mockCollector.result.getValue());
    }
}
