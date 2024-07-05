package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.typeinfo.TypeInfo;

import java.time.ZonedDateTime;
import java.util.Optional;
import java.util.UUID;

@Data
@AllArgsConstructor
public class HumTempRawData {
    private final UUID sensorUuid;
    private final String sensorName;
    private final String groupName;
    private final double latitude;
    private final double longitude;
    private final ZonedDateTime timestamp;
    private final float value;

    public static HumTempRawData fromGenericRecord(GenericRecord record) {
        return new HumTempRawData(
                UUID.fromString(record.get("sensor_uuid").toString()),
                record.get("sensor_name").toString(),
                Optional.ofNullable(record.get("group_name")).map(Object::toString).orElse(null),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                ZonedDateTime.parse(record.get("timestamp").toString()),
                (float) record.get("value")
        );
    }
}
