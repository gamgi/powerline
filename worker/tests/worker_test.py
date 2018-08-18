import sys
import os
from telegram import Message, Update

# Testing
import unittest
from unittest.mock import MagicMock
import testing.postgresql

# Logging
import logging
logging.basicConfig()
logger = logging.getLogger()

# A hack to make imports work in the test target
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import create_database
# Enable following line to echo database queries
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Postgresql class which shares the generated test database
Postgresql = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)

# Helpers


def get_user_id_from_update(update):
    try:
        return update['message']['from_user']['id']
    except BaseException:
        return ''


def get_command_and_args_from_update(update):
    try:
        command, unused, args_joined = update['message']['text'].partition(" ")
        return command.replace("/", "", 1), args_joined.split(" ")
    except BaseException as err:
        logging.info(err)
        return None


# Mock data
from mock_data import MockData
import models

# Test target
from worker import Worker

md = MockData()


def tearDownModule(self):
    # clear cached database at end of tests
    Postgresql.clear_cache()


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.db = Postgresql()
        self.redis = None
        self.bot = MagicMock()

        # Create db schema
        create_database.create_database(self.db.url())

        # Bind to worker
        self.db_engine = create_engine(self.db.url())
        self.session = sessionmaker(bind=self.db_engine)()
        self.worker = Worker()
        self.worker.bind(self.bot, self.db_engine, self.redis)

    def tearDown(self):
        self.session.close()
        self.db.stop()

    def test_command_start(self):
        # update = Update.de_json(
        #    md.req_command_start_01,
        #    self.bot)
        update = md.update_for_command(self.bot, "start")
        user_id = get_user_id_from_update(update)
        #self.worker.state.user.bind(self.bot, user_id, None)
        self.worker.command_start(user_id, update)
        # Asserts
        self.bot.send_message.assert_called()
        args, kwargs = self.bot.send_message.call_args
        self.assertEqual(
            kwargs['chat_id'],
            md.file('req_command_start_01')['message']['chat']['id'])
        self.assertEqual(self.session.query(models.User).count(), 1)
        # TODO assert state

    def test_command_dummy(self):
        self.worker.state.set_state('unregistered')
        update = md.update_for_command(
            self.bot, "dummy", "one", "two", "three")
        user_id = get_user_id_from_update(update)
        command, args = get_command_and_args_from_update(update)
        #self.worker.state.user.bind(self.bot, user_id, None)
        self.worker.handle_command(user_id, update, command, args)

        # Asserts
        self.assertEqual(self.worker.state.state, 'dummy_state')

    def test_register_flow(self):
        self.worker.state.set_state('unregistered')
        update = md.update_from_file(self.bot, 'req_command_start_01')
        user_id = get_user_id_from_update(update)
        self.worker.handle_command(user_id, update, 'start', [])

        # Assert
        self.assertEqual(self.worker.state.state, 'register_1')
