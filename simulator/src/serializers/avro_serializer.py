import io
import json
import os
from typing import Dict
import logging as log

import requests
from avro.io import DatumWriter, BinaryEncoder
from avro.schema import Schema, parse
from dotenv import load_dotenv

from .serializer_strategy import SerializerStrategy
from ..models.raw_data.raw_data import RawData


class AvroSerializer(SerializerStrategy):

    def __init__(self) -> None:
        super().__init__()
        self._schemas_by_subject = load_avro_schemas()

    def serialize(self, data: RawData) -> bytes:
        # json encode the data
        json_item = data.accept(self._visitor)

        # TODO: optimize to avoid creating objects every time
        # avro encode the json data
        schema_id, schema = self._schemas_by_subject[data.subject]
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)

        writer.write(json_item, encoder)
        raw_bytes = bytes_writer.getvalue()

        # prepend the magic byte and schema id to the raw bytes
        return self._schema_bytes_identifier(schema_id) + raw_bytes

    @staticmethod
    def _schema_bytes_identifier(schema_id: int) -> bytes:
        magic_byte = bytearray([0])
        return magic_byte + schema_id.to_bytes(4, 'big')

def _create_all_schemas(schema_registry_url: str, path: str) -> (
        Dict)[str, tuple[int, Schema]]:
    schemas = {}
    for schema_file in os.listdir(path):
        if not schema_file.endswith(".avsc"):
            continue
        name = os.path.basename(schema_file).replace(".avsc", "")
        with open(file=schema_file, encoding='utf-8') as f:
            schema = f.read()
        payload = {"schema": schema, "schemaType": "AVRO"}

        try:
            parsed = parse(schema)
        except Exception as e:
            raise Exception(f"Error parsing schema {name}") from e

        schema_id = _create_subject(schema_registry_url, name, payload)
        schemas[name] = (schema_id, parsed)

    return schemas


def _create_subject(schema_registry_url: str, subject: str, payload: Dict) -> int:
    url = f"{schema_registry_url}/subjects/{subject}/versions"
    log.info(f"Creating schema {subject} at {url}")
    headers = {"Content-Type": "application/vnd.schemaregistry.v1+json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # TODO: just for testing purposes, remove this
    if response.status_code == 409:
        log.info(f"Schema {subject} already exists, overwriting")
        delete_url = f"{schema_registry_url}/subjects/{subject}"
        response = requests.delete(
            f"{delete_url}?permanent=false",
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(f"Error deleting schema {subject}: {response.json()}")
        log.info(f"Schema {subject} soft deleted successfully")

        response = requests.delete(
            f"{delete_url}?permanent=true",
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception(f"Error deleting schema {subject}: {response.json()}")

        # create the new schema
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error creating schema {subject}: {response.json()}")
    elif response.status_code != 200:
        raise Exception(f"Error creating schema {subject}: {response.json()}")

    schema_id = response.json()["id"]
    log.info(f"Schema {subject} created successfully with id {schema_id}")
    return schema_id


def load_avro_schemas() -> Dict[str, tuple[int, Schema]]:
    load_dotenv()

    schema_registry_url = os.getenv('SCHEMA_REGISTRY_URL')
    if schema_registry_url is None or schema_registry_url == "":
        raise Exception("SCHEMA_REGISTRY_URL environment variable must be set")

    log.debug(f'Loading avro schemas to registry {schema_registry_url}')

    schemas_path = os.getenv('SCHEMAS_PATH')
    if schemas_path is None or schemas_path == "":
        raise Exception("SCHEMAS_PATH environment variable must be set")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    schemas_path = os.path.join(current_dir, schemas_path)
    log.debug(f'Loading schemas from dir {schemas_path}')

    log.info(f"Created schema registry client at url {schema_registry_url}")
    return _create_all_schemas(schema_registry_url, schemas_path)
