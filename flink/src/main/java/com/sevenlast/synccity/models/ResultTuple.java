package com.sevenlast.synccity.models;

import org.apache.avro.generic.GenericRecord;
import org.apache.avro.generic.GenericRecordBuilder;
import org.apache.avro.Schema;

import java.time.ZonedDateTime;

public record ResultTuple(String key, double value, ZonedDateTime windowStart) {
    public GenericRecord toGenericRecord(Schema schema) {
        return new GenericRecordBuilder(schema)
                .set("group_name", key)
                .set("value", value)
                .set("timestamp", windowStart.toString())
                .build();
    }
}
