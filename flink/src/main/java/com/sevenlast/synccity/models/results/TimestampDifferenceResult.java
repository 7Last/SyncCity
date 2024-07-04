package com.sevenlast.synccity.models.results;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.flink.api.java.tuple.Tuple2;

import java.time.Duration;

@Data
@AllArgsConstructor
public class TimestampDifferenceResult {
    private Duration occupiedDuration;
    private Duration notOccupiedDuration;
    private String groupName;
}
