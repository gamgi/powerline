import logging

from telegram import ReplyKeyboardRemove

import enums

# General state actions for a transitions.Machine


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
            logging.info('Sent message')
        except KeyError:
            logging.info('Nothing to say')

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
            logging.info('Sent message')
        except KeyError:
            logging.info('Nothing to say')
