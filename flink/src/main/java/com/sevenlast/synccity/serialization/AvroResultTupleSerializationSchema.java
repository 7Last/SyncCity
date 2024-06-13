package com.sevenlast.synccity.serialization;

import com.sevenlast.synccity.models.ResultTuple;
import org.apache.avro.Schema;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroSerializationSchema;

public class AvroResultTupleSerializationSchema implements SerializationSchema<ResultTuple> {
    final String topic;
    final Schema schema;
    final String schemaRegistryUrl;

    public AvroResultTupleSerializationSchema(String topic, Schema schema, String schemaRegistryUrl) {
        this.topic = topic;
        this.schema = schema;
        this.schemaRegistryUrl = schemaRegistryUrl;
    }

    @Override
    public byte[] serialize(ResultTuple element) {
        var serializer = ConfluentRegistryAvroSerializationSchema.forGeneric(topic, schema, schemaRegistryUrl);
        var record = element.toGenericRecord(schema);
        return serializer.serialize(record);
    }
}
