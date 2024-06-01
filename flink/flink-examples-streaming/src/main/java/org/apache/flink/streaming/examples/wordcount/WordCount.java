/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.flink.streaming.examples.wordcount;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.examples.wordcount.util.WordCountData;
import org.apache.kafka.clients.consumer.ConsumerConfig;

import java.util.Properties;

public class WordCount {
    public static void main(String[] args) throws Exception {
        var kafkaBroker = "localhost:19092";

        var env = StreamExecutionEnvironment.getExecutionEnvironment();

        var kafkaProps = new Properties();
        kafkaProps.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBroker);
        kafkaProps.setProperty(ConsumerConfig.GROUP_ID_CONFIG, "consumer_test");

        var topic = "iot";

        var kafkaConsumer = KafkaSource.<String>builder()
                .setBootstrapServers(kafkaBroker)
                .setTopics(topic)
                .setGroupId("consumer_test")
                .setProperties(kafkaProps)
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        var kafkaStream = env.fromSource(kafkaConsumer, WatermarkStrategy.noWatermarks(), "Kafka Source");
        var filteredStream = kafkaStream.map((MapFunction<String, String>) value -> value);

        filteredStream.print();

        env.execute("Kafka Consumer Example");

    }
}