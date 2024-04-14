FROM python:3.11.9-alpine
WORKDIR /simulator
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD ["SENSORS_SIMULATOR_ENV=release","python3","main.py"]