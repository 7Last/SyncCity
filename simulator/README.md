# Python data simulator
Two profiles are provided in the `docker-compose.yaml` file:
- `local`: for local test and debug purposes. Runs the Kafka stack in `docker` containers,
but does not build the `simulator` image, which is expected to be run manually;
- `release`: builds also the `simulator` image, which is then run in the same network as the Kafka stack.

## Running with `local` profile
- Create a virtual environment:
```bash
python -m venv ./simulator/.venv
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
docker-compose up -d
```