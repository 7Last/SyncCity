package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.ResultTuple;
import org.apache.flink.api.common.accumulators.AverageAccumulator;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;

public class AverageWindowFunction implements WindowFunction<RawData, ResultTuple, String, TimeWindow> {

    @Override
    public void apply(String key, TimeWindow window, Iterable<RawData> input, Collector<ResultTuple> out) {
        var accumulator = new AverageAccumulator();
        input.forEach(data -> accumulator.add(data.getValue()));
        var timestamp = ZonedDateTime.ofInstant(Instant.ofEpochMilli(window.getStart()), ZoneOffset.UTC);
        out.collect(new ResultTuple(key, accumulator.getLocalValue(), timestamp));
    }
}
