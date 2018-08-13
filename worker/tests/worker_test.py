import sys
import os

from telegram import Message, Update

# Testing
import unittest
from unittest.mock import MagicMock
import testing.postgresql

# Logging
import logging
logger = logging.getLogger()

# Postgresql class which shares the generated test database
Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)

# A hack to make imports work in the test target
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# Mock data
from mock_data import data as md

# Test target
import worker


def tearDownModule(self):
    # clear cached database at end of tests
    Postgresql.clear_cache()


class TestCommands(unittest.TestCase):
    def setUp(self):
        #self.db = Postgresql()
        self.db = None
        self.redis = None
        self.bot = MagicMock()
        worker.bind(self.bot, self.db, self.redis)

    def tearDown(self):
        # self.db.stop()
        pass

    def test_start(self):
        result = worker.handle_update(
            Update.de_json(
                md.req_command_start_01,
                self.bot))
        self.bot.send_message.assert_called()
        args, kwargs = self.bot.send_message.call_args
        self.assertEqual(
            kwargs['chat_id'],
            md.req_command_start_01['message']['chat']['id'])
        # TODO assert state
