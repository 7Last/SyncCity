package com.sevenlast.synccity.utils;

import org.apache.flink.streaming.api.functions.sink.SinkFunction;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CollectionSink<T> implements SinkFunction<T> {
    public static final List<Object> values = Collections.synchronizedList(new ArrayList<>());

    @Override
    public void invoke(T result, SinkFunction.Context context) {
        values.add(result);
    }
}
