package com.sevenlast.synccity.models.results;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.Set;

@Data
@AllArgsConstructor
public class HeatIndexResult {
    private Set<String> sensorNames;
    private String groupName;
    private double heatIndex;
    private double averageTemperature;
    private double averageHumidity;
    private double centerOfMassLatitude;
    private double centerOfMassLongitude;
    private double radius;
    private LocalDateTime windowStart;
}
