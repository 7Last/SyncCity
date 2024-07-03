package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.RawData;
import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.io.IOException;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Comparator;
import java.util.stream.StreamSupport;


public class TimestampDifferenceAggregateFunction<T extends RawData> implements WindowFunction<RawData, Tuple2<Boolean, Duration>, String, TimeWindow> {

    @Override
    public void apply(String groupName, TimeWindow window, Iterable<RawData> input, Collector<Tuple2<Boolean, Duration>> out) {
        Duration occupied = Duration.ZERO;
        Duration notOccupied = Duration.ZERO;
        ZonedDateTime previousTimestamp = null;

        var sortedInput = StreamSupport.stream(input.spliterator(), false)
                .sorted(Comparator.comparing(RawData::getTimestamp))
                .toList();

        for (RawData data : sortedInput) {
            if (previousTimestamp != null) {
                Duration difference = Duration.between(previousTimestamp, data.getTimestamp());
                if (data.get()) {
                    notOccupied = notOccupied.plus(difference);
                } else {
                    occupied = occupied.plus(difference);
                }
            }
            previousTimestamp = data.getTimestamp();
        }
        out.collect(new Tuple2<>(true, occupied));
        out.collect(new Tuple2<>(false, notOccupied));
    }
}
