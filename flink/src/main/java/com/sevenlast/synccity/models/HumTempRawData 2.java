package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.time.LocalDateTime;

@Data
@EqualsAndHashCode(callSuper = true)
@AllArgsConstructor
public class HumTempRawData extends RawData {
    private final float value;

    public HumTempRawData(String sensorUuid, String sensorName, String groupName, double latitude, double longitude, LocalDateTime timestamp, float value) {
        super(sensorUuid, sensorName, groupName, latitude, longitude, timestamp);
        this.value = value;
    }
}
