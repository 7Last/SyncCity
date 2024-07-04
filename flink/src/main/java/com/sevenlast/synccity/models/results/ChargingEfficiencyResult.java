package com.sevenlast.synccity.models.results;

import com.sevenlast.synccity.serialization.RecordSerializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;

@Data
@AllArgsConstructor
public class ChargingEfficiencyResult implements RecordSerializable {
    private long utilizationRate;
    private long efficiencyRate;

    @Override
    public GenericRecord toGenericRecord(Schema schema) {
        return null;
    }
}
