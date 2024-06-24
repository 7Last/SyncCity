package com.sevenlast.synccity.serialization;

import org.apache.avro.Schema;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroSerializationSchema;

public class RecordSerializationSchema implements SerializationSchema<RecordSerializable> {
    final String topic;
    final Schema schema;
    final String schemaRegistryUrl;

    public RecordSerializationSchema(String topic, Schema schema, String schemaRegistryUrl) {
        this.topic = topic;
        this.schema = schema;
        this.schemaRegistryUrl = schemaRegistryUrl;
    }

    @Override
    public byte[] serialize(RecordSerializable element) {
        var serializer = ConfluentRegistryAvroSerializationSchema.forGeneric(topic, schema, schemaRegistryUrl);
        var record = element.toGenericRecord(schema);
        return serializer.serialize(record);
    }
}
