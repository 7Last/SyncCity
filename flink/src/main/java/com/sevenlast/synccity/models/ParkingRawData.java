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

}
