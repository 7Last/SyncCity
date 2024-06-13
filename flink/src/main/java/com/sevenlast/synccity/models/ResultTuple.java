package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.generic.GenericRecordBuilder;
import org.apache.avro.Schema;

import java.time.ZonedDateTime;

@Data
@AllArgsConstructor
public class ResultTuple {
    private String key;
    private double value;
    private ZonedDateTime windowStart;

    public GenericRecord toGenericRecord(Schema schema) {
        GenericRecord record = new GenericData.Record(schema);
        record.put("group_name", key);
        record.put("value", value);
        record.put("timestamp", windowStart.toString());
        return record;
    }
}
