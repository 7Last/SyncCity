package com.sevenlast.synccity.utils;

import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import org.apache.flink.streaming.api.functions.sink.SinkFunction;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CollectionSink implements SinkFunction<ChargingEfficiencyResult> {
    public static final List<ChargingEfficiencyResult> values = Collections.synchronizedList(new ArrayList<>());

    @Override
    public void invoke(ChargingEfficiencyResult result, SinkFunction.Context context) {
        values.add(result);
    }
}
