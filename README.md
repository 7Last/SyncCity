# Running locally

This document provides instructions on how to run the project locally.

Two profiles are provided in the `docker-compose.yaml` file:

- `local`: for local test and debug purposes. Runs the Kafka stack in `docker` containers,
  but does not build the `simulator` image, which is expected to be run manually;
- `release`: builds also the `simulator` image, which is then run in the same network as the Kafka stack.

## Running with `local` profile

Running the Kafka stack:

```bash
docker-compose --profile local up -d
```

Give all permissions to the `./volumes/` folder that has been created:

```bash
chmod -R 777 ./volumes
```

then **run all containers that are turned off** and then run:

```bash
curl "localhost:8083/connectors/" -H 'Content-Type: application/json' -d @./redpanda/connectors/configs/clickhouse.json
```

Running the simulator:

- Create a virtual environment:

```bash
python3 -m venv ./simulator/.venv
```

- Activate the virtual environment; for Linux and macOS:

```bash
source ./simulator/.venv/bin/activate
```

- Activate the virtual environment; for Windows:

```bash
.\simulator\.venv\Scripts\activate
```

- Install the requirements:

```bash
pip3 install -r ./simulator/requirements.txt
```

- Run the simulator:

```bash
python3 ./simulator/main.py
```

## Running with `release` profile

```bash
docker-compose --profile release up -d
```

## Running with `test` profile (integration test)

```bash
docker-compose -f docker-compose-test.yaml --profile test up -d --build
```
