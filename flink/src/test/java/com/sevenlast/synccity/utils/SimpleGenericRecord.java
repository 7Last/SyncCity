package com.sevenlast.synccity.utils;

import lombok.Getter;
import lombok.Setter;
import org.apache.avro.generic.GenericRecord;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

public class SimpleGenericRecord implements GenericRecord, Serializable {
    private final Map<String, Object> values = new HashMap<>();

    @Override
    public void put(String key, Object v) {
        values.put(key, v);
    }

    @Override
    public Object get(String key) {
        return values.get(key);
    }

    @Override
    public void put(int i, Object v) {
        throw new UnsupportedOperationException();
    }

    @Override
    public Object get(int i) {
        throw new UnsupportedOperationException();
    }

    @Override
    public org.apache.avro.Schema getSchema() {
        throw new UnsupportedOperationException();
    }
}
