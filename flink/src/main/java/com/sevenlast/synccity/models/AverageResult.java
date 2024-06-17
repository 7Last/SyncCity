package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.ZonedDateTime;
import java.util.Set;

@Data
@AllArgsConstructor
public class AverageResult {
    private String groupName;
    private Set<SensorLocation> sensors;
    private double value;
    private ZonedDateTime windowStart;
}
