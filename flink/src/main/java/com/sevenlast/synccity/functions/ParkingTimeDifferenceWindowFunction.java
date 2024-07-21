package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ParkingRawData;


public class ParkingTimeDifferenceWindowFunction extends TimeDifferenceWindowFunction<ParkingRawData> {
    @Override
    protected boolean isOccupied(ParkingRawData data) {
        return data.isOccupied();
    }
}
