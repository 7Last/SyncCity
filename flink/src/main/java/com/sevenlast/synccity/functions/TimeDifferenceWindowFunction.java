package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.Set;
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

        var sensorNames = new HashSet<String>();
        // calculate all the differences for each sensor uuid and then return a unified result
        LocalDateTime sensorPreviousTimestamp = null;
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
            sensorNames.add(data.getSensorName());
        }

        var timestamp = LocalDateTime.ofInstant(Instant.ofEpochMilli(window.getStart()), ZoneId.of("UTC"));
        var groupName = sortedInput.get(0).getGroupName();

        out.collect(
                new TimestampDifferenceResult(
                occupied,
                notOccupied,
                uuid,
                timestamp,
                groupName,
                sensorNames
        ));
    }
}
