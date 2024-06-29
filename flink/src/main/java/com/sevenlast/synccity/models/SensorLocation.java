package com.sevenlast.synccity.models;

import lombok.Data;

@Data
public class SensorLocation {
    private final String sensorName;
    private final double latitude;
    private final double longitude;
}
