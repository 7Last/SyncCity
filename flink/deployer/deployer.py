import argparse
import os
import sys

import requests
import requests.exceptions


class FlinkRestClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = requests.Session()

    def build_url(self, path):
        return f"{self.base_url}/{path}"

    def get_id_if_exists(self, path: str) -> str | None:
        try:
            url = self.build_url("jars")
            response = self.client.get(url)
            response.raise_for_status()
            jobs = response.json()
            for job in jobs['files']:
                if job['name'] == os.path.basename(path):
                    return job['id']
            return None
        except requests.exceptions.HTTPError as e:
            print('Could not check if jar exists', e)
            sys.exit(1)

    def upload_jar(self, path: str) -> str:
        jar_id = self.get_id_if_exists(path)
        if jar_id is not None:
            print(f"Jar file {path} already exists, skipping upload")
            sys.exit(0)

        url = self.build_url("jars/upload")
        try:
            with open(path, 'rb') as file:
                files = {'jarfile': (
                    os.path.basename(path), file, 'application/java-archive',
                )}
                response = self.client.post(url, files=files)
                response.raise_for_status()

                created_jar_filename = self.extract_jar_id(response.json()['filename'])
                print(f"Uploaded jar file: {created_jar_filename}")
                return created_jar_filename
        except requests.exceptions.HTTPError as e:
            print('Could not upload jar file', e)
            sys.exit(1)

    def run_jar(self, jar_id: str, entry_class: str):
        run_jar_request = {"entryClass": entry_class}

        url = self.build_url(f"jars/{jar_id}/run")
        try:
            response = self.client.post(url, json=run_jar_request)
            response.raise_for_status()
            print(f"Successfully jar with id: {jar_id}")
        except requests.exceptions.HTTPError as e:
            print('Could not run jar', e)
            sys.exit(1)

    @staticmethod
    def extract_jar_id(filename: str) -> str:
        return os.path.basename(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flink REST client')
    parser.add_argument('--flink_url', type=str, help='Flink REST API base url',
                        required=True)
    parser.add_argument('--jars', type=str, required=True,
                        help='Comma separated list of jar files to upload')
    parser.add_argument('--classes', type=str, required=True,
                        help='Comma separated list of entry classes')

    args = parser.parse_args()
    client = FlinkRestClient(base_url=args.flink_url)
    jar_files = args.jars.split(',')
    entry_classes = args.classes.split(',')

    for jar_file, entry_class in zip(jar_files, entry_classes, strict=False):
        response = client.upload_jar(jar_file)
        jar_id = client.extract_jar_id(response)
        client.run_jar(jar_id, entry_class)
