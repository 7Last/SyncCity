package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.generic.GenericRecord;

import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.util.UUID;

@Data
@AllArgsConstructor
public class TemperatureRawData {
    private final UUID sensorUuid;
    private final String sensorName;
    private final double latitude;
    private final double longitude;
    private final ZonedDateTime timestamp;
    private final double value;

    public static TemperatureRawData fromGenericRecord(GenericRecord record) {
        return new TemperatureRawData(
                UUID.fromString(record.get("sensorUuid").toString()),
                record.get("sensorName").toString(),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                ZonedDateTime.parse(record.get("timestamp").toString()),
                (double) record.get("value")
        );
    }
}
