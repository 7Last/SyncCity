package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.HumTempRawData;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.functions.MapFunction;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

public class HumTempRawDataMapFunction implements MapFunction<GenericRecord, HumTempRawData> {
    @Override
    public HumTempRawData map(GenericRecord record) {
        return new HumTempRawData(
                UUID.fromString(record.get("sensor_uuid").toString()).toString(),
                record.get("sensor_name").toString(),
                Optional.ofNullable(record.get("group_name")).map(Object::toString).orElse(null),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                LocalDateTime.parse(record.get("timestamp").toString()),
                (float) record.get("value")
        );
    }
}
