import glob
import json
import os
from typing import Dict

import requests

SCHEMA_REGISTRY_URL = "http://localhost:8081"


def create_schema(name: str, payload: Dict):
    url = f"{SCHEMA_REGISTRY_URL}/subjects/{name}/versions"
    response = requests.post(url, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Error creating schema {name}: {response.json()}")
    else:
        print(f"Schema {name} created successfully")


def delete_schema(name: str):
    url = f"{SCHEMA_REGISTRY_URL}/subjects/{name}"
    response = requests.delete(url)
    if response.status_code != 200:
        print(f"Error deleting schema {name}: {response.json()}")
    else:
        print(f"Schema {name} deleted successfully")


def get_latest_schema(schema_name: str):
    latest = requests.get(
        f"{SCHEMA_REGISTRY_URL}/subjects/{schema_name}/versions/latest")
    if latest.status_code == 404:
        return None
    return latest.json()


def check_if_exists(schema_name: str, payload: Dict):
    url = f"{SCHEMA_REGISTRY_URL}/subjects/{schema_name}/versions/latest"
    response = requests.get(url)
    if response.status_code == 404:
        return False
    latest_schema = json.loads(response.json()["schema"])
    payload_schema = json.loads(payload["schema"])
    return latest_schema == payload_schema


def create_if_not_exists(schema_name: str, payload: Dict):
    if not check_if_exists(schema_name, payload):
        create_schema(schema_name, payload)
    else:
        print(f"Schema {schema_name} already exists")


def create_all_schemas(path: str):
    schemas = glob.glob(f"{path}/*.avsc")
    for schema in schemas:
        name = os.path.basename(schema).replace(".avsc", "")
        payload = {
            "schema": open(schema).read(),
            "schemaType": "AVRO"
        }
        create_if_not_exists(name, payload)


if __name__ == '__main__':
    schemas_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schemas')
    create_all_schemas(schemas_path)
    # delete_schema("reading")
