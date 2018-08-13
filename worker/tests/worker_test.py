import sys
import os
import unittest
import testing.postgresql

# Logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Postgresql class which shares the generated test database
Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)

# A hack to make imports work in the test target
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# Test target
import worker

# Mock data
from mock_data import data as md


def tearDownModule(self):
    # clear cached database at end of tests
    Postgresql.clear_cache()


class TestRegisterFlow(unittest.TestCase):
    def setUp(self):
        self.db = Postgresql()
        self.redis = None
        self.worker = worker
        self.worker.bind(self.db, self.redis)

    def tearDown(self):
        self.postgresql.stop()

    def test_dummy(self):
        result = self.worker.handle_update(
            None, md.req_command_start_01)
        self.assertEqual(result, 'FOO')
