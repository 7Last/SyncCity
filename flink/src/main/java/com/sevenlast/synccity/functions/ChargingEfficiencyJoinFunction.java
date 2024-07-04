package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import com.sevenlast.synccity.serialization.RecordSerializable;
import org.apache.flink.api.common.functions.JoinFunction;

public class ChargingEfficiencyJoinFunction implements JoinFunction<TimestampDifferenceResult, TimestampDifferenceResult, RecordSerializable> {

    @Override
    public RecordSerializable join(TimestampDifferenceResult parkingDiff, TimestampDifferenceResult chargingDiff) throws Exception {
        var parkingOccupied = parkingDiff.getOccupiedDuration();
        var totalSeconds = parkingOccupied.plus(parkingDiff.getNotOccupiedDuration()).toSeconds();

        var utilizationRate = chargingDiff.getOccupiedDuration().toSeconds() / totalSeconds;
        var efficiencyRate = chargingDiff.getNotOccupiedDuration().toSeconds() / parkingOccupied.toSeconds();
        return new ChargingEfficiencyResult(utilizationRate, efficiencyRate);
    }
}
