# Python data simulator

## Running the simulator locally

### Starting the Kafka stack

```bash
docker-compose up -d
```

### Running the simulator

There are 2 ways to run the simulator:

1. Inside a docker container. Run:

```bash
docker-compose -f ./docker-compose.simulator.yaml up -d
```

2. Locally (preferred for development).

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
