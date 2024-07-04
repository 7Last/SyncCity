package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.RawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.io.IOException;
import java.sql.Timestamp;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Comparator;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.StreamSupport;


public class TimestampDifferenceAggregateFunction<T extends RawData> implements WindowFunction<T, TimestampDifferenceResult, String, TimeWindow> {

    @Override
    public void apply(String groupName, TimeWindow window, Iterable<T> input, Collector<TimestampDifferenceResult> out) {
        Duration occupied = Duration.ZERO;
        Duration notOccupied = Duration.ZERO;
        final AtomicReference<ZonedDateTime> previousTimestamp = new AtomicReference<>(null);

        StreamSupport.stream(input.spliterator(), false)
                .sorted(Comparator.comparing(RawData::getTimestamp))
                .reduce(new TimestampDifferenceResult(occupied, notOccupied, groupName), (acc, data) -> {
                    if (previousTimestamp.get() != null) {
                        Duration difference = Duration.between(previousTimestamp.get(), data.getTimestamp());
                        if (data.get()) {
                            acc.setOccupiedDuration(acc.getOccupiedDuration().plus(difference));
                        } else {
                            acc.setNotOccupiedDuration(acc.getNotOccupiedDuration().plus(difference));
                        }
                    }
                    previousTimestamp.set(data.getTimestamp());
                    return acc;
                }, (acc1, acc2) -> {
                    acc1.setOccupiedDuration(acc1.getOccupiedDuration().plus(acc2.getOccupiedDuration()));
                    acc1.setNotOccupiedDuration(acc1.getNotOccupiedDuration().plus(acc2.getNotOccupiedDuration()));
                    return acc1;
                })
                .forEach(out::collect);

//        for (RawData data : sortedInput) {
//            if (previousTimestamp != null) {
//                Duration difference = Duration.between(previousTimestamp, data.getTimestamp());
//                if (data.get()) {
//                    notOccupied = notOccupied.plus(difference);
//                } else {
//                    occupied = occupied.plus(difference);
//                }
//            }
//            previousTimestamp = data.getTimestamp();
//        }
        out.collect(new TimestampDifferenceResult(occupied, notOccupied, groupName));
    }
}
