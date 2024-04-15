import glob
import json
import logging as log
import os
from typing import Dict

import requests
from avro.schema import Schema, parse
from dotenv import load_dotenv


def _create_all_schemas(schema_registry_url: str, path: str) -> (
        Dict)[str, tuple[int, Schema]]:
    ids_by_subject = {}
    for schema_file in glob.glob(f"{path}/*.avsc"):
        name = os.path.basename(schema_file).replace(".avsc", "")
        schema = open(schema_file, encoding='utf-8').read()  # noqa: SIM115
        payload = {"schema": schema, "schemaType": "AVRO"}

        try:
            parsed = parse(schema)
        except Exception as e:
            raise Exception(f"Error parsing schema {name}") from e

        ids_by_subject[name] = (
            _create_subject(schema_registry_url, name, payload),
            parsed,
        )
    return ids_by_subject


def _create_subject(schema_registry_url: str, subject: str, payload: Dict) -> int:
    url = f"{schema_registry_url}/subjects/{subject}/versions"
    response = requests.post(url, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"Error creating schema {subject}: {response.json()}")

    schema_id = response.json()["id"]
    log.info(f"Schema {subject} created successfully with id {schema_id}")
    return schema_id


def load_avro_schemas() -> Dict[str, tuple[int, Schema]]:
    load_dotenv()

    schema_registry_url = os.getenv('SCHEMA_REGISTRY_URL')
    log.debug(f'Loading avro schemas to registry {schema_registry_url}')
    schemas_path = os.getenv('SCHEMAS_PATH')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    schemas_path = os.path.join(current_dir, schemas_path)
    log.debug(f'Loading schemas from dir {schemas_path}')

    log.info(f"Created schema registry client at url {schema_registry_url}")
    return _create_all_schemas(schema_registry_url, schemas_path)
