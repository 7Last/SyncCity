import unittest
from testcontainers.compose import DockerCompose
from clickhouse_driver import Client
from kafka import KafkaProducer, KafkaConsumer
import time


class TestIntegrationClickhouse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.compose = DockerCompose("../docker-compose.yml")
        cls.compose.start()
        time.sleep(60)

    @classmethod
    def tearDownClass(cls):
        cls.compose.stop()

    def test_clickhouse(self):
        producer = KafkaProducer(bootstrap_servers="localhost:9092")
        topic = "test-topic"
        message = b"test message"

        producer.send(topic, message)
        producer.flush()

        # Come avviene la comunicazione tra Kafka e Clickhouse?

        time.sleep(10)

        client = Client("localhost")
        query_result = client.execute("SELECT * FROM sensors WHERE topic = 'test-topic'")

        self.assertTrue(len(query_result) > 0)


if __name__ == "__main__":
    unittest.main()
