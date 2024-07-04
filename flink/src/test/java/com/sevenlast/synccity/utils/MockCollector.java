package com.sevenlast.synccity.utils;

import lombok.Getter;
import org.apache.flink.util.Collector;

@Getter
public class MockCollector<T> implements Collector<T> {
    private T result;

    @Override
    public void collect(T t) {
        result = t;
    }

    @Override
    public void close() {
    }

}
