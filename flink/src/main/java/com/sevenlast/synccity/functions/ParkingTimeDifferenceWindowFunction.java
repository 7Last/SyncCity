package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ParkingRawData;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;

import java.util.UUID;


public class ParkingTimeDifferenceWindowFunction
        extends TimeDifferenceWindowFunction<ParkingRawData>
        implements WindowFunction<ParkingRawData, TimestampDifferenceResult, String, TimeWindow> {

    @Override
    protected boolean isOccupied(ParkingRawData data) {
        return data.isOccupied();
    }
}
