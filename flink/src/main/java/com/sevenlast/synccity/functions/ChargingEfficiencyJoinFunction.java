package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import com.sevenlast.synccity.serialization.RecordSerializable;
import com.sevenlast.synccity.serialization.RecordSerializationSchema;
import org.apache.flink.api.common.functions.JoinFunction;

public class ChargingEfficiencyJoinFunction implements JoinFunction<TimestampDifferenceResult, TimestampDifferenceResult, ChargingEfficiencyResult> {

    @Override
    public ChargingEfficiencyResult join(TimestampDifferenceResult parkingDiff, TimestampDifferenceResult chargingDiff) {
        var parkingOccupied = parkingDiff.getOccupiedDuration();
        var totalSeconds = parkingOccupied.plus(parkingDiff.getNotOccupiedDuration()).toSeconds();
        if (totalSeconds == 0) {
            return  ChargingEfficiencyResult.zero();
        }

        var chargingOccupied = chargingDiff.getOccupiedDuration().toSeconds();
        var utilizationRate = (double) chargingOccupied / totalSeconds;

        if (chargingOccupied > parkingOccupied.toSeconds()) {
            chargingOccupied = parkingOccupied.toSeconds();
        }

        var efficiencyRate = (double) chargingOccupied / parkingOccupied.toSeconds();
        return new ChargingEfficiencyResult(utilizationRate, efficiencyRate);
    }
}
