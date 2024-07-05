package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.typeinfo.TypeInfo;

import java.time.ZonedDateTime;
import java.util.Optional;
import java.util.UUID;

@Data
@EqualsAndHashCode(callSuper = true)
@AllArgsConstructor
public class HumTempRawData extends RawData {
    private final float value;

    public HumTempRawData(String sensorUuid, String sensorName, String groupName, double latitude, double longitude, ZonedDateTime timestamp, float value) {
        super(sensorUuid, sensorName, groupName, latitude, longitude, timestamp);
        this.value = value;
    }

    public static HumTempRawData fromGenericRecord(GenericRecord record) {
        return new HumTempRawData(
                UUID.fromString(record.get("sensor_uuid").toString()).toString(),
                record.get("sensor_name").toString(),
                Optional.ofNullable(record.get("group_name")).map(Object::toString).orElse(null),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                ZonedDateTime.parse(record.get("timestamp").toString()),
                (float) record.get("value")
        );
    }
}
