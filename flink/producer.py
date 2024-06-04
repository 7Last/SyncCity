import json, time
from datetime import datetime, timezone, timedelta, tzinfo

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:19092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

sensors = ['probe-1', 'probe-2']
begin_date = datetime(2024, 1, 1, 1, 5, 0)

i = 0
while True:
    item_date = begin_date + timedelta(minutes=i)
    item = {
        'name': sensors[i % 2],
        'temperature': 20.0 + i/10,
        # format as local time
        'datetime': item_date.isoformat()
    }
    item_date_ms = int(item_date.timestamp() * 1000)
    producer.send('sensors', value=item, timestamp_ms=item_date_ms)
    time.sleep(1)
    print(f"Sent: {item}")
    i += 1
