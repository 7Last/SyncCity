package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Comparator;
import java.util.UUID;
import java.util.stream.StreamSupport;


public class TimestampDifferenceAggregateFunction<T extends RawData> implements WindowFunction<T, TimestampDifferenceResult, UUID, TimeWindow> {

    @Override
    public void apply(UUID uuid, TimeWindow window, Iterable<T> input, Collector<TimestampDifferenceResult> out) {
        Duration occupied = Duration.ZERO;
        Duration notOccupied = Duration.ZERO;

        var sortedInput = StreamSupport.stream(input.spliterator(), false)
                .sorted(Comparator.comparing(RawData::getTimestamp))
                .toList();

        // calculate all the differences for each sensor uuid and then return a unified result
        ZonedDateTime sensorPreviousTimestamp = null;
        for (RawData data : sortedInput) {
            if (sensorPreviousTimestamp != null) {
                Duration difference = Duration.between(sensorPreviousTimestamp, data.getTimestamp());
                if (data.get()) {
                    notOccupied = notOccupied.plus(difference);
                } else {
                    occupied = occupied.plus(difference);
                }
            }
            sensorPreviousTimestamp = data.getTimestamp();
        }
        out.collect(new TimestampDifferenceResult(occupied, notOccupied, uuid));
    }
}
