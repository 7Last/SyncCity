# Python data simulator
## Running the simulator in local mode
Running the simulator in local mode means that only the Kafka stack is running
inside the docker container. The simulator is running on the host machine.
This is useful for development and debugging purposes. The corresponding `docker-compose`
file is `docker-compose.local.yml`.

### Create virtual env
```bash
python -m venv ./simulator/.venv
```

### Activate virtual env
On Linux/MacOs:
```bash
source ./simulator/.venv/bin/activate
```

### Install requirements
```bash
pip3 install -r ./simulator/requirements.txt
```

### Start the Kafka stack
```bash
docker-compose -f ./docker-compose.local.yml up -d
```

### Run the script
```bash
python3 ./simulator/main.py
```

## Running the simulator in release mode
Running the simulator in release mode means that the simulator is running inside
the docker container. The corresponding `docker-compose` file is `docker-compose.release.yml`.

There is no need to create a virtual environment or install requirements in this case,
as it is all handled by the Dockerfile.

### Start the whole stack
```bash
docker-compose -f ./docker-compose.release.yml up -d
```

