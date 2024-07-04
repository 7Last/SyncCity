package com.sevenlast.synccity.functions;

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
