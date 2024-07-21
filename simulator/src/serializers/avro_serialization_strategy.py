import os
from pathlib import Path
from typing import Dict

from confluent_avro import SchemaRegistry, AvroValueSerde
from dotenv import load_dotenv

from .dict_raw_data_adapter import DictSerializable
from .serialization_strategy import SerializationStrategy

SerdeWithSchema = (AvroValueSerde, str)


class AvroSerializationStrategy(SerializationStrategy):
    def __init__(self) -> None:
        load_dotenv()
        schema_registry_url = os.getenv('SCHEMA_REGISTRY_URL')
        if schema_registry_url is None or schema_registry_url == "":
            raise Exception("SCHEMA_REGISTRY_URL environment variable must be set")

        schemas_path = os.getenv('SCHEMAS_RELATIVE_PATH')
        if schemas_path is None or schemas_path == "":
            raise Exception("SCHEMAS_RELATIVE_PATH environment variable must be set")

        # <project_root>/redpanda/schemas directory
        self.__schema_path = Path(__file__).parent.joinpath(schemas_path)

        self.__registry_client = SchemaRegistry(
            url=schema_registry_url,
            headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        )
        self.__serde_by_subject: Dict[str, SerdeWithSchema] = {}

    def serialize(self, data: DictSerializable) -> bytes:
        topic = data.topic()
        value_subject = f'{topic}-value'

        if value_subject not in self.__serde_by_subject:
            avro_serde = AvroValueSerde(self.__registry_client, topic)
            value_schema = (self.__schema_path / f"{value_subject}.avsc").read_text()
            self.__serde_by_subject[value_subject] = (avro_serde, value_schema)
        else:
            avro_serde, value_schema = self.__serde_by_subject[value_subject]

        return avro_serde.serialize(data.to_dict(), value_schema)
