import logging

from telegram import ReplyKeyboardRemove

import enums
import helpers

logger = logging.getLogger(__name__)


class MachineHelpers:
    """Helper functions for extending transitions.Machine"""

    def machine_add_states_and_transitions(self, states, transitions):
        """The state machine is using multiple inheritance. This helps combining the states"""
        try:
            self.transitions += transitions
        except BaseException:
            self.transitions = transitions
        try:
            self.states += states
        except BaseException:
            self.states = states

    def default_on_enter(self, event):
        """On entering STATE, checks whether enum STATE exists and sends it to user.
        Also provides a STATE keyboard if defined.
        """
        assert event.transition.dest == self.state
        chat_id = event.kwargs.get('chat_id')
        destination = event.transition.dest.upper()
        # Is there something to say?
        try:
            message = enums.MESSAGES[self.language][destination]
            try:
                keyboard = enums.KEYBOARDS[destination]
            except KeyError:
                keyboard = ReplyKeyboardRemove()

            self.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard,
                parse_mode='Markdown')
            logger.info('Sent message')
        except KeyError:
            logger.info('Nothing to say')

    def default_on_exit(self, event):
        """On exiting STATE, chechs whether enum STATE_EXIT exists and sends it to user.
        Also provides a STATE_EXIT keyboard if defined.
        """
        assert event.transition.source == self.state
        chat_id = event.kwargs.get('chat_id')
        source = event.transition.source.upper()
        # Is there something to say?
        try:
            message = enums.MESSAGES[self.language]['{}_EXIT'.format(source)]
            try:
                keyboard = enums.KEYBOARDS['{}_EXIT'.format(source)]
            except KeyError:
                keyboard = ReplyKeyboardRemove()

            self.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=keyboard,
                parse_mode='Markdown')
            logger.info('Sent message')
        except KeyError:
            logger.info('Nothing to say')

    def default_is_proper(self, event):
        """on call, checks if message value is in the keyboard button options for source state"""
        assert event.transition.source == self.state
        chat_id = event.kwargs.get('chat_id')
        message = event.kwargs.get('message').lower()
        source = event.transition.source.upper()
        try:
            options = helpers.get_keyboard_options(enums.KEYBOARDS[source])
            if message in options:
                logger.info('valid: {}'.format(message))
                return True
            else:
                logger.info('not valid: {}'.format(message))
                self.bot.send_message(
                    chat_id=chat_id,
                    text="Sorry that's not a proper answer")
                return False

        except KeyError:
            logger.exception('default_is_proper called for state with no keyboard')
