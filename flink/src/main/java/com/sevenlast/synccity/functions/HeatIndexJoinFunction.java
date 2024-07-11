package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.SensorLocation;
import com.sevenlast.synccity.models.results.AverageResult;
import com.sevenlast.synccity.models.results.HeatIndexResult;
import org.apache.flink.api.common.functions.JoinFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;

import java.util.Set;
import java.util.stream.Collectors;

public class HeatIndexJoinFunction implements JoinFunction<AverageResult, AverageResult, HeatIndexResult> {

    // constants for heat index calculation
    private static final double C1 = -8.78469475556;
    private static final double C2 = 1.61139411;
    private static final double C3 = 2.33854883889;
    private static final double C4 = -0.14611605;
    private static final double C5 = -0.012308094;
    private static final double C6 = -0.0164248277778;
    private static final double C7 = 2.211732e-3;
    private static final double C8 = 7.2546e-4;
    private static final double C9 = -3.582e-6;

    @Override
    public HeatIndexResult join(AverageResult averageTemperature, AverageResult averageHumidity) {
        double t = averageTemperature.getValue();
        double h = averageHumidity.getValue();

        double heatIndex = C1 + (C2 * t) + (C3 * h) + (C4 * t * h)
                + (C5 * t * t) + (C6 * h * h)
                + (C7 * t * t * h) + (C8 * t * h * h)
                + (C9 * t * t * h * h);

        var sensors = averageTemperature.getSensors();
        sensors.addAll(averageHumidity.getSensors());

        var centroid = centroid(sensors);
        double maxRadius = sensors.stream()
                .map(sensor -> haversine(sensor.getLatitude(), sensor.getLongitude(), centroid.f0, centroid.f1))
                .max(Double::compareTo)
                .orElseThrow();

        return new HeatIndexResult(
                sensors.stream().map(SensorLocation::getSensorName).collect(Collectors.toSet()),
                averageTemperature.getGroupName(),
                heatIndex,
                averageTemperature.getValue(),
                averageHumidity.getValue(),
                centroid.f0,
                centroid.f1,
                maxRadius,
                averageTemperature.getWindowStart()
        );
    }

    private static double haversine(double lat1, double lon1, double lat2, double lon2) {
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

    private static Tuple2<Double, Double> centroid(Set<SensorLocation> sensors) {
        if (sensors.isEmpty()) {
            return new Tuple2<>(0.0, 0.0);
        }

        if (sensors.size() == 1) {
            var sensor = sensors.stream().findFirst().get();
            return new Tuple2<>(sensor.getLatitude(), sensor.getLongitude());
        }

        // Convert to radians and calculate the sum of x, y, z coordinates
        var sum = sensors.stream()
                .map(sensor -> {
                    var lat = Math.toRadians(sensor.getLatitude());
                    var lng = Math.toRadians(sensor.getLongitude());
                    return Tuple3.of(Math.cos(lat) * Math.cos(lng), Math.cos(lat) * Math.sin(lng), Math.sin(lat));
                })
                .reduce(
                        Tuple3.of(0.0, 0.0, 0.0),
                        (acc, tuple) -> Tuple3.of(acc.f0 + tuple.f0, acc.f1 + tuple.f1, acc.f2 + tuple.f2)
                );

        var avgX = sum.f0 / sensors.size();
        var avgY = sum.f1 / sensors.size();
        var avgZ = sum.f2 / sensors.size();

        // Convert average x, y, z coordinate to latitude and longitude
        var lng = Math.atan2(avgY, avgX);
        var hyp = Math.sqrt(avgX * avgX + avgY * avgY);
        var lat = Math.atan2(avgZ, hyp);

        return Tuple2.of(Math.toDegrees(lat), Math.toDegrees(lng));
    }
}
