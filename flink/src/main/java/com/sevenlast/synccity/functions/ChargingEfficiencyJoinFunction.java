package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.api.common.functions.JoinFunction;

import java.util.HashSet;

import static java.lang.Math.min;

public class ChargingEfficiencyJoinFunction implements JoinFunction<TimestampDifferenceResult, TimestampDifferenceResult, ChargingEfficiencyResult> {

    @Override
    public ChargingEfficiencyResult join(TimestampDifferenceResult parkingDiff, TimestampDifferenceResult chargingDiff) {
        var parkingOccupied = parkingDiff.getOccupiedDuration();
        var totalSeconds = parkingOccupied.plus(parkingDiff.getNotOccupiedDuration()).toSeconds();
        var sensorNames = new HashSet<>(parkingDiff.getSensorNames());
        sensorNames.addAll(chargingDiff.getSensorNames());

        if (totalSeconds == 0 || parkingOccupied.isZero()) {
            // The stream is keyed by sensor UUID, taking parkingDiff sensor UUID
            return ChargingEfficiencyResult.zero(
                    parkingDiff.getSensorUuid(),
                    parkingDiff.getTimestamp(),
                    parkingDiff.getGroupName(),
                    sensorNames
            );
        }

        var chargingOccupied = chargingDiff.getOccupiedDuration().toSeconds();
        var utilizationRate = (double) chargingOccupied / totalSeconds;

        if (chargingOccupied > parkingOccupied.toSeconds()) {
            chargingOccupied = parkingOccupied.toSeconds();
        }

        var efficiencyRate = (double) chargingOccupied / parkingOccupied.toSeconds();
        return new ChargingEfficiencyResult(
                min(1, utilizationRate),
                min(1, efficiencyRate),
                parkingDiff.getSensorUuid(),
                parkingDiff.getTimestamp(),
                parkingDiff.getGroupName(),
                sensorNames
        );
    }
}
