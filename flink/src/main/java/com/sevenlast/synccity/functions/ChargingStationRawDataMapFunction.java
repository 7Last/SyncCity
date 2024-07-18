package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.ChargingStationRawData;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.functions.MapFunction;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Optional;

public class ChargingStationRawDataMapFunction implements MapFunction<GenericRecord, ChargingStationRawData> {
    @Override
    public ChargingStationRawData map(GenericRecord record) {
        return new ChargingStationRawData(
                record.get("sensor_uuid").toString(),
                record.get("sensor_name").toString(),
                record.get("group_name").toString(),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                LocalDateTime.parse(record.get("timestamp").toString()),
                record.get("vehicle_type").toString(),
                Double.parseDouble(record.get("battery_level").toString()),
                Double.parseDouble(record.get("kwh_supplied").toString()),
                Optional.ofNullable(record.get("remaining_charge_time"))
                        .map((obj) -> Duration.ofSeconds(Long.parseLong(obj.toString())))
                        .orElse(null),
                Optional.ofNullable(record.get("elapsed_time"))
                        .map((obj) -> Duration.ofSeconds(Long.parseLong(obj.toString())))
                        .orElse(null)
        );
    }
}
