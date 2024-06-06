package com.sevenlast.synccity;

import org.apache.flink.api.common.accumulators.AverageAccumulator;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.time.LocalDateTime;
import java.time.ZoneOffset;

public class AverageWindowFunction implements WindowFunction<SensorData, Tuple3<String, LocalDateTime, Double>, String, TimeWindow> {

    @Override
    public void apply(String key, TimeWindow window, Iterable<SensorData> input, Collector<Tuple3<String, LocalDateTime, Double>> out) {
        var accumulator = new AverageAccumulator();
        input.forEach(data -> accumulator.add(data.getTemperature()));

        var timestamp = LocalDateTime.ofEpochSecond(window.getStart() / 1000, 0, ZoneOffset.UTC);
        out.collect(new Tuple3<>(key, timestamp, accumulator.getLocalValue()));
    }
}
