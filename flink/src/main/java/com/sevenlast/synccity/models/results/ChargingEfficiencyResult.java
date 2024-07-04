package com.sevenlast.synccity.models.results;

import com.sevenlast.synccity.serialization.RecordSerializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;

@Data
@AllArgsConstructor
public class ChargingEfficiencyResult implements RecordSerializable {
    // utilization rate is the ratio of the time the charging station
    // is used by a vehicle to the total time considered
    private double utilizationRate;

    // efficiency rate is the ratio of the time the charging station is
    // used by a vehicle to the total time the parking space is occupied
    private double efficiencyRate;

    @Override
    public GenericRecord toGenericRecord(Schema schema) {
        return null;
    }

    public static ChargingEfficiencyResult zero() {
        return new ChargingEfficiencyResult(0, 0);
    }
}
