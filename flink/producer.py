import json
import time

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:19092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

for i in range(1000):
    print(f"Sending message {i}")
    time.sleep(1)
    producer.send("iot", f"message {i}")
    producer.flush()
