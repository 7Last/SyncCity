package com.sevenlast.synccity;

import org.apache.flink.api.common.functions.AggregateFunction;
import org.apache.flink.api.java.tuple.Tuple2;

import java.time.LocalDateTime;

public class Average {

    public static class Aggregator implements AggregateFunction<SensorData, Tuple2<Integer, Double>, Result> {
        public Tuple2<Integer, Double> createAccumulator() {
            return new Tuple2<>(0, 0.0);
        }

        @Override
        public Tuple2<Integer, Double> add(SensorData value, Tuple2<Integer, Double> accumulator) {
            return new Tuple2<>(accumulator.f0 + 1, accumulator.f1 + value.getTemperature());
        }

        @Override
        public Result getResult(Tuple2<Integer, Double> accumulator) {
            return new Result("sensor", LocalDateTime.now(), accumulator.f1 / accumulator.f0);
        }

        @Override
        public Tuple2<Integer, Double> merge(Tuple2<Integer, Double> a, Tuple2<Integer, Double> b) {
            return new Tuple2<>(a.f0 + b.f0, a.f1 + b.f1);
        }
    }

    public static class Result {
        String sensorName;
        LocalDateTime timestamp;
        Double average;

        public Result(String sensorName, LocalDateTime timestamp, Double average) {
            this.sensorName = sensorName;
            this.timestamp = timestamp;
            this.average = average;
        }

        @Override
        public String toString() {
            return "AggregatedRecord{" +
                    "sensorName='" + sensorName + '\'' +
                    ", timestamp='" + timestamp + '\'' +
                    ", average=" + average +
                    '}';
        }
    }
}
