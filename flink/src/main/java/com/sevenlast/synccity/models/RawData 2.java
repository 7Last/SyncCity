package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor(force = true)
public abstract class RawData {
    private String sensorUuid;
    private String sensorName;
    private String groupName;
    private double latitude;
    private double longitude;
    private LocalDateTime timestamp;
}
