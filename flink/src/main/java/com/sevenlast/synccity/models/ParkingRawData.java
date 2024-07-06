package com.sevenlast.synccity.models;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.apache.avro.generic.GenericRecord;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class ParkingRawData extends RawData {
    private boolean isOccupied;

    public ParkingRawData(String sensorUuid, String sensorName, String groupName, double latitude, double longitude, LocalDateTime timestamp, boolean isOccupied) {
        super(sensorUuid, sensorName, groupName, latitude, longitude, timestamp);
        this.isOccupied = isOccupied;
    }

    public static ParkingRawData fromGenericRecord(GenericRecord record) {
        return new ParkingRawData(
                UUID.fromString(record.get("sensor_uuid").toString()).toString(),
                record.get("sensor_name").toString(),
                Optional.ofNullable(record.get("group_name")).map(Object::toString).orElse(null),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                LocalDateTime.parse(record.get("timestamp").toString()),
                (boolean) record.get("is_occupied")
        );
    }
}
