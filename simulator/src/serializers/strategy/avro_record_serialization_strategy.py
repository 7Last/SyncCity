import os
from pathlib import Path
from typing import Dict

from confluent_avro import SchemaRegistry, AvroValueSerde
from dotenv import load_dotenv

from ...models.raw_data.raw_data import RawData
from .record_serialization_strategy import RecordSerializationStrategy
from ..visitor.json_converter_visitor import JsonConverterVisitor

SerdeWithSchema = (AvroValueSerde, str)


class AvroRecordSerializationStrategy(RecordSerializationStrategy):

    def __init__(self) -> None:
        super().__init__(JsonConverterVisitor())
        load_dotenv()
        schema_registry_url = os.getenv('SCHEMA_REGISTRY_URL')
        if schema_registry_url is None or schema_registry_url == "":
            raise Exception("SCHEMA_REGISTRY_URL environment variable must be set")

        schemas_path = os.getenv('SCHEMAS_RELATIVE_PATH')
        if schemas_path is None or schemas_path == "":
            raise Exception("SCHEMAS_RELATIVE_PATH environment variable must be set")

        # <project_root>/redpanda/schemas directory
        self._schema_path = Path(__file__).parent.parent.joinpath(schemas_path)

        self._registry_client = SchemaRegistry(
            url=schema_registry_url,
            headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        )
        self._serde_by_subject: Dict[str, SerdeWithSchema] = {}

    def serialize_key(self, data: RawData) -> bytes:
        pass

    def serialize_value(self, data: RawData) -> bytes:
        json_item = data.accept(self._visitor)
        value_subject = data.value_subject()

        if value_subject not in self._serde_by_subject:
            avro_serde = AvroValueSerde(self._registry_client, data.topic)
            value_schema = (
                    self._schema_path / f"{data.value_subject()}.avsc").read_text()

            self._serde_by_subject[value_subject] = (avro_serde, value_schema)
        else:
            avro_serde, value_schema = self._serde_by_subject[value_subject]

        return avro_serde.serialize(json_item, value_schema)
