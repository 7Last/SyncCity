package com.sevenlast.synccity.serialization;

import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;

@FunctionalInterface
public interface RecordSerializable {
    GenericRecord toGenericRecord(Schema schema);
}
