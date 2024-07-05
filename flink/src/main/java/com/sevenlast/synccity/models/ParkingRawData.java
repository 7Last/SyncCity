package com.sevenlast.synccity.models;

import lombok.Data;
import lombok.EqualsAndHashCode;
import org.apache.avro.generic.GenericRecord;

import java.time.ZonedDateTime;
import java.util.Optional;
import java.util.UUID;

@Data
@EqualsAndHashCode(callSuper = true)
public class ParkingRawData extends RawData {
    private final boolean isOccupied;

    public ParkingRawData(UUID sensorUuid, String sensorName, String groupName, double latitude, double longitude, ZonedDateTime timestamp, boolean isOccupied) {
        super(sensorUuid, sensorName, groupName, latitude, longitude, timestamp);
        this.isOccupied = isOccupied;
    }

    public static ParkingRawData fromGenericRecord(GenericRecord record) {
        return new ParkingRawData(
                UUID.fromString(record.get("sensor_uuid").toString()),
                record.get("sensor_name").toString(),
                Optional.ofNullable(record.get("group_name")).map(Object::toString).orElse(null),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                ZonedDateTime.parse(record.get("timestamp").toString()),
                (boolean) record.get("is_occupied")
        );
    }

    @Override
    public Boolean get() {
        return isOccupied;
    }
}
