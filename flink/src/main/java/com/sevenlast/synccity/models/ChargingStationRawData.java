package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.apache.avro.generic.GenericRecord;

import java.time.Duration;
import java.time.LocalDateTime;
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

    public ChargingStationRawData(String sensorUuid, String sensorName, String groupName, double latitude, double longitude, LocalDateTime timestamp, String vehicleType, double batteryLevel, double kwhSupplied, Duration remainingChargeTime, Duration elapsedTime) {
        super(sensorUuid, sensorName, groupName, latitude, longitude, timestamp);
        this.vehicleType = vehicleType;
        this.batteryLevel = batteryLevel;
        this.kwhSupplied = kwhSupplied;
        this.remainingChargeTime = remainingChargeTime;
        this.elapsedTime = elapsedTime;
    }
}
