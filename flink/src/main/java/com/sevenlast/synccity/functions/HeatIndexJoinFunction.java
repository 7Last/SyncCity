package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.SensorLocation;
import com.sevenlast.synccity.models.results.AverageResult;
import com.sevenlast.synccity.models.results.HeatIndexResult;
import com.sevenlast.synccity.serialization.RecordSerializable;
import org.apache.flink.api.common.functions.JoinFunction;
import org.apache.flink.api.java.tuple.Tuple2;

import java.util.stream.Collectors;

public class HeatIndexJoinFunction implements JoinFunction<AverageResult, AverageResult, RecordSerializable> {

    private static final double c1 = -8.78469475556;
    private static final double c2 = 1.61139411;
    private static final double c3 = 2.33854883889;
    private static final double c4 = -0.14611605;
    private static final double c5 = -0.012308094;
    private static final double c6 = -0.0164248277778;
    private static final double c7 = 2.211732e-3;
    private static final double c8 = 7.2546e-4;
    private static final double c9 = -3.582e-6;

    @Override
    public RecordSerializable join(AverageResult averageTemperature, AverageResult averageHumidity) throws Exception {
        double t = averageTemperature.getValue();
        double h = averageHumidity.getValue();

        double heatIndex = c1 + (c2 * t) + (c3 * h) + (c4 * t * h)
                + (c5 * t * t) + (c6 * h * h)
                + (c7 * t * t * h) + (c8 * t * h * h)
                + (c9 * t * t * h * h);

        var sensors = averageTemperature.getSensors();
        sensors.addAll(averageHumidity.getSensors());

        Tuple2<Double, Double> centerOfMass = sensors.stream()
                .map(sensor -> new Tuple2<>(sensor.getLatitude(), sensor.getLongitude()))
                .reduce((a, b) -> new Tuple2<>(a.f0 + b.f0, a.f1 + b.f1))
                .map(tuple -> new Tuple2<>(tuple.f0 / sensors.size(), tuple.f1 / sensors.size()))
                .orElseThrow();

        double maxRadius = sensors.stream()
                .map(sensor -> haversine(sensor.getLatitude(), sensor.getLongitude(), centerOfMass.f0, centerOfMass.f1))
                .max(Double::compareTo)
                .orElseThrow();

        return new HeatIndexResult(
                sensors.stream().map(SensorLocation::getSensorName).collect(Collectors.toSet()),
                averageTemperature.getGroupName(),
                heatIndex,
                averageTemperature.getValue(),
                averageHumidity.getValue(),
                centerOfMass.f0,
                centerOfMass.f1,
                maxRadius,
                averageTemperature.getWindowStart()
        );
    }

    static double haversine(double lat1, double lon1, double lat2, double lon2) {
        double latitudeDistance = Math.toRadians(lat2 - lat1);
        double longitudeDistance = Math.toRadians(lon2 - lon1);

        // convert to radians
        lat1 = Math.toRadians(lat1);
        lat2 = Math.toRadians(lat2);

        // apply formulae
        double a = Math.pow(Math.sin(latitudeDistance / 2), 2) +
                Math.pow(Math.sin(longitudeDistance / 2), 2) *
                        Math.cos(lat1) *
                        Math.cos(lat2);
        double rad = 6371;
        double c = 2 * Math.asin(Math.sqrt(a));
        return rad * c; // in kilometers
    }
}
