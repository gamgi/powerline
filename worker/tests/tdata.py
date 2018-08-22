import json
from pathlib import Path
from telegram import Update

test_data_dir = Path('tests/test_data/')


class TData:
    """Provides smooth access to test data
    """

    def __init__(self):
        self.data = {}
        for file_name in test_data_dir.glob('*.json'):
            with open(file_name, "r") as json_file:
                key = Path(file_name).stem
                self.data[key] = json.load(json_file)
    '''
    @property
    def keys(self):
        return self.data.keys

    def __getattr__(self, name):
        return self.data[name]
    '''

    def file(self, name):
        return self.data[name]

    def update_from_file(self, bot, name):
        update = Update.de_json(
            self.file(name),
            bot)
        return update

    def update_for_command(
            self,
            bot,
            command,
            args="",
            user_id=None,
            chat_id=None):
        """Creates a telegram.Update instance"""

        mock_data = self.data['req_template_command_01']
        # set command
        mock_data['message']['text'] = "/{} {}".format(command, args)
        mock_data['message']['entities'][0]['length'] = len(command) + 1
        # set chat_id
        if (chat_id):
            mock_data['message']['chat']['id'] = chat_id

        # set user_id
        if (user_id):
            mock_data['message']['from']['id'] = user_id

        update = Update.de_json(
            mock_data,
            bot)
        return update

    def update_for_message(
            self,
            bot,
            message,
            user_id=None,
            chat_id=None):
        """Creates a telegram.Update instance"""

        mock_data = self.data['req_template_message_01']
        # set command
        mock_data['message']['text'] = message
        # set chat_id
        if (chat_id):
            mock_data['message']['chat']['id'] = chat_id

        # set user_id
        if (user_id):
            mock_data['message']['from']['id'] = user_id

        update = Update.de_json(
            mock_data,
            bot)
        return update
