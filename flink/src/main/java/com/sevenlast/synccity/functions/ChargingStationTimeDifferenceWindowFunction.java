package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ChargingStationRawData;


public class ChargingStationTimeDifferenceWindowFunction extends TimeDifferenceWindowFunction<ChargingStationRawData> {
    @Override
    protected boolean isOccupied(ChargingStationRawData data) {
        return data.getKwhSupplied() <= 0;
    }
}
