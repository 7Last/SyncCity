package com.sevenlast.synccity.utils;

import org.apache.flink.api.connector.sink2.Sink;
import org.apache.flink.api.connector.sink2.SinkWriter;
import org.apache.flink.api.connector.sink2.WriterInitContext;
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class MockCollectSink<T> implements SinkFunction<T> {
    public final List<T> values = Collections.synchronizedList(new ArrayList<>());

    @Override
    public void invoke(T value, Context context) {
        values.add(value);
    }
}
