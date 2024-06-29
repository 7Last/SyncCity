package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.AverageResult;
import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.SensorLocation;
import org.apache.flink.api.common.accumulators.AverageAccumulator;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.time.Instant;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.HashSet;

public class AverageWindowFunction implements WindowFunction<RawData, AverageResult, String, TimeWindow> {

    @Override
    public void apply(String groupName, TimeWindow window, Iterable<RawData> input, Collector<AverageResult> out) {
        var accumulator = new AverageAccumulator();
        var sensors = new HashSet<SensorLocation>();
        input.forEach(data -> {
            accumulator.add(data.getValue());
            sensors.add(new SensorLocation(data.getSensorName(), data.getLatitude(), data.getLongitude()));
        });
        var timestamp = ZonedDateTime.ofInstant(Instant.ofEpochMilli(window.getStart()), ZoneOffset.UTC);
        out.collect(new AverageResult(groupName, sensors, accumulator.getLocalValue(), timestamp));
    }
}