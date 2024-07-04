package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.avro.generic.GenericRecord;

import java.time.ZonedDateTime;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Supplier;

@Data
@AllArgsConstructor
@NoArgsConstructor(force = true)
public abstract class RawData implements Supplier<Boolean> {
    private UUID sensorUuid;
    private String sensorName;
    private String groupName;
    private double latitude;
    private double longitude;
    private ZonedDateTime timestamp;
}
