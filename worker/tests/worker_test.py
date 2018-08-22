import sys
import os.path

# Testing
import pytest
from unittest.mock import MagicMock

# A hack to make imports work in the test target
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# Database
from sqlalchemy.orm import sessionmaker
from create_fake_database import fake_database, create_database_fixture

# Logging
import logging
# Enable following line to echo database queries
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Test data / misc
import models
from tdata import TData
import state_fixture

# Test target
from worker import Worker

td = TData()


@pytest.fixture(scope="module")
def db_engine():
    db = fake_database()
    db_engine = db.engine()

    # Create db schema
    create_database_fixture(db_engine, 'simple_one_user')

    yield db_engine
    db.stop()


@pytest.fixture(scope="module")
def redis():
    return None


@pytest.fixture(scope="function")
def bot():
    return MagicMock()


@pytest.fixture(scope="module")
def State():
    return state_fixture.State


@pytest.fixture(scope="function")
def Session(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    trans = connection.begin()

    Session = sessionmaker(bind=connection)

    yield Session

    # rollback transaction
    trans.rollback()

    # return connection to the Engine
    connection.close()


@pytest.fixture(scope="function")
def inspect_session(Session):
    """For making database queries in test assertion"""
    inspect_session = Session()
    yield inspect_session
    inspect_session.close()


@pytest.fixture(scope="function")
def worker(bot, Session, redis, State):
    worker = Worker()
    worker.bind(bot, Session, redis, State)
    yield worker


class TestCommands:
    def test_handle_command_start(self, Session, inspect_session, worker, bot):
        user_id = chat_id = 123
        update = td.update_for_command(
            bot, "start", chat_id=chat_id, user_id=user_id)
        worker.handle_command_start(user_id, update)

        # Asserts
        bot.send_message.assert_called()
        args, kwargs = bot.send_message.call_args
        assert kwargs['chat_id'] == chat_id
        assert inspect_session.query(models.User).count() == 1
        # TODO assert state

    def test_command_dummy(self, worker, bot):
        worker.state.set_state('unregistered')
        update = td.update_for_command(
            bot, "dummy", "one two three")
        user_id = helpers.get_user_id_from_update(update)
        worker.handle_command(user_id, update)

        # Asserts
        assert worker.state.state == 'dummy_state'

    def test_load_user(self):
        pass

    def test_multiple_users(self):
        pass


class TestRegisterFlow:
    def test_register_flow(self, worker, bot):
        worker.state.set_state('unregistered')
        user_id = chat_id = 123
        update = td.update_from_file(bot, 'req_command_start_01')
        update = td.update_for_command(
            bot, "start", chat_id=chat_id, user_id=user_id)
        worker.handle_command_start(user_id, update)
        #worker.handle_command(user_id, update, 'start', [])

        # Assert
        bot.send_message.assert_called()
        assert worker.state.state == 'register_1'

        update = td.update_for_message(
            bot, "mr")
        worker.handle_message(user_id, update, "mr")

        # Assert
        bot.send_message.assert_called()
        assert worker.state.state == 'register_2'
