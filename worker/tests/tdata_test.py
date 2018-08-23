import sys
import os.path
import pytest

# A hack to make imports work in the test target
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

# Test data / misc
import helpers
# Test target
from tdata import TData

td = TData()


@pytest.mark.tdata
class TestUpdateForCommand:
    def test_command(self):
        update = td.update_for_command(None, "start")

        # Asserts
        assert update.message.text == "/start"
        assert update.message.from_user.id == 123

    def test_command_and_args(self):
        update = td.update_for_command(None, "dummy", "one two three")

        # Asserts
        assert update.message.text == "/dummy one two three"
        assert update.message.from_user.id == 123

    def test_command_and_params(self):
        update = td.update_for_command(None, "start", user_id=1337, chat_id=2000)

        # Asserts
        assert update.message.text == "/start"
        assert update.message.from_user.id == 1337
        assert update.message.chat.id == 2000

    def test_no_writes(self):
        other_update = td.update_for_command(None, "start", user_id=1337, chat_id=2000)
        update = td.update_for_command(None, "dummy", "one two three")
        user_id = helpers.get_user_id_from_update(update)

        # Asserts
        assert user_id == 123
