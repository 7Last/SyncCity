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
public class HeatIndexResult implements RecordSerializable {
    private Set<String> sensorNames;
    private String groupName;
    private double heatIndex;
    private double averageTemperature;
    private double averageHumidity;
    private double centerOfMassLatitude;
    private double centerOfMassLongitude;
    private double radius;
    private LocalDateTime windowStart;

    public GenericRecord toGenericRecord(Schema schema) {
        GenericRecord record = new GenericData.Record(schema);
        record.put("sensor_names", sensorNames);
        record.put("group_name", groupName);
        record.put("heat_index", heatIndex);
        record.put("avg_temperature", averageTemperature);
        record.put("avg_humidity", averageHumidity);
        record.put("center_of_mass_latitude", centerOfMassLatitude);
        record.put("center_of_mass_longitude", centerOfMassLongitude);
        record.put("radius_in_km", radius);
        record.put("timestamp", windowStart.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        return record;
    }
}
