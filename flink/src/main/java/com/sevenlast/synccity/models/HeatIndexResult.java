package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Set;

@Data
@AllArgsConstructor
public class HeatIndexResult {
    private Set<String> sensorNames;
    private String groupName;
    private double heatIndex;
    private double averageTemperature;
    private double averageHumidity;
    private ZonedDateTime windowStart;

    public GenericRecord toGenericRecord(Schema schema) {
        GenericRecord record = new GenericData.Record(schema);
        record.put("group_name", groupName);
        record.put("sensor_names", sensorNames);
        record.put("heat_index", heatIndex);
        record.put("avg_temperature", averageTemperature);
        record.put("avg_humidity", averageHumidity);
        record.put("timestamp", windowStart.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME));
        return record;
    }
}
