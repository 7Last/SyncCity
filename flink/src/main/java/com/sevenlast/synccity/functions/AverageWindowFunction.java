package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.HumTempRawData;
import com.sevenlast.synccity.models.SensorLocation;
import com.sevenlast.synccity.models.results.AverageResult;
import org.apache.flink.api.common.accumulators.AverageAccumulator;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.HashSet;

public class AverageWindowFunction implements WindowFunction<HumTempRawData, AverageResult, String, TimeWindow> {

    @Override
    public void apply(String groupName, TimeWindow window, Iterable<HumTempRawData> input, Collector<AverageResult> out) {
        var accumulator = new AverageAccumulator();
        var sensors = new HashSet<SensorLocation>();
        input.forEach(data -> {
            accumulator.add(data.getValue());
            sensors.add(new SensorLocation(data.getSensorName(), data.getLatitude(), data.getLongitude()));
        });
        var timestamp = LocalDateTime.ofInstant(Instant.ofEpochMilli(window.getEnd()), ZoneId.systemDefault());
        out.collect(new AverageResult(groupName, sensors, accumulator.getLocalValue(), timestamp));
    }
}
