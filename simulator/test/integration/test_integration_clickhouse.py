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

        time.sleep(10)

        # Come avviene la comunicazione tra Kafka e Clickhouse?
        # Forse bastano le seguenti linee di codice

        client = Client("localhost")
        query = "SELECT * FROM sensors WHERE topic = 'test-topic'"
        query_result = client.execute(query)

        self.assertTrue(len(query_result) > 0)


if __name__ == "__main__":
    unittest.main()
