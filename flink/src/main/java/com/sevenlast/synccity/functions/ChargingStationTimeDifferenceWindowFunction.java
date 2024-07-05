package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ChargingStationRawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;

import java.util.UUID;


public class ChargingStationTimeDifferenceWindowFunction extends TimeDifferenceWindowFunction<ChargingStationRawData>
        implements WindowFunction<ChargingStationRawData, TimestampDifferenceResult, String, TimeWindow> {

    @Override
    protected boolean isOccupied(ChargingStationRawData data) {
        return data.getKwhSupplied() <= 0;
    }
}
