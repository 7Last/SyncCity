package com.sevenlast.synccity.models.results;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.time.Duration;
import java.util.UUID;

@Data
@AllArgsConstructor
public class TimestampDifferenceResult {
    private Duration occupiedDuration;
    private Duration notOccupiedDuration;
    private UUID sensorUuid;
}
