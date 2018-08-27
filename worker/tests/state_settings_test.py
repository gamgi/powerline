import sys
import os.path
# Testing
import pytest
from unittest.mock import MagicMock

# A hack to make imports work in the test target
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# Database
from sqlalchemy.orm import sessionmaker
#from sqlalchemy_utils import force_instant_defaults
from create_fake_database import fake_database, create_database_fixture

# Logging
#import logging
# Enable following line to echo database queries
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Test data / misc
import models
import state_fixture
import enums


def sent_text(mock):
    mock.send_message.assert_called()
    args, kwargs = mock.send_message.call_args
    return kwargs['text']


@pytest.fixture(scope="function")
def user():
    # force_instant_defaults()
    user = models.User()
    return user


@pytest.fixture(scope="function")
def bot():
    return MagicMock()


@pytest.fixture(scope="function", params=['EN'])
# @pytest.fixture(scope="function", params=['EN', 'SE']) # To test multilang
def state(bot, request):
    state = state_fixture.State(bot)
    # Utilize pytest parametrized test to test different languages
    state.language = request.param
    return state


@pytest.mark.state_settings
class TestStateSettings:
    def test_settings_menu(self, state, user, bot):
        state.set_state('idle')
        state.trigger('settings', user=user)

        # Asserts
        assert state.state == 'settings_menu'
        bot.send_message.assert_called()

        state.trigger('back', user=user)

        # Asserts
        assert state.state == 'idle'

    def test_settings_menu(self, state, user, bot):
        state.set_state('idle')
        state.trigger('settings', args=['these', 'wont', 'matter'], user=user)

        # Asserts
        assert state.state == 'settings_menu'
        bot.send_message.assert_called()

    def test_settings_register_3(self, state, user, bot):
        state.set_state('settings_menu')
        state.trigger('subscription', user=user)

        # Asserts
        assert state.state == 'settings_register_3'
        bot.send_message.assert_called()

        state.trigger('message', message="badvalue")

        # Asserts
        assert state.state == 'settings_register_3'
        bot.send_message.assert_called()

        state.trigger('message', message="a lot", user=user)

        # Asserts
        assert state.state == 'idle'
        assert user.subscription == 'a lot'

    def test_settings_delete(self, state, user, bot):
        state.set_state('settings_menu')
        state.trigger('delete', user=user)

        # Asserts
        assert state.state == 'settings_delete'
        bot.send_message.assert_called()

        state.trigger('back', user=user)
        state.trigger('settings', user=user)

        # Asserts
        assert state.state == 'settings_menu'

        state.trigger('delete', user=user)
        state.trigger('yesimsuredelete', user=user)

        # Asserts
        assert state.state == 'unregistered'
        # TODO actually delete
