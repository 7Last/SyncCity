package com.sevenlast.synccity.serialization;

import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;

import java.time.format.DateTimeFormatter;

@Getter
@AllArgsConstructor
public class ChargingEfficiencyRecordSerializableAdapter implements RecordSerializable {
    private final ChargingEfficiencyResult adaptee;

    @Override
    public GenericRecord toGenericRecord(Schema schema) {
        GenericRecord record = new GenericData.Record(schema);
        record.put("utilization_rate", adaptee.getUtilizationRate());
        record.put("efficiency_rate", adaptee.getEfficiencyRate());
        record.put("sensor_uuid", adaptee.getSensorUuid());
        record.put("timestamp", adaptee.getTimestamp().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        record.put("group_name", adaptee.getGroupName());
        record.put("sensor_names", adaptee.getSensorNames());
        return record;
    }
}
