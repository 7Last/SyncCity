package com.sevenlast.synccity.models.results;

import com.sevenlast.synccity.serialization.RecordSerializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class ChargingEfficiencyResult implements RecordSerializable {
    // utilization rate is the ratio of the time the charging station
    // is used by a vehicle to the total time considered
    private double utilizationRate;

    // efficiency rate is the ratio of the time the charging station is
    // used by a vehicle to the total time the parking space is occupied
    private double efficiencyRate;

    private String sensorUuid;

    private LocalDateTime timestamp;

    public GenericRecord toGenericRecord(Schema schema) {
        GenericRecord record = new GenericData.Record(schema);
        record.put("utilization_rate", utilizationRate);
        record.put("efficiency_rate", efficiencyRate);
        record.put("sensor_uuid", sensorUuid);
        return record;
    }

    public static ChargingEfficiencyResult zero(String sensorUuid, LocalDateTime timestamp) {
        return new ChargingEfficiencyResult(0, 0, sensorUuid, timestamp);
    }
}
