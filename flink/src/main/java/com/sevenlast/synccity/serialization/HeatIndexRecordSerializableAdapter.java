package com.sevenlast.synccity.serialization;

import com.sevenlast.synccity.models.results.HeatIndexResult;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;

import java.time.format.DateTimeFormatter;

@Getter
@AllArgsConstructor
public class HeatIndexRecordSerializableAdapter implements RecordSerializable {
    private final HeatIndexResult adaptee;

    @Override
    public GenericRecord toGenericRecord(Schema schema) {
        GenericRecord record = new GenericData.Record(schema);
        record.put("sensor_names", adaptee.getSensorNames());
        record.put("group_name", adaptee.getGroupName());
        record.put("heat_index", adaptee.getHeatIndex());
        record.put("avg_temperature", adaptee.getAverageTemperature());
        record.put("avg_humidity", adaptee.getAverageHumidity());
        record.put("center_of_mass_latitude", adaptee.getCenterOfMassLatitude());
        record.put("center_of_mass_longitude", adaptee.getCenterOfMassLongitude());
        record.put("radius_in_km", adaptee.getRadius());
        record.put("timestamp", adaptee.getWindowStart().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        return record;

    }
}
