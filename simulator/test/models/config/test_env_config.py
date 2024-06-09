import os
import unittest.mock

from simulator.src.models.config.env_config import EnvConfig


class TestEnvConfig(unittest.TestCase):

    @unittest.mock.patch.dict(os.environ, {
        "KAFKA_HOST": "host",
        "KAFKA_PORT": "1234",
        "LOG_LEVEL": "INFO",
        "KAFKA_MAX_BLOCK_MS": "2000",
    }, clear=True)
    def test_existing_envs(self) -> None:
        conf = EnvConfig()
        # Check that the values are correctly set
        self.assertEqual(conf.kafka_host, "host")
        self.assertEqual(conf.kafka_port, "1234")
        self.assertEqual(conf.log_level, "INFO")
        self.assertEqual(conf.max_block_ms, 2000)

    @unittest.mock.patch.dict(os.environ, {
        "KAFKA_PORT": "1234",
        "KAFKA_HOST": "host",
        "LOG_LEVEL": "INFO",
        # set to empty string to override any env on the host machine
        "KAFKA_MAX_BLOCK_MS": "",
    }, clear=True)
    def test_default_values(self) -> None:
        conf = EnvConfig()
        # Check that the default values are correctly set
        self.assertEqual(conf.max_block_ms, 1000)

    @unittest.mock.patch.dict(os.environ, {
        # Missing KAFKA_HOST
        "KAFKA_HOST": "",
        "KAFKA_PORT": "1234",
        "LOG_LEVEL": "INFO",
    }, clear=True)
    def test_throw_if_missing_envs(self) -> None:
        with self.assertRaises(ValueError):
            EnvConfig()

    @unittest.mock.patch.dict(os.environ, {
        "KAFKA_HOST": "host",
        "KAFKA_PORT": "1234",
        "LOG_LEVEL": "INFO",
        "KAFKA_MAX_BLOCK_MS": "2000",
    }, clear=True)
    def test_bootstrap_server(self) -> None:
        conf = EnvConfig()
        self.assertEqual(conf.bootstrap_server, "host:1234")
