import unittest
from testcontainers.compose import DockerCompose
from kafka import KafkaProducer, KafkaConsumer
import time

class TestIntegrationKafka(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.compose = DockerCompose("../docker-compose.yml")
        cls.compose.start()
        time.sleep(60)

    @classmethod
    def tearDownClass(cls):
        cls.compose.stop()

    def test_kafka(self):
        producer = KafkaProducer(bootstrap_servers="localhost:9092")
        topic = "test-topic"
        message = b"test message"

        producer.send(topic, message)
        producer.flush()

        time.sleep(10)

        consumer = KafkaConsumer(topic, bootstrap_servers="localhost:9092", auto_offset_reset="earliest")

        received_messages = [msg.value for msg in consumer]

        self.assertIn(message, received_messages)

if __name__ == "__main__":
    unittest.main()