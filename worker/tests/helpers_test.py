import sys
import os.path

from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import pytest

# A hack to make imports work in the test target
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# Test data / misc
from tdata import TData
td = TData()

# Test target
import helpers


class TestGetCommandFromUpdate:
    def test_without_args(self):
        update = td.update_for_command(None, "start")
        command = helpers.get_command_from_update(update)

        # Asserts
        assert command == "start"

    def test_with_args(self):
        update = td.update_for_command(None, "start", "one two three")
        command = helpers.get_command_from_update(update)

        # Asserts
        assert command == "start"

    def test_without_command(self):
        update = td.update_for_message(None, "dead / beef")
        command = helpers.get_command_from_update(update)

        # Asserts
        assert command is None


class TestGetCommandAndArgsFromUpdate:
    def test_with_command(self):
        update = td.update_for_command(None, "start")
        command, args = helpers.get_command_and_args_from_update(update)

        # Asserts
        assert command == "start"
        assert args == []

    def test_with_command_and_args(self):
        update = td.update_for_command(None, "start", "one two three")
        command, args = helpers.get_command_and_args_from_update(update)

        # Asserts
        assert command == "start"
        assert args == ["one", "two", "three"]

    def test_with_message(self):
        update = td.update_for_message(None, "dead / beef")
        command, args = helpers.get_command_and_args_from_update(update)

        # Asserts
        assert command is None
        assert args is None


class TestGetUserIdFromUpdate:
    def test_with_command(self):
        update = td.update_for_command(None, "start", user_id="1337")
        user_id = helpers.get_user_id_from_update(update)

        # Asserts
        assert user_id == 1337

    def test_with_command_and_args(self):
        update = td.update_for_command(
            None, "start", "one two three", user_id="1337")
        user_id = helpers.get_user_id_from_update(update)

        # Asserts
        assert user_id == 1337

    def test_with_message(self):
        update = td.update_for_message(None, "dead / beef", user_id="1337")
        user_id = helpers.get_user_id_from_update(update)

        # Asserts
        assert user_id == 1337


class TestGetMessageFromUpdate:
    def test_with_message(self):
        update = td.update_for_message(None, "dead / beef")
        message = helpers.get_message_from_update(update)

        # Asserts
        assert message == "dead / beef"

    def test_with_command(self):
        update = td.update_for_command(None, "start", "one two three")
        message = helpers.get_message_from_update(update)

        # Asserts
        assert message == "/start one two three"


@pytest.mark.state_helpers
class TestGetKeyboardOptions:
    def test_with_simple_keyboard(self):
        keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton('option 1'), KeyboardButton('option 2')]])
        options = helpers.get_keyboard_options(keyboard)

        # Asserts
        assert options == ['option 1', 'option 2']

    def test_with_multirow_keyboard(self):
        keyboard = ReplyKeyboardMarkup([[KeyboardButton('option 1'), KeyboardButton('option 2')], [
                                       KeyboardButton('option 3'), KeyboardButton('option 4')]])
        options = helpers.get_keyboard_options(keyboard)

        # Asserts
        assert options == ['option 1', 'option 2', 'option 3', 'option 4']

    def test_with_empty_keyboard(self):
        keyboard = ReplyKeyboardMarkup([])
        options = helpers.get_keyboard_options(keyboard)

        # Asserts
        assert options == []
