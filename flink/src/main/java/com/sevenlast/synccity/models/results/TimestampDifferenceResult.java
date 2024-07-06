package com.sevenlast.synccity.models.results;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Set;

@Data
@AllArgsConstructor
public class TimestampDifferenceResult {
    private Duration occupiedDuration;
    private Duration notOccupiedDuration;
    private String sensorUuid;
    private LocalDateTime timestamp;
    private String groupName;
    private Set<String> sensorNames;
}
