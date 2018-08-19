import sys
import os
from telegram import Message, Update

# Testing
import pytest
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
from create_database import create_database
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


@pytest.fixture(scope="module")
def db_engine():
    db = Postgresql()
    create_database(db.url())
    db_engine = create_engine(db.url())
    yield db_engine
    db.stop()


@pytest.fixture(scope="module")
def redis():
    return None


@pytest.fixture(scope="function")
def bot():
    return MagicMock()


@pytest.fixture(scope="function")
def Session(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    #trans = connection.begin()

    Session = sessionmaker(bind=connection)

    yield Session
    # trans.rollback()

    # return connection to the Engine
    connection.close()


@pytest.fixture(scope="function")
def inspect_session(Session):
    """For making database queries in test assertion"""
    inspect_session = Session()
    yield inspect_session
    inspect_session.close()


@pytest.fixture(scope="function")
def worker(bot, Session, redis):
    worker = Worker()
    worker.bind(bot, Session, redis)
    yield worker


class TestCommands:
    def test_command_start(self, Session, inspect_session, worker, bot):
        user_id = chat_id = 123
        update = md.update_for_command(
            bot, "start", chat_id=chat_id, user_id=user_id)
        worker.command_start(user_id, update)

        # Asserts
        bot.send_message.assert_called()
        args, kwargs = bot.send_message.call_args
        assert kwargs['chat_id'] == chat_id
        assert inspect_session.query(models.User).count() == 1
        # TODO assert state

    def test_command_dummy(self, worker, bot):
        worker.state.set_state('unregistered')
        update = md.update_for_command(
            bot, "dummy", "one two three")
        user_id = get_user_id_from_update(update)
        command, args = get_command_and_args_from_update(update)
        worker.handle_command(user_id, update, command, args)

        # Asserts
        assert worker.state.state == 'dummy_state'

    def test_load_user(self):
        pass

    def test_multiple_users(self):
        pass


class TestRegisterFlow:
    def test_register_flow(self, worker):
        worker.state.set_state('unregistered')
        update = md.update_from_file(bot, 'req_command_start_01')
        user_id = get_user_id_from_update(update)
        worker.handle_command(user_id, update, 'start', [])

        # Assert
        assert worker.state.state == 'register_1'
