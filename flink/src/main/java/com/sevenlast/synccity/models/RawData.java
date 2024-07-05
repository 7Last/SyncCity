package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.ZonedDateTime;
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
