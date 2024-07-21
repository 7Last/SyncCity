package com.sevenlast.synccity.models.results;

import com.sevenlast.synccity.models.SensorLocation;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.Set;

@Data
@AllArgsConstructor
public class AverageResult {
    private String groupName;
    private Set<SensorLocation> sensors;
    private double value;
    private LocalDateTime windowStart;
}
