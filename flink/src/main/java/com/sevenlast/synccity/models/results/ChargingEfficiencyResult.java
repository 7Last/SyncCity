package com.sevenlast.synccity.models.results;

import com.sevenlast.synccity.serialization.RecordSerializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Set;

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

    private String groupName;

    private Set<String> sensorNames;

    public GenericRecord toGenericRecord(Schema schema) {
        GenericRecord record = new GenericData.Record(schema);
        record.put("utilization_rate", utilizationRate);
        record.put("efficiency_rate", efficiencyRate);
        record.put("sensor_uuid", sensorUuid);
        record.put("timestamp", timestamp.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        record.put("group_name", groupName);
        record.put("sensor_names", sensorNames);
        return record;
    }

    public static ChargingEfficiencyResult zero(String sensorUuid, LocalDateTime timestamp, String groupName, Set<String> sensorNames) {
        return new ChargingEfficiencyResult(0, 0, sensorUuid, timestamp, groupName, sensorNames);
    }
}
