"""This module contains the AnyCommandHandler class."""
import warnings

from future.utils import string_types

from telegram.ext import Handler, CommandHandler
from telegram import Update


class AnyCommandHandler(CommandHandler):
    """Handler class to handle Telegram commands.

    Commands are Telegram messages that start with ``/``, optionally followed by an ``@`` and the
    bot's name and/or some additional text.

    Extends the original CommandHandler class by allowing any command
    """

    def __init__(self,
                 callback,
                 filters=None,
                 allow_edited=False,
                 pass_args=False,
                 pass_update_queue=False,
                 pass_job_queue=False,
                 pass_user_data=False,
                 pass_chat_data=False):
        super(AnyCommandHandler, self).__init__(
            "dummycommand",
            callback,
            pass_update_queue=pass_update_queue,
            pass_job_queue=pass_job_queue,
            pass_user_data=pass_user_data,
            pass_chat_data=pass_chat_data)

        self.filters = filters
        self.allow_edited = allow_edited
        self.pass_args = pass_args

    def check_update(self, update):
        """Determines whether an update should be passed to this handlers :attr:`callback`.

        Args:
            update (:class:`telegram.Update`): Incoming telegram update.

        Returns:
            :obj:`bool`

        """
        if (isinstance(update, Update) and (
                update.message or update.edited_message and self.allow_edited)):
            message = update.message or update.edited_message

            if message.text and message.text.startswith(
                    '/') and len(message.text) > 1:
                first_word = message.text_html.split(None, 1)[0]
                if len(first_word) > 1 and first_word.startswith('/'):
                    command = first_word[1:].split('@')
                    # in case the command was sent without a username
                    command.append(message.bot.username)

                    if not (command[1].lower() ==
                            message.bot.username.lower()):
                        return False

                    if self.filters is None:
                        res = True
                    elif isinstance(self.filters, list):
                        res = any(func(message) for func in self.filters)
                    else:
                        res = self.filters(message)

                    return res

        return False

    def handle_update(self, update, dispatcher):
        """Send the update to the :attr:`callback`.

        Args:
            update (:class:`telegram.Update`): Incoming telegram update.
            dispatcher (:class:`telegram.ext.Dispatcher`): Dispatcher that originated the Update.

        """

        message = update.message or update.edited_message

        return self.callback(dispatcher.bot, update, message)
