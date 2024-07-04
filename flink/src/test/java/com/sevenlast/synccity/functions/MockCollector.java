package com.sevenlast.synccity.functions;

import org.apache.flink.util.Collector;

public class MockCollector<T> implements Collector<T> {
    private T result;

    @Override
    public void collect(T t) {
        result = t;
    }

    @Override
    public void close() {
    }

    public T getResult() {
        return result;
    }
}
