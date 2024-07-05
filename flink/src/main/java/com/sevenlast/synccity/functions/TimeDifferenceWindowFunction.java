package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Comparator;
import java.util.stream.StreamSupport;


public abstract class TimeDifferenceWindowFunction<T extends RawData>
        implements WindowFunction<T, TimestampDifferenceResult, String, TimeWindow> {
    protected abstract boolean isOccupied(T data);

    public void apply(String uuid, TimeWindow window, Iterable<T> input, org.apache.flink.util.Collector<TimestampDifferenceResult> out) {

        Duration occupied = Duration.ZERO;
        Duration notOccupied = Duration.ZERO;

        var sortedInput = StreamSupport.stream(input.spliterator(), false)
                .sorted(Comparator.comparing(RawData::getTimestamp))
                .toList();

        // calculate all the differences for each sensor uuid and then return a unified result
        ZonedDateTime sensorPreviousTimestamp = null;
        for (T data : sortedInput) {
            if (sensorPreviousTimestamp != null) {
                Duration difference = Duration.between(sensorPreviousTimestamp, data.getTimestamp());
                if (isOccupied(data)) {
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
