package com.sevenlast.synccity.models.results;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.Duration;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class TimestampDifferenceResult {
    private Duration occupiedDuration;
    private Duration notOccupiedDuration;
    private String sensorUuid;
    private LocalDateTime timestamp;
}
