package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.apache.avro.generic.GenericRecord;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Optional;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class ChargingStationRawData extends RawData {
    private String vehicleType;
    private double batteryLevel;
    private double kwhSupplied;
    private Duration remainingChargeTime;
    private Duration elapsedTime;

    public ChargingStationRawData(String sensorUuid, String sensorName, String groupName, double latitude, double longitude, ZonedDateTime timestamp, String vehicleType, double batteryLevel, double kwhSupplied, Duration remainingChargeTime, Duration elapsedTime) {
        super(sensorUuid, sensorName, groupName, latitude, longitude, timestamp);
        this.vehicleType = vehicleType;
        this.batteryLevel = batteryLevel;
        this.kwhSupplied = kwhSupplied;
        this.remainingChargeTime = remainingChargeTime;
        this.elapsedTime = elapsedTime;
    }

    public static ChargingStationRawData fromGenericRecord(GenericRecord record) {
        return new ChargingStationRawData(
                UUID.fromString(record.get("sensor_uuid").toString()).toString(),
                record.get("sensor_name").toString(),
                Optional.ofNullable(record.get("group_name")).map(Object::toString).orElse(null),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                ZonedDateTime.parse(record.get("timestamp").toString(), DateTimeFormatter.ISO_OFFSET_DATE_TIME),
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
