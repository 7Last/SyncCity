package com.sevenlast.synccity.serialization;

import lombok.AllArgsConstructor;
import org.apache.avro.Schema;
import org.apache.flink.api.common.serialization.SerializationSchema;
import org.apache.flink.formats.avro.registry.confluent.ConfluentRegistryAvroSerializationSchema;

@AllArgsConstructor
public class RecordSerializationSchema<T extends RecordSerializable> implements SerializationSchema<T> {
    final String topic;
    final Schema schema;
    final String schemaRegistryUrl;

    @Override
    public byte[] serialize(T element) {
        var serializer = ConfluentRegistryAvroSerializationSchema.forGeneric(topic, schema, schemaRegistryUrl);
        var record = element.toGenericRecord(schema);
        return serializer.serialize(record);
    }
}
